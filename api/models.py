import datetime

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.utils.text import slugify
# from django.contrib.gis.db import models as gismodels
# from django.contrib.gis.geos import Point
from multiselectfield import MultiSelectField
from pytz import unicode
from rest_framework.authtoken.models import Token



# USER
class User(AbstractUser):

    KUCHING = "KCH"
    SAMARAHAN = "SMH"
    SERIAN = "SER"
    SRIAMAN = "SAM"
    BETONG = "BTG"
    SARIKEI = "SKI"
    SIBU = "SBU"
    MUKAH = "MKH"
    BINTULU = "BIN"
    KAPIT = "KPT"
    MIRI = "MRI"
    LIMBANG = "LBG"

    DIVISION_CHOICES = [(KUCHING, "KUCHING"),
                        (SAMARAHAN, "KOTA SAMARAHAN"),
                        (SERIAN, "SERIAN"),
                        (SRIAMAN, "SRI AMAN"),
                        (BETONG, "BETONG"),
                        (SARIKEI, "SARIKEI"),
                        (SIBU, "SIBU"),
                        (MUKAH, "MUKAH"),
                        (BINTULU, "BINTULU"),
                        (KAPIT, "KAPIT"),
                        (MIRI, "MIRI"),
                        (LIMBANG, "LIMBANG")]

    division = models.CharField(max_length=3, choices=DIVISION_CHOICES, null=True, blank=True)
    fullname = models.CharField(max_length=50, blank=True)
    is_farmer = models.BooleanField(default=False)  # to indicate the user is a farmer


# STAFF
class OfficeLocation(models.Model):
    contact_number = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=100, blank=True)


class StaffProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True,
                                related_name='staff_profile')  # just deactivate the staff, don't delete its profile
    div_office = models.ForeignKey(OfficeLocation, on_delete=models.DO_NOTHING,
                                   null=True)  # just set the user account as non-active, do not delete the data.

    # username = models.CharField(max_length=20, blank=True)
    # account_status = models.TextField(max_length=20, choices=[('active', 'Aktif'), ('inactive', 'Tidak aktif')],
    #                                  blank=True)

    def __int__(self):
        return self


# FARMER
class FarmerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True,
                                related_name='farmer_profile')
    contact_number = models.CharField(max_length=100)
    address = models.TextField(max_length=20, blank=True)
    slug = models.SlugField(blank=True, unique=True)

    def __int__(self):
        return self.user


# when a user is created, the profile for each user category is to be created as well
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if instance.is_farmer:
        FarmerProfile.objects.get_or_create(user=instance)
    else:
        StaffProfile.objects.get_or_create(user=instance)

@receiver(post_save, sender=FarmerProfile)
def pre_save_farmer_receiver(sender, instance, *args, **kwargs): #renamed pre_save_case_receiver to pre_save_farmer_receiver
    if not instance.slug:
        instance.slug = slugify(instance.user.username)


pre_save.connect(pre_save_farmer_receiver, sender=FarmerProfile) #renamed pre_save_case_receiver to pre_save_farmer_receiver


# USER AUTHENTICATION - generate token for authentication
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# FARM
class Farm(models.Model):

    # farm condition
    BUKIT = "B"
    RATA = "R"
    LAIN = "L"
    FARM_CONDITION_CHOICES = [(BUKIT, "BERBUKIT"),
                              (RATA, "RATA"),
                              (LAIN, "LAIN-LAIN")]

    # farm area
    FARM_AREA_CHOICES = [("H1", "Kurang daripada 1 hektar"),
                         ("H2", "1–20 hektar"),
                         ("H3", "21–40 hektar"),
                         ("H4", "41–60 hektar"),
                         ("H5", "61–80 hektar"),
                         ("H6", "81–100 hektar"),
                         ("H7", "Lebih daripada 100 hektar")]

    # pepper variety
    SEMENGGOK_AMAN = "SA"
    KUCHING = "KC"
    SEMENGGOK_EMAS = "SE"
    SEMENGGOK_PERAK = "SP"
    INDIA = "ID"
    LAIN_LAIN = "LL"
    VARIETY_CHOICES = [(SEMENGGOK_AMAN, "Semonggok Aman"),
                       (SEMENGGOK_EMAS, "Semonggok Emas"),
                       (SEMENGGOK_PERAK, "Semonggok Perak"),
                       (KUCHING, "Kuching"),
                       (INDIA, "India"),
                       (LAIN_LAIN, "Lain-lain")]

    # number of pepper vines
    VINE_NO_CHOICES = [("VN1", "100 atau kurang"),
                       ("VN2", "101–300"),
                       ("VN3", "301–500"),
                       ("VN4", "501–700"),
                       ("VN5", "701–900"),
                       ("VN6", "901–1100"),
                       ("VN7", "1101–1300"),
                       ("VN8", "1301–1500"),
                       ("VN9", "1501–1700"),
                       ("VN10", "1701–1900"),
                       ("VN11", "1901–2100"),
                       ("VN12", "2101–2300"),
                       ("VN13", "2301–2500"),
                       ("VN14", "2501–2700"),
                       ("VN15", "2701–2900"),
                       ("VN16", "2901–3100"),
                       ("VN17", "3101–3300"),
                       ("VN18", "3301–3500"),
                       ("VN19", "3501–3700"),
                       ("VN20", "3701–3900"),
                       ("VN21", "3901–4000"),
                       ("VN22", "Lebih daripada 4000")]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True,
                                related_name='farmer_farm')  # do not delete the farm data, might be useful
    # gpspoint = models.PointField(null=True, default=0)  #the point field is pre-computed in form before submission
    # farm_id = models.CharField(primary_key=True, max_length=5)
    farm_gps = models.CharField(max_length=30, null=True, blank=True)  # temporary field before fully configuring pointField
    farm_condition = models.CharField(max_length=6, choices=FARM_CONDITION_CHOICES, null=True, blank=True)
    farm_area = models.CharField(max_length=2, choices=FARM_AREA_CHOICES, null=True, blank=True)
    # variety = MultiSelectField(choices=VARIETY_CHOICES, max_length=20) #require django-multiselectfield package to be installed
    variety = models.CharField(max_length=30, null=True, blank=True)
    vine_number = models.CharField(max_length=5, choices=VINE_NO_CHOICES, null=True, blank=True)
    farm_age = models.CharField(max_length=20, blank=True)
    slug = models.SlugField(blank=True) # to point to specific farm

    def __int__(self):
        return self


def pre_save_farm_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.user.username + "_farm")


pre_save.connect(pre_save_farm_receiver, sender=Farm)


# CASE
# to store uploaded image
def upload_location(instance, filename, **kwargs):
    file_path = 'cases/{farmer_id}/{case_subject}-{filename}'.format(
        farmer_id=str(instance.farmer.id), case_subject=str(instance.case_subject), filename=filename)
    return file_path


class Case(models.Model):

    # affected vine part
    VINE_PART_CHOICES = [("daun", "DAUN"),
                         ("buah", "BUAH"),
                         ("batang", "BATANG"),
                         ("dahan", "DAHAN/RANTING"),
                         ("pucuk", "PUCUK"),
                         ("tangkai", "TANGKAI BUNGA/BUAH"),
                         ("akar", "AKAR")]


    farmer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    case_gps = models.CharField(max_length=30, null=True, blank=True) # temporarily using CharField to store latitude & longitude before changing to PointField
    vine_no = models.CharField(max_length=20, blank=True) # should be for affected number of vines
    vine_age = models.CharField(max_length=20, blank=True) # average age of the vines with disease
    case_start_date = models.DateField(auto_now_add=False)
    case_subject = models.CharField(max_length=200, blank=True)
    case_descriptions = models.CharField(max_length=200, blank=True)
    vine_part = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True) # not finalised yet, trying to create a separate case image class to store multiple images per case
    case_reported_datetime = models.DateTimeField(auto_now=True, null=True) # will autogenerate date time once the case is submitted
    case_status = models.CharField(max_length=20,
                                   choices=[('open', 'Buka'), ('processing', 'Sedang diproses'), ('closed', 'Tutup')],
                                   blank=True)
    slug = models.SlugField(blank=True, unique=True)

    def __int__(self):
        return self.case_subject


@receiver(post_delete, sender=Case)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)
'''
def pre_save_case_receiver(self, *args, **kwargs):
    self.slug = slugify(unicode('%s'% (self.farmer.username + "_" + self.case_subject)))
    super(Case, self).save(*args, **kwargs)
    '''


def pre_save_case_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.farmer.username + "-" + instance.case_subject)


pre_save.connect(pre_save_case_receiver, sender=Case)
'''
class CaseImg(models.Model):
    case_subject = models.ForeignKey(Case, on_delete=models.CASCADE, null=True)
    image = models.ImageField(null=True, blank=True)
'''
