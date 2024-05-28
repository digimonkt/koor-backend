from django.core.management.base import BaseCommand
from random import randint
from django.template.defaultfilters import slugify
from jobs.models import JobDetails


class Command(BaseCommand):
    help = 'Update slugs for JobDetails instances where slug is not added'

    def handle(self, *args, **options):
        job_details = JobDetails.objects.all()
        for job_detail in job_details:
            
            unique_slug = slugify(job_detail.title)
            counter = 1
            while JobDetails.objects.filter(slug=unique_slug).exclude(pk=job_detail.pk).exists():
                unique_slug = f"{unique_slug}-{counter}"
                counter += 1
            JobDetails.objects.filter(pk=job_detail.pk).update(slug=unique_slug)
            self.stdout.write(self.style.SUCCESS(f'Slug added for JobDetails instance with id {job_detail.id}'))