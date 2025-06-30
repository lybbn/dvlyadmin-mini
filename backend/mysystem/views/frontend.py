from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from utils.file_upload import ImageUpload
from utils.jsonResponse import SuccessResponse,DetailResponse,ErrorResponse

#后端图片上传
class SysImagesUploadView(APIView):
    '''
    post:
    【功能描述】图片上传功能API</br>
    【参数说明】无，需要登录携带token后才能调用</br>
    '''
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        result = ImageUpload(request,"file", "platform")
        if result['code'] == 200:
            return SuccessResponse(data=result['img'], msg=result['msg'])
        else:
            return ErrorResponse(msg=result['msg'])

#h5端页面
def h5web(request):
    return render(request,"h5/index.html")