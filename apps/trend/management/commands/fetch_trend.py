"""
apps/trend/management/commands/fetch_trend.py

트렌드 API를 호출해 오늘의 키워드 데이터를 DB에 저장하거나,
오래된 데이터를 삭제하는 Management Command.

사용법:
    # 오늘 트렌드 수집 (매일 06:00 cron)
    python manage.py fetch_trend

    # 특정 날짜 트렌드 수집 (수동 재수집 시)
    python manage.py fetch_trend --date 2026-01-01

    # 오늘 날짜가 아닌 데이터 삭제 (매일 06:20 cron)
    python manage.py fetch_trend --delete-old

crontab 등록 예시:
    0  6 * * * python /path/to/trend4us/manage.py fetch_trend
    20 6 * * * python /path/to/trend4us/manage.py fetch_trend --delete-old
"""

import logging
from datetime import date

from django.core.management.base import BaseCommand, CommandError

from apps.trend.models import TrendKeyword
from base.api_module import get_trend_result

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "트렌드 API에서 오늘의 키워드 정보를 수집해 DB에 저장합니다."

    # ------------------------------------------------------------------ #
    # 인자 정의
    # ------------------------------------------------------------------ #
    def add_arguments(self, parser):
        parser.add_argument(
            "--date",
            type=str,
            default=None,
            metavar="YYYY-MM-DD",
            help="수집할 날짜를 지정합니다. 생략하면 오늘 날짜(KST)를 사용합니다.",
        )
        parser.add_argument(
            "--delete-old",
            action="store_true",
            default=False,
            help="오늘 날짜가 아닌 레코드를 모두 삭제합니다. 수집은 실행하지 않습니다.",
        )

    # ------------------------------------------------------------------ #
    # 메인 핸들러
    # ------------------------------------------------------------------ #
    def handle(self, *args, **options):
        if options["delete_old"]:
            self._delete_old_data()
        else:
            self._fetch_and_save(options["date"])

    # ------------------------------------------------------------------ #
    # 수집 로직
    # ------------------------------------------------------------------ #
    def _fetch_and_save(self, date_str: str | None):
        """트렌드 API를 호출하고 결과를 DB에 저장합니다."""

        # 날짜 결정
        if date_str is None:
            target_date = date.today()
            date_str = target_date.strftime("%Y-%m-%d")
        else:
            try:
                target_date = date.fromisoformat(date_str)
            except ValueError:
                raise CommandError(f"날짜 형식이 올바르지 않습니다: '{date_str}' (YYYY-MM-DD 형식 필요)")

        self.stdout.write(f"[fetch_trend] {date_str} 트렌드 수집 시작")

        # API 호출
        response = get_trend_result(date_str)

        if response is None:
            raise CommandError("트렌드 API 호출에 실패했습니다. 로그를 확인해주세요.")

        if response.get("state") != 200:
            raise CommandError(
                f"트렌드 API가 비정상 응답을 반환했습니다. state={response.get('state')}"
            )

        results = response.get("result", [])
        if not results:
            self.stdout.write(self.style.WARNING(f"[fetch_trend] {date_str} 수집된 키워드가 없습니다."))
            return

        # DB 저장
        saved_count = 0
        updated_count = 0

        for item in results:
            keyword = item.get("keyword", "").strip()
            if not keyword:
                logger.warning("[fetch_trend] keyword 필드가 비어있는 항목을 건너뜁니다: %s", item)
                continue

            defaults = {
                "search_volume": item.get("search_vol", 0),
                "trend_time": item.get("trend_time", 0),
                "related": item.get("related", []),
                "description": item.get("description", []),
            }

            _, created = TrendKeyword.objects.update_or_create(
                date=target_date,
                keyword=keyword,
                defaults=defaults,
            )

            if created:
                saved_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"[fetch_trend] 완료 — 신규: {saved_count}건, 갱신: {updated_count}건 (날짜: {date_str})"
            )
        )
        return

    # ------------------------------------------------------------------ #
    # 삭제 로직
    # ------------------------------------------------------------------ #
    def _delete_old_data(self):
        """오늘 날짜가 아닌 TrendKeyword 레코드를 모두 삭제합니다."""

        today = date.today()
        self.stdout.write(f"[fetch_trend] {today} 이전 데이터 삭제 시작")

        deleted_count, _ = TrendKeyword.objects.exclude(date=today).delete()

        self.stdout.write(
            self.style.SUCCESS(f"[fetch_trend] 삭제 완료 — {deleted_count}건 삭제됨")
        )
        return