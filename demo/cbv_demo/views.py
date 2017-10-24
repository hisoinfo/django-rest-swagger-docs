from demo.cbv_demo.serializers import ContactDataSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Contact
from rest_framework import status , generics
from rest_framework.decorators import api_view

from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route


class ContactData(viewsets.GenericViewSet):
    serializer_class = ContactDataSerializer
    # permission_classes = [IsAuthenticated,]
    queryset = Contact.objects.all()

    @list_route(methods=['get'])
    def get_test(self, request, pk=None):
        """
        返回
        --------------------

        成功返回示例:
        --------------------

            [
              
            ]

        错误返回:
        ------------

            =======================  ===========================
                error_key                   response
            =======================  ===========================
                code_invalid               代码输入有误
            =======================  ===========================

        code -- 代码
        """
        print(request.user)
        print(request.data)
        contacts = Contact.objects.all()
        serializer = ContactDataSerializer(contacts, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        '''
        返回
        --------------------

        成功返回示例:
        --------------------

            [
              
            ]

        错误返回:
        ------------

            =======================  ===========================
                error_key                   response
            =======================  ===========================
                code_invalid               代码输入有误
            =======================  ===========================

        code -- 代码
        '''
        return Response('ok')

    @list_route(methods=['post'])
    def hello(self, request, format=None):
        """
        返回
        --------------------

        成功返回示例:
        --------------------

            [
             
            ]

        错误返回:
        ------------

            =======================  ===========================
                error_key                   response
            =======================  ===========================
                code_invalid              代码输入有误
            =======================  ===========================

        code -- 代码
        test -- 测试位
        """
        serializer = ContactDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)