from app_nurse.models import Nurse
from app_nurse.serializers import NurseSerializer
from utils.viewset import CustomModelViewSet

class NurseViewSet(CustomModelViewSet):
    queryset = Nurse.objects.select_related('nurse_dept').all()
    serializer_class = NurseSerializer
    filterset_fields = ['nurse_status','nurse_dept','nurse_role','nurse_phone']
    search_fields = ['nurse_name','nurse_code','nurse_phone','nurse_role']
    ordering = ['-create_datetime']