from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework import (
    generics, response, status, 
    permissions, serializers, filters
)

from core.pagination import CustomPagination

from users.models import User

from user_profile.models import EmployerProfile

from jobs.models import JobDetails

from .serializers import (
    UpdateAboutSerializers,
    CreateJobsSerializers,
    GetJobsSerializers
)


class UpdateAboutView(generics.GenericAPIView):

    serializer_class = UpdateAboutSerializers
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        context = dict()
        profile_instance = get_object_or_404(JobSeekerProfile, user=request.user)
        serializer = self.serializer_class(data=request.data, instance=profile_instance, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            if serializer.update(profile_instance, serializer.validated_data):
                context['message'] = "Updated Successfully"
                return response.Response(
                    data=context,
                    status=status.HTTP_200_OK
                )
        except serializers.ValidationError:
            return response.Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
