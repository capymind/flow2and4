"""
This is the module for helpers related to pyduck community.
"""

from datetime import datetime, timedelta, timezone

today = datetime.now(timezone.utc).date()

date_filters = [
    {"code": "created_at-ge-past_day", "name": "최근 하루", "value": today.isoformat()},
    {
        "code": "created_at-ge-past_week",
        "name": "최근 일주",
        "value": (today - timedelta(days=7)).isoformat(),
    },
    {
        "code": "created_at-ge-past_month",
        "name": "최근 한달",
        "value": (today - timedelta(days=30)).isoformat(),
    },
    {
        "code": "created_at-ge-past_year",
        "name": "최근 일년",
        "value": (today - timedelta(days=365)).isoformat(),
    },
    {"code": "created_at-ge-all", "name": "전체", "value": "1"},
]
