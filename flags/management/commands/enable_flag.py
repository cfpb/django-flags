from django.core.management.base import BaseCommand, CommandError

from flags.state import enable_flag


class Command(BaseCommand):
    help = (
        "Enables the given feature flag "
        "when any required conditions (if defined) are met"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "flag_name", help="The name of the feature flag to enable"
        )

    def handle(self, *args, **options):
        try:
            enable_flag(options["flag_name"])
        except KeyError as err:
            raise CommandError(err) from err

        self.stdout.write(
            self.style.SUCCESS(f"Successfully enabled {options['flag_name']}")
        )
