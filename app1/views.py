import re

from django.shortcuts import render

# Create your views here.
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import status
from rest_framework.exceptions import ParseError, ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from app1.models import Data1

mobile_validation = lambda mobile_number: bool(re.search(r"^[9876]\d{9}$", str(mobile_number)))


class CustomMessage(Exception):
    def __init__(self, message):
        self.message = message


class DataAPI(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        try:
            id1 = request.query_params.get("id")
            mobile = request.query_params.get("mobile")
            name = request.query_params.get("name")
            if id1:
                try:
                    d_obj = Data1.objects.get(id=id1)
                    return Response({"is_success": True, "data": {"id": d_obj.id, "name": d_obj.name,
                                                                  "mobile": d_obj.mobile}}, status=status.HTTP_200_OK)
                except Data1.DoesNotExist:
                    raise CustomMessage("Please provide valid id")
            elif mobile and name:
                if not mobile_validation(mobile):
                    raise CustomMessage("Enter valid Mobile number")

                d_obj = Data1.objects.create(name=name, mobile=mobile)
                return Response({"is_success": True, "data": {"id": d_obj.id, "name": d_obj.name,
                                                              "mobile": d_obj.mobile}}, status=status.HTTP_200_OK)
            else:
                raise CustomMessage("Please provide id or name & mobile")

        except CustomMessage as e:
            return Response({"is_success": False, "message": e.message},
                            status=status.HTTP_200_OK)
        except (ParseError, ZeroDivisionError, MultiValueDictKeyError, KeyError, ValueError, ValidationError):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "message": "fail", "raw_message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
