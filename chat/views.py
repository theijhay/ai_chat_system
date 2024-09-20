from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Chat
from .serializers import UserRegistrationSerializer
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from django.http import HttpResponse
from rest_framework.permissions import AllowAny
import openai
from django.conf import settings


def home(request):
    return HttpResponse("<h1>Welcome to the AI Chat System API!</h1><p>Go to <a href='/api/docs/'>API Docs</a></p>")

"""User Registration View"""
class UserRegistrationView(APIView):
    """Override permission classes for this view to allow public access"""
    permission_classes = [AllowAny]
    
    @extend_schema(
        description="Register a new user.",
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string', 'description': 'Desired username'},
                    'password': {'type': 'string', 'description': 'Desired password'},
                },
                'required': ['username', 'password'],
            }
        },
        responses={
            201: {
                'description': 'User registered successfully.',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'message': {'type': 'string', 'description': 'Registration success message'},
                            },
                        }
                    }
                }
            },
        }
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""Chat API View"""
class ChatView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        description="Send a message to the model.",
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'description': 'Message to the chatbot'},
                },
                'required': ['message'],
            }
        },
        responses={
            200: {
                'description': 'Success',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'message': {'type': 'string', 'description': 'User message'},
                                'response': {'type': 'string', 'description': 'Response from the AI'},
                                'remaining_tokens': {'type': 'integer', 'description': 'Remaining tokens'},
                            },
                        }
                    }
                }
            },
        }
    )
    def post(self, request):
        message = request.data.get('message')
        if not message:
            return Response({'error': 'Message is required'}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        
        """Check if the user has enough tokens"""
        if user.tokens < 100:
            return Response({'error': 'Insufficient tokens'}, status=status.HTTP_403_FORBIDDEN)

        """Deduct 100 tokens"""
        user.tokens -= 100
        user.save()

        """Generate AI response (hardcoded for now)"""
        ai_response = "This is a dummy response."

        """Save chat to the databasetokens_to_add = request.data.get('tokens', 0)"""
        chat = Chat.objects.create(user=user, message=message, response=ai_response, timestamp=timezone.now())
        
        return Response({
            'message': message,
            'response': ai_response,
            'remaining_tokens': user.tokens
        }, status=status.HTTP_200_OK)

"""Token Balance API View"""
class TokenBalanceView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        description="Check the user's remaining token balance.",
        responses={
            200: {
                'description': 'Token balance retrieved successfully.',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'tokens': {'type': 'integer', 'description': 'Remaining number of tokens'},
                            },
                        }
                    }
                }
            }
        }
    )
    def get(self, request):
        user = request.user
        return Response({'tokens': user.tokens}, status=status.HTTP_200_OK)

class TokenTopUpView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description="Top-up tokens to your account.",
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'tokens': {'type': 'integer', 'description': 'Number of tokens to add to the user account'},
                },
                'required': ['tokens'],
            }
        },
        responses={
            200: {
                'description': 'Tokens successfully added to user account.',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'message': {'type': 'string', 'description': 'Success message'},
                                'total_tokens': {'type': 'integer', 'description': 'Updated token balance'},
                            },
                        }
                    }
                }
            },
            400: {'description': 'Invalid token amount'},
        }
    )
    def post(self, request):
        user = request.user
        tokens_to_add = request.data.get('tokens', 0)

        if tokens_to_add <= 0:
            return Response({'error': 'Invalid token amount.'}, status=status.HTTP_400_BAD_REQUEST)

        user.tokens += tokens_to_add
        user.save()

        return Response({
            'message': f'Successfully added {tokens_to_add} tokens.',
            'total_tokens': user.tokens
        }, status=status.HTTP_200_OK)
