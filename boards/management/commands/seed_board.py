from django.core.management.base import BaseCommand
import random
from faker import Faker
from boards.models import Board


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

        for _ in range(number):
            title = f"{random.choice(coding_terms)} 강의"
            content = (
                f"안녕하세요. 오늘 소개할 강의는 {random.choice(coding_terms)} 입니다. "
                + faker.text(max_nb_chars=150)
            )
            Board.objects.create(title=title, content=content)

        self.stdout.write(self.style.SUCCESS(f"{number}개의 게시글이 생성되었습니다."))
