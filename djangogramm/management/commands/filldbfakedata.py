from django.core.management.base import BaseCommand, CommandError
from . import fake_fill_db


class Command(BaseCommand):
    help = "Fills database with fake data."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting fill db..."))
        fill_db_bool = fake_fill_db.main()
        if not fill_db_bool:
            raise CommandError("Something went wrong with db fills!")
        self.stdout.write(self.style.SUCCESS("Database filled successfully!"))
