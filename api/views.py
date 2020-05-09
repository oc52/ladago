# Create your views here.
from PIL import Image
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.helpers import modify_input_for_multiple_files
from api.models import User, FarmerProfile, Farm, Case
from api.serializers import RegistrationSerializer, AccountPropertiesSerializer, FarmerProfileSerializer, \
    FarmSerializer, CaseSerializer, CaseListSerializer, FullFarmerProfileSerializer\
    #, CaseImgSerializer


@api_view(['POST',])
@permission_classes((AllowAny,))
def register(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = "Berjaya mendaftar pengguna baharu"
            data['username'] = account.username
            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)


# USER
# view user info
@api_view(['GET',])
@permission_classes((IsAuthenticated, ))
def user_detail(request):
    try:
        account = request.user
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AccountPropertiesSerializer(account)
        return Response(serializer.data)


# user profile update - NOT USED AT THE MOMENT
@api_view(['PUT',])
@permission_classes((IsAuthenticated, ))
def user_update(request):
    try:
        account = request.user
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = AccountPropertiesSerializer(account, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = "Berjaya kemas kini akaun"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# FARMER PROFILE
@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
@csrf_exempt
def farmer_create(request):
    user = request.user

    farmer_profile = FarmerProfile(user=user)

    if request.method == 'POST':
        serializer = FarmerProfileSerializer(farmer_profile, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def farmer_detail(request, slug):
    try:
        farmer_profile = FarmerProfile.objects.get(slug=slug)
    except FarmerProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = FarmerProfileSerializer(farmer_profile)
        return Response(serializer.data)


@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
def farmer_update(request, slug):
    try:
        farmer_profile = FarmerProfile.objects.get(slug=slug)
    except FarmerProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if farmer_profile.user != user:
        return Response({'response':"Anda tidak dibenarkan untuk edit ini."})

    if request.method == 'PUT':
        serializer = FarmerProfileSerializer(farmer_profile, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data["success"]="berjaya kemas kini"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAuthenticated, ))
class full_profile(APIView):
    """
    A class based view for creating and fetching student records
    """
    def get(self, format=None):
        """
        Get all the student records
        :param format: Format of the student records to return to
        :return: Returns a list of student records
        """
        user = self.request.user
        farmer_profile = FarmerProfile.objects.filter(user=user)
        serializer = FullFarmerProfileSerializer(farmer_profile, many=True)
        return Response(serializer.data)


# FARM
@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def farm_create(request):
    user = request.user

    farm = Farm(user=user)

    if request.method == 'POST':
        serializer = FarmSerializer(farm, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def farm_detail(request, slug):
    try:
        farm = Farm.objects.get(slug=slug)
    except Farm.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = FarmSerializer(farm)
        return Response(serializer.data)


@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
def farm_update(request, slug):
    try:
        farm = Farm.objects.get(slug=slug)
    except Farm.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if farm.user != user:
        return Response({'response':"Anda tidak dibenarkan untuk edit ini."})

    if request.method == 'PUT':
        serializer = FarmSerializer(farm, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data["success"]="berjaya kemas kini"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# CASE
@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def case_create(request):
    account = request.user

    case = Case(farmer=account)

    if request.method == 'POST':
        serializer = CaseSerializer(case, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAuthenticated,))
class case_list(ListAPIView):
    serializer_class = CaseListSerializer

    def get_queryset(self):
        """
        This view should return a list of all the cases
        for the currently authenticated user.
        """
        user = self.request.user
        queryset = Case.objects.filter(farmer=user).order_by('-case_reported_datetime')
        return queryset


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def case_detail(request, slug):
    try:
        case = Case.objects.get(slug=slug)
    except Case.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CaseSerializer(case)
        return Response(serializer.data)


@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
def case_update(request, slug):
    try:
        case = Case.objects.get(slug=slug)
    except Case.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if case.farmer != user:
        return Response({'response':"Anda tidak dibenarkan untuk edit ini."})

    if request.method == 'PUT':
        serializer = CaseSerializer(case, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data["success"]="berjaya kemas kini"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def case_delete(request, slug):
    try:
        case = Case.objects.get(slug=slug)
    except Case.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if case.farmer != user:
        return Response({'response':"Anda tidak dibenarkan untuk memadam ini."})

    if request.method == 'DELETE':
        operation = case.delete()
        data = {}
        if operation:
            data["success"]="berjaya dipadamkan"
        else:
            data["failure"]="gagal dipadamkan"
        return Response(data=data)

'''
@permission_classes((IsAuthenticated,))
class ImageView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        all_images = Image.objects.all()
        serializer = CaseImgSerializer(all_images, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, *args, **kwargs):
        case_subject = request.data['case_subject']

        # converts querydict to original dict
        images = dict((request.data).lists())['image']
        flag = 1
        arr = []
        for img_name in images:
            modified_data = modify_input_for_multiple_files(case_subject,
                                                            img_name)
            file_serializer = CaseImgSerializer(data=modified_data)
            if file_serializer.is_valid():
                file_serializer.save()
                arr.append(file_serializer.data)
            else:
                flag = 0

        if flag == 1:
            return Response(arr, status=status.HTTP_201_CREATED)
        else:
            return Response(arr, status=status.HTTP_400_BAD_REQUEST)'''