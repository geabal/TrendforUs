from django.shortcuts import render
from base.api_module import get_search_result
from django.core.paginator import Paginator

PAGE_SIZE = 10
PAGE_WINDOW = 2
def search(request):
    user_query = request.GET.get("q", "").strip()
    current_page = int(request.GET.get("page", 1))

    results = []
    total = 0
    error = None
    page_range = []
    total_pages = 1

    if user_query:
        try:
            data = get_search_result(user_query)

            all_results = data.get("result", [])
            total = len(all_results)

            paginator = Paginator(all_results, PAGE_SIZE)
            page_obj = paginator.get_page(current_page)
            results = page_obj.object_list
            total_pages = paginator.num_pages

            # 페이지 번호 범위 계산 (최대 5개, 현재 페이지 중앙)
            start = max(1, current_page - PAGE_WINDOW)
            end = min(total_pages, current_page + PAGE_WINDOW)

            # 5개 미만이면 범위 보정
            if end - start + 1 < 5:
                if start == 1:
                    end = min(total_pages, start + 4)
                elif end == total_pages:
                    start = max(1, end - 4)

            page_range = range(start, end + 1)
        
        # 에러 메시지 부분은 디버깅용 메시지. 배포 시 삭제 필요
        except Exception as e:
            error = f"검색 서버에 연결할 수 없습니다. 잠시 후 다시 시도해 주세요."

    context = {
        "query": user_query,
        "results": results,
        "total": total,
        "current_page": current_page,
        "total_pages": total_pages,
        "page_range": page_range,
        "error": error,
    }

    return render(request, 'search/search.html', context)
