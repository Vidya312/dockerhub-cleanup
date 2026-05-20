import os
import re
import json
import boto3
import requests
from datetime import datetime, timezone
from dateutil import parser

# =========================
# CONFIG
# =========================

DOCKER_USER = os.environ["DOCKERHUB_USERNAME"]
DOCKER_TOKEN = os.environ["DOCKERHUB_TOKEN"]
NAMESPACE = os.environ["DOCKERHUB_NAMESPACE"]

SLACK_WEBHOOK = os.environ["SLACK_WEBHOOK_URL"]
SNS_TOPIC_ARN = os.environ["SNS_TOPIC_ARN"]

DRY_RUN = os.environ.get("DRY_RUN", "true").lower() == "true"

BASE_URL = "https://hub.docker.com/v2"

KEEP_LAST_N = 20

DELETE_AFTER_DAYS = {
    r"^pr-.*": 3,
    r"^feature-.*": 7,
    r"^nightly-.*": 2,
    r"^dev-.*": 5,
}

PROTECTED_TAGS = ["latest", "prod", "stable"]

PROTECTED_REGEX = [r"^v\d+\.\d+\.\d+$"]

session = requests.Session()
sns = boto3.client("sns")

# =========================
# AUTH
# =========================

def login():
    resp = session.post(
        f"{BASE_URL}/users/login/",
        json={"username": DOCKER_USER, "password": DOCKER_TOKEN}
    )
    resp.raise_for_status()

    token = resp.json()["token"]

    session.headers.update({
        "Authorization": f"JWT {token}"
    })

# =========================
# LIST REPOSITORIES (NEW)
# =========================

def fetch_repositories():
    repos = []

    url = f"{BASE_URL}/repositories/{NAMESPACE}/?page_size=100"

    while url:
        resp = session.get(url)
        resp.raise_for_status()

        data = resp.json()

        repos.extend(data["results"])

        url = data["next"]

    return [r["name"] for r in repos]

# =========================
# FETCH TAGS
# =========================

def fetch_tags(repo):
    tags = []

    url = f"{BASE_URL}/repositories/{NAMESPACE}/{repo}/tags?page_size=100"

    while url:
        resp = session.get(url)
        resp.raise_for_status()

        data = resp.json()

        tags.extend(data["results"])

        url = data["next"]

    return tags

# =========================
# RULES
# =========================

def is_protected(tag):
    name = tag["name"]

    if name in PROTECTED_TAGS:
        return True

    for pattern in PROTECTED_REGEX:
        if re.match(pattern, name):
            return True

    return False


def should_delete(tag):
    name = tag["name"]

    if is_protected(name):
        return False

    updated = parser.parse(tag["last_updated"])
    age_days = (datetime.now(timezone.utc) - updated).days

    for pattern, max_days in DELETE_AFTER_DAYS.items():
        if re.match(pattern, name) and age_days > max_days:
            return True

    return False

# =========================
# DELETE TAG
# =========================

def delete_tag(repo, tag_name):
    url = f"{BASE_URL}/repositories/{NAMESPACE}/{repo}/tags/{tag_name}/"

    if DRY_RUN:
        return {"repo": repo, "tag": tag_name, "status": "DRY_RUN"}

    resp = session.delete(url)

    if resp.status_code in [202, 204]:
        return {"repo": repo, "tag": tag_name, "status": "DELETED"}

    return {"repo": repo, "tag": tag_name, "status": "FAILED", "error": resp.text}

# =========================
# NOTIFICATIONS
# =========================

def send_slack(msg):
    requests.post(SLACK_WEBHOOK, json={"text": msg}, timeout=10)


def publish_sns(subject, msg):
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject=subject,
        Message=msg
    )

# =========================
# MAIN LAMBDA
# =========================

def lambda_handler(event, context):

    login()

    repos = fetch_repositories()

    summary = {
        "total_repos": len(repos),
        "results": [],
        "deleted_count": 0,
        "dry_run": DRY_RUN
    }

    for repo in repos:

        tags = fetch_tags(repo)

        if not tags:
            continue

        # sort by newest first
        tags_sorted = sorted(
            tags,
            key=lambda x: parser.parse(x["last_updated"]),
            reverse=True
        )

        keep_set = set([t["name"] for t in tags_sorted[:KEEP_LAST_N]])

        deleted = []

        for tag in tags_sorted:

            name = tag["name"]

            if name in keep_set:
                continue

            if is_protected(tag):
                continue

            if should_delete(tag):
                result = delete_tag(repo, name)
                deleted.append(result)

        summary["results"].append({
            "repo": repo,
            "deleted": len(deleted)
        })

        summary["deleted_count"] += len(deleted)

    message = json.dumps(summary, indent=2)

    publish_sns("DockerHub Multi-Repo Cleanup", message)

    send_slack(
        f"""
DockerHub Cleanup Completed

Namespace: {NAMESPACE}
Repos Scanned: {len(repos)}
Total Deleted: {summary['deleted_count']}
DryRun: {DRY_RUN}
"""
    )

    return {
        "statusCode": 200,
        "body": summary
    }
