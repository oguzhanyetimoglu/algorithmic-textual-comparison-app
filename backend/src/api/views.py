from datetime import datetime
from django.http import Http404
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated

from .models import NAICSCode, SICCode, TenK, TenKFileUpload
from .serializers import NAICSCodeSerializer, SICCodeSerializer, TenKSerializer, TenKFileUploadSerializer, DynamicFieldsTenKSerializer
from rest_framework.response import Response
from django.db.models import Count


class SICCodeList(generics.ListCreateAPIView):
    queryset = SICCode.objects.all()
    serializer_class = SICCodeSerializer
    permission_classes = [IsAuthenticated]


class SICCodeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SICCode.objects.all()
    serializer_class = SICCodeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, sic_code):
        try:
            return self.get_queryset().get(sic_code=sic_code)
        except SICCode.DoesNotExist:
            raise Http404


class NAICSCodeList(generics.ListCreateAPIView):
    queryset = NAICSCode.objects.all()
    serializer_class = NAICSCodeSerializer
    permission_classes = [IsAuthenticated]


class NAICSCodeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = NAICSCode.objects.all()
    serializer_class = NAICSCodeSerializer

    permission_classes = [IsAuthenticated]

    def get_object(self, sic_code):
        try:
            return self.queryset().get(sic_code=sic_code)
        except NAICSCode.DoesNotExist:
            raise Http404


class TenKList(generics.ListCreateAPIView):
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'cik', 'trading_symbol', 'company', 'exchange', 'filing_type',
        'state_location'
    ]

    def get_queryset(self):
        queryset = TenK.objects.filter(is_active=True).order_by('-filing_date')
        sic_start = self.request.query_params.get('sic_start', None)
        year = self.request.query_params.get('year', None)
        state = self.request.query_params.get('state', None)
        filing_type = self.request.query_params.get('filing_type', None)

        if sic_start is not None:
            queryset = queryset.filter(sic__startswith=sic_start)
        if year is not None:
            start_date = datetime.strptime(f"{year}-01-01", "%Y-%m-%d")
            end_date = datetime.strptime(f"{year}-12-31", "%Y-%m-%d")
            queryset = queryset.filter(filing_date__range=(start_date, end_date))
        if state is not None:
            queryset = queryset.filter(state_location=state)
        if filing_type is not None:
            queryset = queryset.filter(filing_type=filing_type)
        return queryset

    def get_serializer_class(self):
        fields = self.request.query_params.get('fields')
        if fields:
            return lambda *args, **kwargs: DynamicFieldsTenKSerializer(
                *args, fields=fields.split(','), **kwargs)
        return TenKSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        count_only = request.query_params.get('count_only', 'false') == 'true'
        count_by_state = request.query_params.get('count_by_state', 'false') == 'true'
        count_by_filing_type = request.query_params.get('count_by_filing_type', 'false') == 'true'
        if count_only:
            count = self.get_queryset().count()
            return Response({'count': count})
        elif count_by_state:
            counts = self.get_queryset().values('state_location').annotate(count=Count('state_location')).order_by()
            return Response({item['state_location']: item['count'] for item in counts})
        elif count_by_filing_type:
            counts = self.get_queryset().values('filing_type').annotate(count=Count('filing_type')).order_by()
            return Response({item['filing_type']: item['count'] for item in counts})
        return super().list(request, *args, **kwargs)

class TenKDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TenK.objects.filter(is_active=True)
    serializer_class = TenKSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            cik = self.kwargs['cik']
            filing_date = self.kwargs['filing_date']
            return self.get_queryset().get(cik=cik, filing_date=filing_date)
        except TenK.DoesNotExist:
            raise Http404


class FileUploadView(generics.CreateAPIView):
    queryset = TenKFileUpload.objects.all()
    serializer_class = TenKFileUploadSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Generate timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Change the name of the uploaded file
        request.data['file'].name = f'tenk_import_{timestamp}.json'

        return super().create(request, *args, **kwargs)
