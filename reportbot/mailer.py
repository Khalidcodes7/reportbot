"""Send the Excel report by email (via SendGrid, with a safe local fallback)."""
from __future__ import annotations

import base64
import os
from email.message import EmailMessage
from pathlib import Path
from typing import Optional

import requests


def send_report(
    to_email: str,
    subject: str,
    body: str,
    attachment_path: str,
    from_email: Optional[str] = None,
) -> str:
    """
    Send an email with the given attachment.

    If SENDGRID_API_KEY and REPORTBOT_FROM env vars are set, sends via SendGrid.
    Otherwise, saves the email as a .eml file (openable in any mail client)
    so you can preview the result without any credentials.
    """
    api_key = os.environ.get("SENDGRID_API_KEY", "").strip()
    sender = (from_email or os.environ.get("REPORTBOT_FROM", "")).strip()

    attachment = Path(attachment_path)
    if not attachment.exists():
        raise FileNotFoundError(f"Attachment not found: {attachment_path}")

    # Build the message
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender or "reportbot@example.com"
    msg["To"] = to_email
    msg.set_content(body)
    msg.add_attachment(
        attachment.read_bytes(),
        maintype="application",
        subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=attachment.name,
    )

    # Fallback mode: no credentials -> save to disk
    if not api_key or not sender:
        out = Path("output") / "would_send.eml"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(msg.as_bytes())
        print("[mailer] SENDGRID_API_KEY / REPORTBOT_FROM not set.")
        print(f"[mailer] Saved preview to {out} (open with any mail client).")
        return str(out)

    # Real send via SendGrid v3
    payload = {
        "personalizations": [{"to": [{"email": to_email}]}],
        "from": {"email": sender},
        "subject": subject,
        "content": [{"type": "text/plain", "value": body}],
        "attachments": [
            {
                "content": base64.b64encode(attachment.read_bytes()).decode(),
                "filename": attachment.name,
                "type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            }
        ],
    }

    resp = requests.post(
        "https://api.sendgrid.com/v3/mail/send",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=30,
    )
    if resp.status_code >= 400:
        raise RuntimeError(f"SendGrid error {resp.status_code}: {resp.text}")

    print(f"[mailer] Sent report to {to_email}")
    return "sent"