from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def get_data(request):
    data = {"message": "stuju ga prpl asing kronus"}
    return Response(data)

@api_view(['POST'])
def save_user(request):
    nama = request.data.get('nama')
    return Response({"status": "ok", "nama": nama})
