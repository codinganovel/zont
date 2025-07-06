# zont
**zont** is a fast, intuitive time zone converter for your terminal. It's designed to let you quickly convert times between any time zones without the hassle of opening web converters or doing mental math. Supports both quick CLI commands and an interactive TUI mode with smart autocomplete.

> No web browsers. No bookmarks. Just convert and go.

---

## ✨ Features
- Lightning-fast CLI conversions with natural syntax
- Interactive TUI mode with timezone autocomplete
- Smart time parsing (3pm, 15:30, now, full dates)
- Common timezone abbreviations (EST, PST, UTC, etc.)
- Colored output with clear visual indicators
- Automatic day change detection (+1 day, -1 day)
- Support for all IANA timezone identifiers

---

## 📦 Installation

[get yanked](https://github.com/codinganomel/yanked)

---

## 🚀 Usage

### CLI Mode (Quick Conversions)
```bash
# Basic timezone conversion
zont 3pm EST to PST

# Using full timezone names  
zont 15:30 UTC to Asia/Tokyo

# Convert current time
zont now America/New_York to Europe/London

# With full date-time
zont "2024-01-15 14:30" America/Los_Angeles to Asia/Seoul
```

### TUI Mode (Interactive)
```bash
zont --tui
```
Launches an interactive interface with:
- Smart timezone autocomplete
- Step-by-step prompts
- Beautiful formatted results
- Option to convert multiple times

---

## 🌍 Supported Timezones

### Common Abbreviations
| Abbrev | Full Name |
|--------|-----------|
| `EST` | America/New_York |
| `PST` | America/Los_Angeles |
| `MST` | America/Denver |
| `CST` | America/Chicago |
| `GMT` | Europe/London |
| `UTC` | UTC |
| `JST` | Asia/Tokyo |
| `CET` | Europe/Paris |
| `IST` | Asia/Kolkata |
| `AEST` | Australia/Sydney |

### Full IANA Database
All standard timezone identifiers are supported (e.g., `America/New_York`, `Europe/Stockholm`, `Asia/Shanghai`)

---

## ⏰ Time Formats

| Format | Example | Description |
|--------|---------|-------------|
| `3pm`, `11am` | 12-hour with AM/PM |
| `3:30pm`, `11:45am` | 12-hour with minutes |
| `15:30`, `09:15` | 24-hour format |
| `now` | Current time |
| `2024-01-15 14:30` | Full date-time |

---

## 🎨 Example Output

```
🕐 3:00 PM EST → 12:00 PM PST
🕐 11:30 PM JST → 9:30 AM EST (+1 day)
🕐 2:00 AM UTC → 7:00 PM PST (-1 day)
```

---

## 📋 Dependencies & Compatibility

**Core Dependencies** (built-in):
- `datetime` and `zoneinfo` (Python 3.9+)
- `argparse`, `re`, `os`, `sys`

**Optional Dependencies:**
- `prompt-toolkit` - For interactive TUI mode with autocomplete

### Platform Support
✅ **macOS** - Full support  
✅ **Linux** - Full support  
✅ **Windows** - Full support

---

## 📁 License
MIT

---

## ⚡ Created for Developers
Because time zone math shouldn't slow you down during standups, deployments, or coordinating with global teams.