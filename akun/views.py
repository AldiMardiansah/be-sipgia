# akun/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from .models import Akun
from .serializers import RegisterSerializer, LoginSerializer, AkunSerializer
import traceback

class RegisterView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []  # Disable authentication for register

    def post(self, request):
        try:
            print("📝 Registration attempt:", request.data)
            
            serializer = RegisterSerializer(data=request.data)
            if not serializer.is_valid():
                print("❌ Validation errors:", serializer.errors)
                return Response({
                    'error': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            akun = serializer.save()
            print(f"✅ Account created: {akun.username}")
            
            # Generate JWT token
            refresh = RefreshToken()
            refresh['user_id'] = str(akun.id)
            refresh['username'] = akun.username
            
            response_data = {
                'akun': AkunSerializer(akun).data,
                'token': str(refresh.access_token),
                'refresh': str(refresh),
                'message': 'Registration successful'
            }
            
            print("✅ Registration successful for:", akun.username)
            return Response(response_data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            print(f"❌ Registration error: {str(e)}")
            print(traceback.format_exc())
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []  # Disable authentication for login

    def post(self, request):
        try:
            print("🔐 Login attempt:", request.data.get('username'))
            
            serializer = LoginSerializer(data=request.data)
            if not serializer.is_valid():
                print("❌ Login validation errors:", serializer.errors)
                return Response({
                    'error': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            akun = serializer.validated_data['akun']
            
            # Generate JWT token
            refresh = RefreshToken()
            refresh['user_id'] = str(akun.id)
            refresh['username'] = akun.username
            
            response_data = {
                'akun': AkunSerializer(akun).data,
                'token': str(refresh.access_token),
                'refresh': str(refresh),
                'message': 'Login successful'
            }
            
            print(f"✅ Login successful: {akun.username}")
            return Response(response_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"❌ Login error: {str(e)}")
            print(traceback.format_exc())
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            return Response({
                'message': 'Logout successful'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"⚠️ Logout error: {str(e)}")
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class AkunListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            akun_list = Akun.objects.filter(is_active=True)
            serializer = AkunSerializer(akun_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"❌ Error fetching accounts: {str(e)}")
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class CurrentAkunView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Get user_id from JWT token
            auth_header = request.headers.get('Authorization', '')
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                from rest_framework_simplejwt.tokens import AccessToken
                token_obj = AccessToken(token)
                user_id = token_obj['user_id']
                
                akun = Akun.objects.get(id=user_id)
                serializer = AkunSerializer(akun)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'No valid authentication token provided'
                }, status=status.HTTP_401_UNAUTHORIZED)
            
        except Akun.DoesNotExist:
            return Response({
                'error': 'Account not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class AkunDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            akun = Akun.objects.get(pk=pk)
            serializer = AkunSerializer(akun)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Akun.DoesNotExist:
            return Response({
                'error': 'Account not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)