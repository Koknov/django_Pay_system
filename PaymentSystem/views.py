# Create your views here.
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, views, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .renderers import UserJSONRenderer
from .models import Users, Transaction
from .serializer import UsersSerializer, TransactionSerializer, RegistrationSerializer


class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = UsersSerializer
    queryset = Users.objects.all()


class TransactionsViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()


class UsersView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        messages = Users.objects.all()
        serializer = UsersSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=UsersSerializer)
    def post(self, request):
        serializer = UsersSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            message_saved = serializer.save()
            return Response({"success": "User added {}".format(message_saved.username)})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionsView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, wallet_number):
        """
        Get user instance using unique wallet number

        :param wallet_number:
        :return: User object or raise HTTP_400_BAD_REQUEST
        """
        try:
            return Users.objects.get(wallet_number=wallet_number)
        except(Users.DoesNotExist, ValidationError, TypeError):
            raise status.HTTP_400_BAD_REQUEST

    def validate_users(self, wallets):
        """
        Validate users' wallets that participate in transaction

        :param wallets: list wallet ids of sender and receiver
        :return: None or error response HTTP_422_UNPROCESSABLE_ENTITY
        """
        for w in wallets:
            try:
                Users.objects.get(wallet_number=w)
            except(Users.DoesNotExist, ValidationError, TypeError):
                response_msg = {'Error:': "Wallet number <{}> doesn't exist".format(
                    w)}
                return Response(response_msg, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def get(self, request):
        messages = Transaction.objects.all()
        serializer = TransactionSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=TransactionSerializer)
    def post(self, request):
        sender_wallet_num = request.data['sender_wallet_number']
        receiver_wallet_num = request.data['receiver_wallet_number']

        response = self.validate_users([sender_wallet_num, receiver_wallet_num])
        if response:
            return response

        sender = self.get_object(sender_wallet_num)
        receiver = self.get_object(receiver_wallet_num)

        if request.data['transaction_amount'] < 0:
            response_msg = {'Error:': "Transaction amount should be a positive number, not {}".format(
                request.data['transaction_amount'])}
            return Response(response_msg, status=status.HTTP_406_NOT_ACCEPTABLE)
        elif request.data['transaction_amount'] > sender.total:
            response_msg = {'Error:': "You've got not enough money on your account: {}".format(
                sender.total)}
            return Response(response_msg, status=status.HTTP_406_NOT_ACCEPTABLE)

        # update users total info
        sender.total = sender.total - request.data['transaction_amount']
        receiver.total = receiver.total + request.data['transaction_amount']

        # save instances
        sender.save()
        receiver.save()

        # add transaction to db
        transaction_serializer = TransactionSerializer(data=request.data)
        if transaction_serializer.is_valid(raise_exception=False):
            transaction_serializer.save()
            response = {"Success": "You've got a completed transaction!!!! Your total: {}".format(
                Users.objects.get(wallet_number=request.data['sender_wallet_number']).total)}
            return Response(response, status=status.HTTP_202_ACCEPTED)
        return Response(transaction_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    @swagger_auto_schema(request_body=RegistrationSerializer)
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

