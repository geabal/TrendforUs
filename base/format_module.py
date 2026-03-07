

def format_search_volume(volume: int) -> str:
    """
    언급량을 사람이 읽기 좋은 형식으로 변환.
    1,000 이상이면 k 단위로 표시 (예: 1500 → 1.5k).
    """
    if volume >= 1000:
        formatted = volume / 1000
        # 소수점이 0이면 정수로 표시 (예: 2.0k → 2k)
        if formatted == int(formatted):
            return f"{int(formatted)}k"
        return f"{formatted:.1f}k"
    return str(volume)