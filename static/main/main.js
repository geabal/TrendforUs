/**
 * 검색어 입력 후 Enter 키 처리
 */
function handleSearchKeydown(event) {
    if (event.key === 'Enter') {
        goSearch();
    }
}

/**
 * 검색 페이지로 이동
 */
function goSearch() {
    const query = document.getElementById('mainSearchInput').value.trim();
    if (query) {
        window.location.href = '/search/?q=' + encodeURIComponent(query);
    }
}