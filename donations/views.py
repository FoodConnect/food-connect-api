from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from users.models import Donor, User

from .models import Donation

from .serializers import DonationSerializer

class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    def perform_create(self, serializer):
        user_id = self.request.data.get('donor_id')
        user = get_object_or_404(User, id=user_id)
        donor = get_object_or_404(Donor, user=user)
        serializer.save(donor=donor)
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'list':
            queryset = queryset.select_related('donor__user')
        return queryset
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        existing_donor_id = instance.donor_id
        request.data['donor_id'] = existing_donor_id
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        validated_data.pop('donor_id', None)
        self.perform_update(serializer)
        return Response(serializer.data)


