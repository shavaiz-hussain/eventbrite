import logging
from django.core.management.base import BaseCommand, CommandError
from events.eventbrite_adpater import EventbriteAdapter

logger = logging.getLogger("app")



class Command(BaseCommand):
    help = 'Pull the Organization Id from eventbrite'

    def handle(self, *args, **options):
        adapter = EventbriteAdapter()
        org_id = adapter.get_organization_id()
        print(org_id)




