from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from apps.common.permissions import IsMerchant
from apps.common.views import LoggedAPIView

from .services import recognize_product


class RecognizeView(LoggedAPIView):
    permission_classes = [IsMerchant]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        image = request.data.get("image")
        if image is None:
            return Response({"detail": "未上传图片"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(recognize_product(image), status=status.HTTP_200_OK)
