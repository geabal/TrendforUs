from datetime import datetime


def parse_published_date(date_str: str) -> datetime | None:
    """
    검색 API에서 반환하는 datetime 객체 표현형 문자열을 datetime으로 파싱합니다.
    "None" 문자열이거나 파싱에 실패하면 None을 반환합니다.

    지원 형식 예시:
      - "2026-04-10 14:30:00"
      - "2026-04-10 14:30:00.123456"
      - "2026-04-10T14:30:00"
    """
    if not date_str or date_str.strip().lower() == "none":
        return None

    formats = [
        "%Y-%m-%d %H:%M:%S.%f",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue

    return None


def format_relative_time(date_str: str) -> str | None:
    """
    날짜 문자열을 현재 시각 기준 상대 시간 문자열로 변환합니다.

    반환 규칙:
      - 1시간 미만  → "N분 전"  (0분인 경우 "방금 전")
      - 24시간 미만 → "N시간 전"
      - 7일 미만    → "N일 전"
      - 30일 미만   → "N주일 전"
      - 12개월 미만 → "N개월 전"
      - 12개월 이상 → "yyyy.mm.dd"
      - 파싱 실패 또는 "None" → None (UI에 날짜를 표시하지 않음)
    """
    parsed = parse_published_date(date_str)
    if parsed is None:
        return None

    now = datetime.now()
    diff = now - parsed
    total_seconds = int(diff.total_seconds())

    # 미래 날짜 방어 처리
    if total_seconds < 0:
        return "방금 전"

    minutes = total_seconds // 60
    hours = total_seconds // 3600
    days = diff.days
    weeks = days // 7
    months = days // 30

    if minutes < 1:
        return "방금 전"
    elif hours < 1:
        return f"{minutes}분 전"
    elif hours < 24:
        return f"{hours}시간 전"
    elif days < 7:
        return f"{days}일 전"
    elif days < 30:
        return f"{weeks}주 전"
    elif months < 12:
        return f"{months}개월 전"
    else:
        return parsed.strftime("%Y.%m.%d")