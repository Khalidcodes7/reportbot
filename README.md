# ReportBot

> Scrape any website, build a formatted Excel report, and email it — automatically. One command does it all.

[![CI](https://github.com/Khalidcodes7/reportbot/actions/workflows/ci.yml/badge.svg)](https://github.com/Khalidcodes7/reportbot/actions)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

ReportBot is a complete automation pipeline: it scrapes a website, formats the data into a professional Excel workbook (with charts), and delivers it by email — on demand or on a schedule.

Built for businesses that need recurring reports without manual work: **competitor prices, marketplace listings, lead generation, research data, and more.**

---

## ✨ What it does

```
┌──────────┐    ┌──────────────┐    ┌──────────┐
│  Scrape  │ ─► │  Build Excel │ ─► │  Email   │
│  (YAML)  │    │  (formatted) │    │ (SendGrid)│
└──────────┘    └──────────────┘    └──────────┘
```

All three steps run with **one command**:

```bash
reportbot run config.yaml
```

---

## 🚀 Features

- 🎯 **Config-driven** — describe the job in YAML, no code required
- 📊 **Formatted Excel output** — title, styled headers, auto-sized columns, frozen pane
- 📈 **Built-in charts** — bar charts of any numeric column (prices, counts, scores)
- 📧 **Email delivery** — sends via SendGrid with the report attached
- 🧪 **Safe by default** — if email credentials aren't set, saves a preview `.eml` instead
- 🔁 **Reuses ScrapeKit** — powered by my own open-source scraper package
- 🧪 **Tested** — pytest suite, CI on every push
- 🖥️ **CLI + Python API**

---

## 📦 Installation

```bash
git clone https://github.com/Khalidcodes7/reportbot.git
cd reportbot
pip install -e ".[dev]"
```

---

## ⚡ Quick Start

### 1. Write a config — `my_report.yaml`

```yaml
name: books-report

start_urls:
  - https://books.toscrape.com/catalogue/page-1.html

item_selector: "css:article.product_pod"
next_page: "css:li.next a"
max_pages: 2

fetch:
  delay: 1.0
  respect_robots: true

fields:
  - name: title
    selector: "css:h3 a"
    attr: title
  - name: price
    selector: "css:p.price_color"
    transform: float
  - name: rating
    selector: "css:p.star-rating"
    attr: class
    regex: "star-rating (\\w+)"
  - name: url
    selector: "css:h3 a"
    attr: href

output:
  path: output/books_report.xlsx
  title: Books Report
  chart_column: price

email:
  to: "you@example.com"
  subject: "Books report"
  body: |
    Hi,
    Please find the latest books report attached.
    Regards,
    ReportBot
```

### 2. Set email credentials (optional)

```bash
# Windows
set SENDGRID_API_KEY=SG.xxxxxxxx
set REPORTBOT_FROM=you@example.com

# macOS/Linux
export SENDGRID_API_KEY=SG.xxxxxxxx
export REPORTBOT_FROM=you@example.com
```

If these aren't set, ReportBot still runs — it saves a preview email to `output/would_send.eml` instead of sending.

### 3. Run it

```bash
reportbot run my_report.yaml
```

**Output:**

```
INFO   Step 1/3: scraping 1 URL(s)
INFO   Scraped 40 records
INFO   Step 2/3: building Excel report -> output/books_report.xlsx
INFO   Step 3/3: emailing report to you@example.com
INFO   Done: 40 rows -> output/books_report.xlsx (3.8s)
```

You get a **styled Excel workbook** with a data sheet and a chart sheet — ready to send to a client.

---

## 🐍 Python API

```python
from reportbot import ReportConfig, run_pipeline

config = ReportConfig.from_file("my_report.yaml")
result = run_pipeline(config)

print(f"{result['rows']} rows -> {result['report']}")
```

---

## 🖥️ CLI Reference

### `reportbot run <config>`

| Flag | Description |
|------|-------------|
| `--email-to EMAIL` | Override the recipient in the config |
| `--no-email` | Skip the email step entirely |
| `--output PATH` | Override the report output path |
| `--max-pages N` | Override the number of pages to scrape |
| `-v, --verbose` | Debug logging |

---

## 📚 Config Reference

### Top-level

| Key | Description |
|-----|-------------|
| `name` | Job label (used in logs) |
| `start_urls` | One or more URLs to begin from |
| `item_selector` | Repeating item container selector |
| `next_page` | "Next page" link selector for pagination |
| `max_pages` | Stop after N pages |
| `fields` | Field definitions (see ScrapeKit docs) |
| `fetch` | Networking options (delay, retries, robots.txt) |
| `output` | `path`, `title`, `chart_column` |
| `email` | `to`, `subject`, `body` |

*(Field and fetch options are identical to ScrapeKit's — see that repo for the full reference.)*

---

## 🗂️ Project Structure

```
reportbot/
├── reportbot/
│   ├── __init__.py
│   ├── cli.py          # Command-line interface
│   ├── mailer.py       # SendGrid + local .eml fallback
│   ├── pipeline.py     # Scrape -> report -> email orchestration
│   └── report.py       # Excel writer with styling + charts
├── examples/
│   └── books.yaml      # Demo config
├── tests/
│   └── test_pipeline.py
├── .github/workflows/ci.yml
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## ⚖️ Legal & Ethical Use

This tool respects `robots.txt` by default and uses polite delays. **You are responsible** for complying with target sites' Terms of Service and applicable laws. Only scrape data you have the right to access.

---

## 📄 License

MIT — see [LICENSE](LICENSE).

---

## 💼 Hire Me

Need a **custom scraping + reporting pipeline** for your business? I build automation tools that:
- Extract data from any website
- Deliver it as formatted Excel reports
- Send it on a schedule — daily, weekly, or monthly

**Save hours of manual work every week.**

📧 **Contact:** k.naveedfsd1968@gmail.com  
🔗 **GitHub:** [@Khalidcodes7](https://github.com/Khalidcodes7)
