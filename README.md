# Docker Hub Cleanup

**A comprehensive utility for managing and cleaning up Docker Hub repositories, images, and resources efficiently.**

---

## Table of Contents

- **[Overview](#overview)**
- **[Features](#features)**
- **[Prerequisites](#prerequisites)**
- **[Installation](#installation)**
- **[Configuration](#configuration)**
- **[Usage](#usage)**
- **[Command-Line Options](#command-line-options)**
- **[Contributing](#contributing)**
- **[License](#license)**
- **[Security](#security)**
- **[Support](#support)**

---

## Overview

**Docker Hub Cleanup is a powerful tool designed to help developers and DevOps engineers maintain their Docker Hub namespaces by automating the removal of unused or outdated images, tags, and repositories. This utility streamlines repository management and helps optimize storage resources.**

---

## Features

- **Automated Cleanup** - **Remove unused Docker images and tags automatically**
- **Batch Operations** - **Process multiple repositories efficiently**
- **Smart Filtering** - **Filter images by age, tags, or custom criteria**
- **Detailed Logging** - **Comprehensive logs for audit and tracking purposes**
- **Secure Authentication** - **Safe credential handling for Docker Hub API**
- **Performance Optimized** - **Fast processing of large image repositories**
- **Dry-Run Mode** - **Preview changes before applying them**
- **Detailed Reports** - **Generate cleanup reports and statistics**
- **Scheduled Tasks** - **Automate cleanup on a schedule**

---

## Prerequisites

**Before getting started, ensure you have the following installed:**

- **Python 3.7 or higher**
- **Docker Hub account with API credentials**
- **pip (Python package manager)**
- **Git (for version control)**

---

## Installation

**Clone the repository:**

```bash
git clone https://github.com/Vidya312/dockerhub-cleanup.git
cd dockerhub-cleanup
```

**Install dependencies:**

```bash
pip install -r requirements.txt
```

**Verify installation:**

```bash
python cleanup.py --version
```

---

## Configuration

**Create a `.env` file in the project root directory:**

```env
DOCKERHUB_USERNAME=your_username
DOCKERHUB_PASSWORD=your_password_or_token
DOCKERHUB_API_URL=https://hub.docker.com/v2
LOG_LEVEL=INFO
```

**Alternatively, set environment variables:**

```bash
export DOCKERHUB_USERNAME=your_username
export DOCKERHUB_PASSWORD=your_password_or_token
export DOCKERHUB_API_URL=https://hub.docker.com/v2
```

---

## Usage

### **Basic Usage**

```bash
python cleanup.py --help
```

### **Remove Old Images**

**Keep only images from the last 30 days:**

```bash
python cleanup.py --keep-days 30
```

### **Dry-Run Mode**

**Preview what will be deleted without making changes:**

```bash
python cleanup.py --keep-days 30 --dry-run
```

### **Clean Specific Repository**

**Remove old images from a specific repository:**

```bash
python cleanup.py --repository my-repo --keep-days 14
```

### **Remove Untagged Images**

**Delete all untagged images:**

```bash
python cleanup.py --remove-untagged
```

### **Verbose Output**

**Enable detailed logging:**

```bash
python cleanup.py --keep-days 30 --verbose
```

---

## Command-Line Options

| **Option** | **Description** |
|---|---|
| `--help` | **Show help message and exit** |
| `--version` | **Display the version number** |
| `--repository` | **Specify a single repository to clean** |
| `--keep-days` | **Keep images newer than specified days (default: 30)** |
| `--remove-untagged` | **Remove all untagged images** |
| `--dry-run` | **Preview changes without applying them** |
| `--verbose` | **Enable verbose logging output** |
| `--config` | **Path to configuration file** |

---

## Contributing

**We welcome contributions! Please follow these steps:**

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

**Please ensure your code follows our style guidelines and includes appropriate tests.**

---

## License

**This project is licensed under the MIT License - see the** [**LICENSE**](LICENSE) **file for details.**

---

## Security

### **Important Security Notes:**

- **Never commit credentials or `.env` files to version control**
- **Use Docker Hub access tokens instead of passwords when possible**
- **Ensure proper file permissions on configuration files** (`chmod 600 .env`)
- **Review dry-run results before executing cleanup operations**
- **Rotate access tokens regularly**
- **Monitor API usage and rate limits**

---

## Support

**For issues, questions, or suggestions, please:**

- **Open an** [**Issue**](https://github.com/Vidya312/dockerhub-cleanup/issues)
- **Check existing documentation and FAQs**
- **Review the** [**Discussions**](https://github.com/Vidya312/dockerhub-cleanup/discussions) **section**

---

## Changelog

**See** [**CHANGELOG.md**](CHANGELOG.md) **for version history and updates.**

---

## Disclaimer

**Use this tool with caution. Always verify dry-run results before performing actual cleanup operations. The author is not responsible for unintended data loss. Test in a non-production environment first.**

---

**Repository:** [**Vidya312/dockerhub-cleanup**](https://github.com/Vidya312/dockerhub-cleanup)

**Last Updated:** **2026-05-20**
