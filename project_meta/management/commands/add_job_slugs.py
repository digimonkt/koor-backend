from django.core.management.base import BaseCommand
from jobs.models import JobDetails


class Command(BaseCommand):
    help = 'Add slugs for JobDetails instances where slug is not added'

    def handle(self, *args, **options):
        job_details_without_slug = JobDetails.objects.filter(slug__isnull=True)
        for job_detail in job_details_without_slug:
            job_detail.save()
            self.stdout.write(self.style.SUCCESS(f'Slug added for JobDetails instance with id {job_detail.id}'))