from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import UserAccount
from .serializers import UserCreateSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserById(request, pk):
    user = UserAccount.objects.get(id=pk)
    serializer = UserCreateSerializer(user, many=False)
    return Response(serializer.data)
