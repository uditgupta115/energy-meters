from django import http
from django.conf import settings
from django.db import models as django_models
from django.shortcuts import get_object_or_404
from django.utils import dateparse
from django.views import generic

from data import models
from domain.readings import config
from domain.readings.exceptions import SupplyPointDoesNotExist
from plugins.clients.models import Client


class ReadingsView(generic.View):
    readings_config: config.ReadingsConfig
    supply_point: models.SupplyPoint

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.readings_config = config.get_config(settings.CLIENT_NAME)
        self.supply_point = self.readings_config.get_supply_point(
            kwargs["supply_point_identifier"]
        )

    def get(self, request, *args, **kwargs) -> http.HttpResponse:
        if from_dt := request.GET.get("from_dt"):
            from_dt = dateparse.parse_datetime(from_dt)
        else:
            from_dt = None
        if to_dt := request.GET.get("to_dt"):
            to_dt = dateparse.parse_datetime(to_dt)
        else:
            to_dt = None

        readings = self.readings_config.get_readings(
            supply_point=self.supply_point,
            from_dt=from_dt,
            to_dt=to_dt,
        )
        return http.JsonResponse(readings, safe=False)


class ClientBasedReadingView(generic.View):
    """
    supporting App-Id to determine the client for the request and
    accordingly handle the things
    """
    readings_config: config.ReadingsConfig
    supply_point: models.SupplyPoint
    client: None

    def prerequisites(self, request, *args, **kwargs):
        """
        checking whether App-Id is present in the request or not if yes, is it valid and
        thus supply point should also be existed in the given client else return status False
        """
        app_id = request.headers.get('App-Id')
        if not app_id:
            return http.JsonResponse(
                {
                    'status': False,
                    'error': 'App-Id header is missing!'
                },
                status=400
            )
        self.client = Client.objects.filter(
            app_id=app_id,
            is_active=True
        ).last()

        if not self.client:
            return http.JsonResponse(
                {
                    'status': False,
                    "error": "Not a valid Client App-Id"
                },
                status=400
            )
        self.readings_config = config.get_config(self.client.code)
        try:
            self.supply_point = self.readings_config.get_supply_point(
                kwargs["supply_point_identifier"]
            )
        except django_models.ObjectDoesNotExist:
            return http.JsonResponse(
                {
                    'status': False,
                    'error': 'Not a valid Supply Point!'
                },
                status=400
            )

    def get(self, request, *args, **kwargs) -> http.HttpResponse:
        res = self.prerequisites(request, *args, **kwargs)
        if res:
            return res

        if from_dt := request.GET.get("from_dt"):
            from_dt = dateparse.parse_datetime(from_dt)
        else:
            from_dt = None
        if to_dt := request.GET.get("to_dt"):
            to_dt = dateparse.parse_datetime(to_dt)
        else:
            to_dt = None

        readings = self.readings_config.get_readings(
            supply_point=self.supply_point,
            from_dt=from_dt,
            to_dt=to_dt,
        )
        return http.JsonResponse(
            {'status': True, 'data': readings},
            safe=False
        )
