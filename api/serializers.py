from rest_framework import serializers
from api.models import User, FarmerProfile, Farm, Case\
    #, CaseImg


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'fullname', 'password', 'password2', 'division', 'is_farmer']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self, **kwargs):
        account = User(
            username=self.validated_data['username'],
            fullname=self.validated_data['fullname'],
            division=self.validated_data['division'],
            is_farmer=self.validated_data['is_farmer']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Kata laluan mesti sama.'})
        account.set_password(password)
        account.save()
        return account


class AccountPropertiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'username', 'division', 'fullname', 'is_farmer']


# FARMER
class FarmerProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = FarmerProfile
        fields = ['contact_number', 'address']


class FullFarmerProfileSerializer(serializers.ModelSerializer):
    user = AccountPropertiesSerializer(required=True)

    class Meta:
        model = FarmerProfile
        fields = ['user', 'contact_number', 'address']


class FarmSerializer(serializers.ModelSerializer):
    #username = serializers.SerializerMethodField('get_username_from_user')

    class Meta:
        model = Farm
        fields = ['pk', 'farm_gps', 'farm_condition', 'farm_area', 'variety', 'vine_number', 'farm_age']

    #def get_username_from_user(self, api):
    #    username = api.user.username
    #    return username


class CaseSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.SerializerMethodField('get_username_from_farmer')

    class Meta:
        model = Case
        fields = ['pk', 'username', 'case_gps', 'vine_no', 'vine_age', 'case_start_date', 'case_subject', 'case_descriptions', 'vine_part', 'image', 'case_reported_datetime', 'case_status']


    def get_case_subject_from_case(self, case):
        case_subject = case.case_subject
        return case_subject


    def get_username_from_farmer(self, case):
        username = case.farmer.username
        return username

    #def create(self, validated_data):
    #    username = validated_data.farmer.username
    #    images_data = self.context.get('view').request.FILES
    #    case = Case.objects.create(case_subject=validated_data.get('case_subject', 'no-case_subject'),
    #                               username=username)
    #    for image_data in images_data.values():
    #        CaseImg.objects.create(case=case, image=image_data)

class CaseListSerializer(serializers.ModelSerializer):
    # farmer = serializers.SerializerMethodField('farmer_username')

    class Meta:
        model = Case
        fields = ['pk', 'farmer', 'case_gps', 'vine_no', 'vine_age', 'case_start_date', 'case_subject', 'case_descriptions', 'image', 'case_reported_datetime', 'case_status']
        # fields = ['pk', 'farmer', 'case_gps', 'vine_no', 'vine_age', 'case_start_date', 'case_subject', 'case_descriptions', 'image', 'case_reported_datetime', 'case_status', 'filterdate', 'filterstatus']

'''
class CaseImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseImg
        fields = ['case_subject', 'image']'''