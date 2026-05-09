from app_service_object.models import ServiceObject
from app_service_object.serializers import ServiceObjectSerializer
from utils.viewset import CustomModelViewSet

class ServiceObjectViewSet(CustomModelViewSet):
    queryset = ServiceObject.objects.select_related('nurse_dept','nurse').all()
    serializer_class = ServiceObjectSerializer
    filterset_fields = ['service_status', 'nurse_dept', 'nurse', 'object_gender']
    search_fields = ['object_name', 'object_phone', 'id_card']
    ordering = ['-create_datetime']