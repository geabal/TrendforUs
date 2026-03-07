
from ulid import ULID
from django.db import models


def generate_ulid():
    """ULID 문자열을 생성해 반환합니다."""
    return str(ULID())


class TrendKeyword(models.Model):
    """
    매일 수집되는 트렌드 키워드 정보를 저장하는 모델.
    하루치 데이터만 유지하며, 전날 데이터는 매일 06:20에 자동 삭제됩니다.
    """

    id = models.CharField(
        max_length=26,
        primary_key=True,
        default=generate_ulid,
        editable=False,
        verbose_name="ULID",
    )
    date = models.DateField(
        verbose_name="집계 일자",
        help_text="트렌드 데이터가 집계된 날짜 (API의 today 파라미터 값)",
    )
    keyword = models.CharField(
        max_length=100,
        verbose_name="트렌드 키워드",
    )
    search_volume = models.IntegerField(
        verbose_name="검색량",
        help_text="API의 search_volume 값",
    )
    trend_time = models.IntegerField(
        verbose_name="트렌드 유지 시간",
        help_text="트렌드가 유지된 시간 (API 제공 단위 그대로 저장)",
    )
    related = models.JSONField(
        verbose_name="연관검색어",
        default=list,
        help_text='연관검색어 리스트. 예: ["연관어1", "연관어2"]',
    )
    description = models.JSONField(
        verbose_name="AI 요약 문장",
        default=list,
        help_text='AI가 생성한 요약 문장 리스트. 예: ["문장1", "문장2"]',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="레코드 생성 시각",
    )

    class Meta:
        unique_together = ("date", "keyword")
        ordering = ["-search_volume"]  # 기본 정렬: 검색량 내림차순
        verbose_name = "트렌드 키워드"
        verbose_name_plural = "트렌드 키워드 목록"

    def __str__(self):
        return f"[{self.date}] {self.keyword} ({self.search_volume:,})"