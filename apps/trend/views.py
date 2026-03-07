import requests
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .models import TrendKeyword
from base.api_module import get_search_result
from base.format_module import format_search_volume
def trend(request):
    return render(request, 'trend/trend.html')

NEWS_MAX_COUNT = 4

def _fetch_related_news(keyword: str) -> list:
    """
    검색 API를 호출하여 키워드 관련 뉴스를 최대 NEWS_MAX_COUNT개 반환.
    호출 실패 시 빈 리스트 반환.
    """
    try:
        data = get_search_result(keyword)
        return data.get("result", [])[:NEWS_MAX_COUNT]
    except Exception:
        return []

def trend_detail(request, keyword: str):
    """
    트렌드 키워드 상세 페이지 뷰.

    - DB에서 오늘 날짜 기준으로 해당 키워드 레코드 조회
    - 데이터 없을 경우 404
    - 검색 API로 관련 뉴스 최대 4개 조회
    """
    today = timezone.localdate()

    trend = get_object_or_404(TrendKeyword, keyword=keyword, date=today)

    news_list = _fetch_related_news(keyword)

    context = {
        "keyword": trend.keyword,
        "date": trend.date.strftime("%Y.%m.%d"),
        "search_volume": format_search_volume(trend.search_volume),
        "related": trend.related,           # list
        "description": trend.description,   # list
        "news_list": news_list,
    }
    return render(request, "trend/detail.html", context)