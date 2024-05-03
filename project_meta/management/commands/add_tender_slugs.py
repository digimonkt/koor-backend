from django.core.management.base import BaseCommand
from tenders.models import TenderDetails


class Command(BaseCommand):
    help = 'Add slugs for TenderDetails instances where slug is not added'

    def handle(self, *args, **options):
        TenderDetails_without_slug = TenderDetails.objects.filter(slug__isnull=True)
        for TenderDetail in TenderDetails_without_slug:
            TenderDetail.save()
            self.stdout.write(self.style.SUCCESS(f'Slug added for TenderDetails instance with id {TenderDetail.id}'))