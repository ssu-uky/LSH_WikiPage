from django.core.management.base import BaseCommand
import random
from faker import Faker
from boards.models import Board
from django.conf import settings
import pytz


class Command(BaseCommand):
    help = "게시글을 생성합니다."

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=50,
            type=int,
            help="생성할 게시글의 수를 지정합니다.",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        faker = Faker("ko_KR")
        timezone = pytz.timezone(settings.TIME_ZONE)

        coding_terms = [
            "Python",
            "Django",
            "JavaScript",
            "HTML",
            "CSS",
            "React",
            "Vue",
            "Angular",
            "Java",
            "Spring",
            "C",
            "C++",
        ]

        posts = []

        for _ in range(number):
            title = f"{random.choice(coding_terms)} 강의"
            content = (
                f"안녕하세요. 오늘 소개할 강의는 {title} 입니다. "
                + faker.text(max_nb_chars=150)
            )

            created_at = faker.date_time_between(
                start_date="-1y", end_date="now", tzinfo=timezone
            )

            updated_at = faker.date_time_between(
                start_date=created_at, end_date="now", tzinfo=timezone
            )

            posts.append(
                Board(
                    title=title,
                    content=content,
                    created_at=created_at,
                    updated_at=updated_at,
                )
            )

        sorted_posts = sorted(posts, key=lambda x: x.created_at)

        for post in sorted_posts:
            Board.objects.create(
                title=post.title,
                content=post.content,
                created_at=post.created_at,
                updated_at=post.updated_at,
            )

            # Board.objects.create(
            #     title=title,
            #     content=content,
            #     created_at=created_at,
            #     updated_at=updated_at,
            # )

        self.stdout.write(self.style.SUCCESS(f"{number}개의 게시글이 생성되었습니다."))
