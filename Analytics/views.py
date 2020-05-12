from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet


class AnalyticsViewSet(GenericViewSet):
    @action(detail=False, methods=["post"])
    def analytics(self, request, *args, **kwargs):
        request_data = request.data.copy()
        request_data['user'] = request.user.id
        analytics_serializer = AnalyticsChildSerializer(data=request_data)
        if analytics_serializer.is_valid(raise_exception=True):
            analytics_serializer_create = analytics_serializer.create(analytics_serializer.validated_data)
            analytics_serializer_create = AnalyticsChildSerializer(analytics_serializer_create)
            return Response(status=200, data={'message': analytics_serializer_create.data})
