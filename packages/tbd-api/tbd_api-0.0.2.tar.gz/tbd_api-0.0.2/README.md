# TorrentBD API

Unofficial API for TorrentBD with search and profile access.

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 📋 Overview

TorrentBD API is a Python package that wraps the TorrentBD website into a RESTful API. It handles authentication, session management, and parsing of web content.

## ⚠️ Disclaimer

This project is not affiliated with or endorsed by TorrentBD. This is an unofficial API created for educational purposes only. Use at your own risk.

## 🚀 Installation

```bash
pip install tbd-api
```

## 🖥️ System Requirements

For login functionality:
- Chrome or Chromium browser
- ChromeDriver (compatible with your Chrome/Chromium version)
- v3cap package (automatically installed as dependency for reCAPTCHA handling)

Note: The login process uses v3cap for automated reCAPTCHA solving.

## 🔧 Quick Start

```bash
# Basic usage (uses saved config if available)
tbd-api

# With credentials (automatically saved to config)
tbd-api --username "user" --password "pass" --totp-secret "secret"

# Custom host and port
tbd-api --host "127.0.0.1" --port 8000
```

## 📋 Command-Line Arguments

```
usage: tbd-api [-h] [--username USERNAME] [--password PASSWORD] [--totp-secret TOTP_SECRET] 
               [--port PORT] [--host HOST] [--cookies COOKIES]

options:
  -h, --help            show this help message and exit
  --username USERNAME   TorrentBD username
  --password PASSWORD   TorrentBD password
  --totp-secret TOTP_SECRET
                        TOTP secret for 2FA
  --port PORT           Port to run the server on (default: 5000)
  --host HOST           Host to bind the server to (default: 0.0.0.0)
  --cookies COOKIES     Path to cookies file
```

## ⚙️ Configuration

All data is automatically saved in `~/.config/tbd-api/`:
- Credentials and settings: `config.json`
- Login cookies: `cookies.txt`

### Environment Variables

You can also use a `.env` file in the project folder:
```
USERNAME=your_username
PASSWORD=your_password
TOTP_SECRET=your_totp_secret
```

## 🔗 API Endpoints

| Endpoint | Description | Parameters |
|----------|-------------|------------|
| `/search` | Search torrents | `query` (required): Search term<br>`page` (optional): Page number (default: 1) |
| `/profile` | Get user profile | None |

## 🔐 Authentication Flow

The application follows this authentication sequence:
1. First tries to use existing cookies if available
2. If cookies are invalid, attempts login with credentials from:
   - Command-line arguments
   - Environment variables
   - Saved configuration file
3. Successfully authenticated session cookies are saved for future use

## 🐳 Docker

Build and run with Docker:

```bash
# Build the image
docker build -t tbd-api .

# Run the container
docker run -p 5000:5000 tbd-api --username "user" --password "pass" --totp-secret "secret"

# or
docker run --env-file .env -p 5000:5000 tbd-api
```

## 🛠️ Development

Clone the repository and install in development mode:

```bash
git clone https://github.com/TanmoyTheBoT/torrentbd-api.git
cd torrentbd-api
pip install .
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 