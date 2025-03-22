from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

#For all conversation
class ConversationListView(APIView):
    def get(self, request):
        conversations = Conversation.objects.all()
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ConversationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class MessageListView(APIView):
    def post(self, request, conversation_id):
        try:
            conversation = Conversation.objects.get(pk=conversation_id)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation not found"}, status=status.HTTP_404_NOT_FOUND)


        request.data['conversation'] = conversation.id

        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    #Get all messages for a specific conversation
    def get(self, request, conversation_id):
        try:
            conversation = Conversation.objects.get(pk=conversation_id)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation not found"}, status=status.HTTP_404_NOT_FOUND)


        messages = conversation.messages.all() 
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, message_id):
            try:
                message = Message.objects.get(pk=message_id)
            except Message.DoesNotExist:
                return Response(
                    {"error": "Message not found"}, status=status.HTTP_404_NOT_FOUND)

            update = request.data.get('real_time_feedback')

            if not update:
                return Response(
                    {"error": "real_time_feedback field is required"}, status=status.HTTP_400_BAD_REQUEST)

            message.real_time_feedback = update
            message.save()
            return Response(status=status.HTTP_200_OK)