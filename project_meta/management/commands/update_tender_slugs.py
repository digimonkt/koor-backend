from django.core.management.base import BaseCommand
from random import randint
from django.template.defaultfilters import slugify
from tenders.models import TenderDetails


class Command(BaseCommand):
    help = 'Add slugs for TenderDetails instances where slug is not added'

    def handle(self, *args, **options):
        tender_details = TenderDetails.objects.all()
        for tender_detail in tender_details:
            unique_slug = slugify(tender_detail.title)
            counter = 1
            while TenderDetails.objects.filter(slug=unique_slug).exclude(pk=tender_detail.pk).exists():
                unique_slug = f"{unique_slug}-{counter}"
                counter += 1
                
            TenderDetails.objects.filter(pk=tender_detail.pk).update(slug=unique_slug)
            self.stdout.write(self.style.SUCCESS(f'Slug added for TenderDetails instance with id {tender_detail.id}'))
