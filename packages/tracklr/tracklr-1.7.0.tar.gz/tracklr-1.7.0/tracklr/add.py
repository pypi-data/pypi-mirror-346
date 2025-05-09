import logging

from datetime import datetime
from datetime import timedelta

from cliff.command import Command
from tracklr import Tracklr


class Add(Command):

    log = logging.getLogger(__name__)

    tracklr = Tracklr()

    def take_action(self, parsed_args):
        """Add calendar event."""
        self.tracklr.banner(
            parsed_args.kalendar, parsed_args.title, parsed_args.subtitle
        )

        if parsed_args.begin_datetime is None:
            now = datetime.now()
            parsed_args.begin_datetime = now.strftime("%Y-%m-%dT%H:%M:%S")

        if parsed_args.end_datetime is None:
            in_hour = now + timedelta(hours=1)
            parsed_args.end_datetime = in_hour.strftime("%Y-%m-%dT%H:%M:%S")

        response = self.tracklr.add_event(
            parsed_args.kalendar,
            parsed_args.begin_datetime,
            parsed_args.end_datetime,
            parsed_args.name,
            parsed_args.description,
        )
        self.log.info(f"id:{response}")

    def get_description(self):
        return "add calendar event"

    def get_parser(self, prog_name):
        parser = super(Add, self).get_parser(prog_name)
        parser.add_argument("-n", "--name", required=True)
        parser.add_argument("-d", "--description")
        parser.add_argument("-b", "--begin_datetime")
        parser.add_argument("-e", "--end_datetime")
        return self.tracklr.get_base_parser(parser)
