import httpx
from bs4 import BeautifulSoup
from datetime import datetime
from sqlalchemy.orm import Session
from models.database import ComplianceAlert

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

COMPLIANCE_SOURCES = [
    {
        "url": "https://labour.gov.in/whats-new",
        "law_area": "labour",
        "name": "Ministry of Labour"
    },
    {
        "url": "https://www.meity.gov.in/content/notifications",
        "law_area": "data_privacy",
        "name": "MeitY Data Privacy"
    },
    {
        "url": "https://www.mca.gov.in/content/mca/global/en/acts-rules/ebooks/notifications.html",
        "law_area": "corporate",
        "name": "MCA Corporate"
    },
]


def fetch_updates_from_source(source: dict) -> list:
    alerts = []
    try:
        with httpx.Client(headers=HEADERS, timeout=15, follow_redirects=True) as client:
            response = client.get(source["url"])
            response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.find_all(["li", "div", "tr"], limit=10)

        for item in items[:5]:
            text = item.get_text(strip=True)
            if len(text) < 20:
                continue

            link_tag = item.find("a")
            source_url = ""
            if link_tag and link_tag.get("href"):
                href = link_tag.get("href")
                source_url = href if href.startswith("http") else source["url"]

            alerts.append({
                "title": text[:150],
                "description": text[:500],
                "law_area": source["law_area"],
                "severity": "info",
                "source_url": source_url or source["url"],
            })

    except Exception as e:
        print(f"[Compliance] Error fetching {source['name']}: {e}")

    return alerts


def refresh_compliance_alerts(db: Session):
    print("[Compliance] Refreshing compliance alerts...")
    new_count = 0

    for source in COMPLIANCE_SOURCES:
        alerts = fetch_updates_from_source(source)
        for alert_data in alerts:
            existing = db.query(ComplianceAlert).filter(
                ComplianceAlert.title == alert_data["title"],
                ComplianceAlert.law_area == alert_data["law_area"]
            ).first()

            if not existing:
                alert = ComplianceAlert(**alert_data)
                db.add(alert)
                new_count += 1

    db.commit()
    print(f"[Compliance] Added {new_count} new alerts.")


def get_active_alerts(db: Session, law_area: str = None) -> list:
    query = db.query(ComplianceAlert).filter(ComplianceAlert.is_active == True)
    if law_area:
        query = query.filter(ComplianceAlert.law_area == law_area)
    return query.order_by(ComplianceAlert.fetched_at.desc()).limit(50).all()
