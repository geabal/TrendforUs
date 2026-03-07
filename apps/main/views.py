from django.shortcuts import render
from django.utils import timezone

from base.api_module import get_search_result
from base.format_module import format_search_volume
from apps.trend.models import TrendKeyword

def index(request):
    today = timezone.localdate()

    # 오늘의 트렌드 키워드 조회 (언급량 내림차순, 최대 6개)
    trend_keywords = TrendKeyword.objects.filter(date=today).order_by('-search_volume')[:6]

    trends = []
    news_by_keyword = []

    for trend in trend_keywords:
        # 트렌드 요약 카드 데이터 구성
        trends.append({
            'keyword': trend.keyword,
            'search_volume': format_search_volume(trend.search_volume),
            'description': trend.description[0] if trend.description else '',
            'related': trend.related,
        })

        # 키워드별 뉴스 검색
        news_list = []
        try:
            result = get_search_result(trend.keyword)
            news_list = result.get('result', [])[:3]
        except Exception:
            news_list = []

        news_by_keyword.append({
            'keyword': trend.keyword,
            'news_list': news_list,
        })

    context = {
        'trends': trends,
        'news_by_keyword': news_by_keyword,
        'has_trends': len(trends) > 0,
    }

    return render(request, 'main/index.html', context)