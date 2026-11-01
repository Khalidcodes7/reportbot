# ReportBot

[![CI](https://github.com/Khalidcodes7/reportbot/actions/workflows/ci.yml/badge.svg)](https://github.com/Khalidcodes7/reportbot/actions)

Scrape data from a website, generate an Excel report with charts, and email it. All in one script.

I built this to automate weekly reporting tasks so I don't have to manually copy data and email Excel files every week.

## Features

- Scrapes data using ScrapeKit
- Generates formatted Excel files with auto-sized columns and charts (using openpyxl)
- Sends the file via SendGrid (or saves a `.eml` file if no credentials are set)
- Config-driven (YAML)

## Installation

```bash
git clone https://github.com/Khalidcodes7/reportbot.git
cd reportbot
pip install -e .