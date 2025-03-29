from drf_yasg.openapi import Schema
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from users.serializers.verification import EmailVerificationSerializer
from verification.models import VerificationToken


class EmailVerifyView(GenericAPIView):
    """
    Verify email using the token
    """

    serializer_class = EmailVerificationSerializer

    @swagger_auto_schema(
        responses={
            HTTP_200_OK: Schema(
                type="object", properties={"message": Schema(type="string", description="Success message")}
            ),
            HTTP_400_BAD_REQUEST: Schema(
                type="object", properties={"error": Schema(type="string", description="Error message")}
            ),
        }
    )
    def get(self, request, token: str):
        serializer = self.serializer_class(data={"token": token})
        serializer.is_valid(raise_exception=True)
        token_instance = VerificationToken.objects.filter(token=serializer.validated_data["token"]).first()

        if not token_instance:
            raise ValidationError({"error": "Token invalid or expired"})
        if token_instance.is_expired:
            raise ValidationError({"error": "Token expired"})

        token_instance.user.is_active = True
        token_instance.user.save()
        token_instance.delete()

        return Response({"message": "Email verified successfully"}, status=HTTP_200_OK)
