from rest_framework.decorators import api_view
from .serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

"""for jwt registration"""
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed


@api_view(["POST"])
def registration_view(request):
    if request.method == "POST":
        serializer = RegistrationSerializer(data=request.data)

        data = {}

        if serializer.is_valid():
            account = serializer.save()
            # print(serializer)
            data["response"] = "Registration Successful!"
            data["username"] = account.username
            data["email"] = account.email

            """Access token"""
            # token = Token.objects.get(user=account).key  # Returns Token
            # data["token"] = token

            """JWT Token"""  # utilize old url link ie path("register/", views.registration_view, name="register"),
            refresh = RefreshToken.for_user(account)
            data["token"] = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }

        else:
            data = serializer.errors  # this is dict too
            # return Response(serializer.data) # USERNAME AND EMAIL IS SENT CUZ PASSWORD IS WRITE ONLY
        return Response(data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def logout_view(request):
    if request.method == "POST":
        request.user.auth_token.delete()  # request.user is current logged in user
        return Response(status=status.HTTP_200_OK)


"""1st method to create a token """
# from django.contrib.auth.models import User
# from rest_framework.authtoken.models import Token

# for user in User.objects.all():
#     Token.objects.get_or_create(user=user)
