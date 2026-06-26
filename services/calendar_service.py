# services/calendar_service.py

from google_calendar import get_calendar_service, register_matches


def add_matches_to_calendar(matches):
    """
    試合をGoogleカレンダーに登録する（完全委任）
    """

    if not matches:
        return []

    service = get_calendar_service()

    # 実際の登録処理は全部google_calendar側へ
    links = register_matches(service, matches)

    return links