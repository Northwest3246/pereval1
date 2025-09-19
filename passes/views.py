from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .models import Pass
from .serializers import PassSerializer

@api_view(['POST'])
def submit_data(request):
    serializer = PassSerializer(data=request.data)
    if serializer.is_valid():
        try:
            pas = serializer.save()
            return Response({
                "status": 200,
                "message": None,
                "id": pas.id
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": 500,
                "message": f"Ошибка сохранения: {str(e)}",
                "id": None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({
            "status": 400,
            "message": "Ошибка валидации данных",
            "errors": serializer.errors,
            "id": None
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_pass(request, pk):
    try:
        pas = Pass.objects.get(pk=pk)
        serializer = PassSerializer(pas)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Pass.DoesNotExist:
        return Response({
            "status": 404,
            "message": "Запись не найдена",
            "id": None
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['PATCH'])
def edit_pass(request, pk):
    try:
        pas = Pass.objects.get(pk=pk)
    except Pass.DoesNotExist:
        return Response({
            "state": 0,
            "message": "Запись не найдена"
        }, status=status.HTTP_404_NOT_FOUND)

    if pas.status != 'new':
        return Response({
            "state": 0,
            "message": "Редактирование запрещено: статус не 'new'"
        }, status=status.HTTP_400_BAD_REQUEST)

    serializer = PassSerializer(pas, data=request.data, partial=True)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response({
                "state": 1,
                "message": "Успешно обновлено"
            }, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({
                "state": 0,
                "message": str(e.detail[0]) if isinstance(e.detail, list) else str(e.detail)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "state": 0,
                "message": f"Ошибка сервера: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({
            "state": 0,
            "message": "Ошибка валидации",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_passes_by_user(request):
    email = request.GET.get('user__email')
    if not email:
        return Response({
            "status": 400,
            "message": "Параметр user__email обязателен",
            "data": []
        }, status=status.HTTP_400_BAD_REQUEST)

    passes = Pass.objects.filter(user__email=email)
    serializer = PassSerializer(passes, many=True)
    return Response({
        "status": 200,
        "message": None,
        "data": serializer.data
    }, status=status.HTTP_200_OK)


