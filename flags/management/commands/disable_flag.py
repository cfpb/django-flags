from django.core.management.base import BaseCommand, CommandError

from flags.state import disable_flag


class Command(BaseCommand):
    help = (
        "Disables the given feature flag "
        "unless any required conditions (if defined) are met"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "flag_name", help="The name of the feature flag to disable"
        )

    def handle(self, *args, **options):
        try:
            disable_flag(options["flag_name"])
        except KeyError as err:
            raise CommandError(err) from err

        self.stdout.write(
            self.style.SUCCESS(f"Successfully disabled {options['flag_name']}")
        )
