from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from .models import postimage
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser
from .serializers import PostSerializer
from rest_framework.views import APIView
from rest_framework import status
from django.http import HttpResponse
import io
from PIL import Image
# Create your views here.

class PostView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def get(self, request, *args, **kwargs):
        posts =  postimage.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        posts_serializer = PostSerializer(data=request.data)
        if posts_serializer.is_valid():
            posts_serializer.save()
            return Response(posts_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('error', posts_serializer.errors)
            return Response(posts_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['post', 'GET'])
def postImage(request):
    parser_classes = (MultiPartParser, FormParser)
    if request.method == 'POST':
        # posts_serializer = PostSerializer(data=request.data)
        user_img = request.data.get('img')
        user_id = request.data.get('user_id')
        user = postimage(user_id=user_id, img=user_img)
        return Response({'test':"123"})
    return Response("error")
@api_view(['post', 'GET'])
def getprofileimage(request):
    if request.method == 'POST':
        received_json_data=json.loads(request.body)
        my_uuid = received_json_data['uuid']
        my_id = received_json_data['user_id']
        Number_of_images_uploaded = postimage.objects.filter(user_id=my_id).count()
        if Number_of_images_uploaded != 0:
            Latest_image = postimage.objects.filter(user_id=my_id)[Number_of_images_uploaded - 1]
            myFileID = Latest_image.img._id
            img_data = Latest_image.img.read()   
            roiImg = Image.open(io.BytesIO(img_data)) # Image開啟二進位制流Byte位元組流資料
            imgByteArr = io.BytesIO()  # 建立一個空的Bytes物件
            roiImg.save(imgByteArr, format='PNG')  # PNG就是圖片格式，我試過換成JPG/jpg都不行
            imgByteArr = imgByteArr.getvalue()  # 這個就是儲存的二進位制流
            # with open("./postimage/Media/tmp.png", "wb") as f:
                # f.write(imgByteArr)
            # print(imgByteArr)
        return HttpResponse(imgByteArr, content_type="image/png")
    return Response("error")
