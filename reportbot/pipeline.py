# pipeline.py
from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import Optional

import yaml

from scrapekit import Field, ScrapeConfig, Scraper
from .mailer import send_report
from .report import build_report

logger = logging.getLogger(__name__)


@dataclass
class ReportConfig:
    name: str
    start_urls: list
    fields: list
    item_selector: Optional[str] = None
    next_page: Optional[str] = None
    max_pages: int = 1

    output_path: str = "output/report.xlsx"
    report_title: str = "Report"
    chart_column: Optional[str] = None

    email_to: str = ""
    email_subject: str = "Your report"
    email_body: str = "Hi,\n\nPlease find the latest report attached.\n\nRegards,\nReportBot"

    @classmethod
    def from_file(cls, path: str) -> "ReportConfig":
        with open(path, "r", encoding="utf-8") as handle:
            text = handle.read()

        if path.endswith((".yaml", ".yml")):
            data = yaml.safe_load(text)
        else:
            data = json.loads(text)

        output = data.pop("output", {}) or {}
        email = data.pop("email", {}) or {}
        fetch_cfg = data.pop("fetch", {}) or {}

        data.setdefault("output_path", output.get("path", "output/report.xlsx"))
        data.setdefault("report_title", output.get("title", "Report"))
        data.setdefault("chart_column", output.get("chart_column"))

        data.setdefault("email_to", email.get("to", ""))
        data.setdefault("email_subject", email.get("subject", "Your report"))
        if "body" in email:
            data.setdefault("email_body", email["body"])

        raw_fields = data.pop("fields", [])
        data["fields"] = [f if isinstance(f, Field) else Field(**f) for f in raw_fields]

        urls = data.pop("start_urls", [])
        if isinstance(urls, str):
            urls = [urls]
        data["start_urls"] = urls

        config = cls(**data)
        config._fetch = fetch_cfg
        return config

    def to_scrape_config(self) -> ScrapeConfig:
        from scrapekit import FetchConfig

        fetch_kwargs = getattr(self, "_fetch", {}) or {}
        return ScrapeConfig(
            start_urls=self.start_urls,
            fields=self.fields,
            item_selector=self.item_selector,
            next_page=self.next_page,
            max_pages=self.max_pages,
            fetch=FetchConfig(**fetch_kwargs),
        )


def run_pipeline(config: ReportConfig) -> dict:
    logger.info("Starting job: %s", config.name)

    logger.info("Scraping %d URL(s)...", len(config.start_urls))
    with Scraper(config.to_scrape_config()) as scraper:
        rows = list(scraper.run())
        
    logger.info("Scraped %d records", len(rows))
    if not rows:
        raise RuntimeError("No records scraped.")

    logger.info("Building Excel report at %s", config.output_path)
    build_report(
        rows,
        config.output_path,
        title=config.report_title,
        chart_column=config.chart_column,
    )

    result = {"rows": len(rows), "report": config.output_path, "email": "skipped"}
    
    if config.email_to:
        logger.info("Emailing report to %s", config.email_to)
        send_report(
            to_email=config.email_to,
            subject=config.email_subject,
            body=config.email_body,
            attachment_path=config.output_path,
        )
        result["email"] = config.email_to
    else:
        logger.info("No email recipient set, skipping.")

    logger.info("Done. Report at %s", config.output_path)
    return result