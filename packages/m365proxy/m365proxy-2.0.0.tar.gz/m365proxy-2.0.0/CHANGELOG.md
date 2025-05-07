# 📦 Changelog — m365proxy

## [2.0.0] - 2025-05-06

### ✨ Major Changes

- 🔐 **POP3: Added STARTTLS support**
- 🔐 **SMTP: Full SSL/TLS support (SMTPS on port 465)**
- 🧩 **Simultaneous multi-protocol support**:
  - SMTP (STARTTLS)
  - SMTPS (TLS from start)
  - POP3 (STARTTLS)
  - POP3S (TLS from start)
- 🛠️ **Completely refactored configuration parsing**:
  - robust validation for TLS, ports, paths, mailboxes, and HTTPS proxy
- 🤝 **Improved compatibility with mail clients and devices**
  - tested with Outlook, Thunderbird, network printers, scanners, etc.

### ✅ Final release for this stage

Further features like IMAP, calendars, and shared folders are outside the scope of this project. While technically feasible, their implementation would move the project toward building a full-fledged enterprise-grade mail system — which, despite being powered by Microsoft’s $2/month plans with excellent antispam and antivirus, could conflict with Microsoft’s licensing agreement, and that’s not a fight I’m looking for.

---

## [1.2.2] - 2025-05-06

### ✨ New Features

- **Fully asynchronous SMTP and POP3 proxy**
  - The proxy server is now built entirely on `asyncio`, allowing non-blocking performance and better concurrency.
- **SMTP queue and offline resend support**
  - Outgoing messages are stored on disk and retried automatically when Graph API becomes reachable.
- **HTTPS proxy support via `HTTPS_PROXY` environment variable**
  - Enables deployment behind corporate or cloud proxies.
- **Safe resend without duplication**
  - The queue system is aware of delivery status to prevent double-sending.
- **AUTH PLAIN and AUTH LOGIN for POP3**
  - Compatible with Outlook, Thunderbird, and other standard clients.

### 🔧 Improvements

- Improved logging of network/API failures
- Graph API 405/403 responses treated as valid reachability indicators
- Added architectural diagram and offline-mode documentation
- Enhanced `README.md` with structured features and examples
- Initial `docs/` folder with `mkdocs.yml` and Markdown pages

### ⚠️ Upgrade Notes

- Python 3.9 or higher is recommended
- `start_smtp_server()` is now async and must be awaited
- Queue processing and token refresh now run as background tasks

---

**Full Changelog**: https://github.com/sh0rch/m365proxy/compare/v1.1.4...v1.2.2

**Full Changelog**: https://github.com/sh0rch/m365proxy/compare/v1.2.0...v1.2.2
