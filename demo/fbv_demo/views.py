from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Medical
from rest_framework import status

from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from demo.cbv_demo.serializers import ContactDataSerializer

@api_view(['POST'])
def save_medical(request):
    """
    保存数据
    ---

    成功返回示例:
    -----------

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
    name = request.POST.get('name')
    bloodgroup = request.POST.get('bloodgroup')
    birthmark = request.POST.get('birthmark')

    try:
        Medical.objects.create(name= name, bloodgroup = bloodgroup, birthmark = birthmark)
        return Response("Data Saved!", status=status.HTTP_201_CREATED)

    except Exception as ex:
        return Response(ex, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_medical(request):
    """
    取得数据
    -------

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
    return Response(Medical.objects.all().values(), status=status.HTTP_200_OK)


from rest_framework import serializers
class DemoDataSerializer(serializers.ModelSerializer):
    pass
    
class DemoViewSet(viewsets.GenericViewSet):
    serializer_class = DemoDataSerializer
    queryset = Medical.objects.all()

    @list_route(methods=['GET'])
    def get_demo(self, request):
        """
        get测试demo:
        ------------
        成功返回数据:
        ------------
            {
    
            }

        code -- test code input
        """
        return Response('ok')


