from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from api import views

app_name = "api"

urlpatterns = [
    # REGISTRATION
    path('register/', views.register, name="register"),

    # LOGIN
    path('login/', obtain_auth_token, name="login"), # view name cannot be changed as it is django rest framework default login view (for token authentication)

    # USER INFO (USERNAME, FULLNAME, DIVISION, IS_FARMER...)
    path('user/detail/', views.user_detail, name="user_detail"),

    # path('user/update/', views.user_update, name="update"), # NOT USED AT THE MOMENT

    # FARMER PROFILE (CONTACT NUMBER, ADDRESS)
    # add farmer's contact number and address
    path('farmer/create', views.farmer_create, name='farmer_create'),
    # view farmer profile
    path('farmer/detail/<slug>/', views.farmer_detail, name='farmer_detail'),
    #update farmer profile
    path('farmer/update/<slug>/', views.farmer_update, name='farmer_update'),

    # FULL FARMER PROFILE (COMBINE USER & FARMER PROFILE)
    # path('farmer/full_profile/', views.full_profile.as_view()), # REDUNDANT, NOT USED AT THE MOMENT

    # FARM
    # add farmer's farm details
    path('farm/create', views.farm_create, name='farm_create'),
    # view farm details
    path('farm/detail/<slug>/', views.farm_detail, name='farm_detail'),
    # update farm details<slug>/
    path('farm/update/<slug>/', views.farm_update, name='farm_update'),

    # CASE
    # submit case
    path('case/create', views.case_create, name='case_create'),
    # view list of submitted cases
    path('case/list/', views.case_list.as_view(), name='case_list'),
    # view details of submitted cases
    path('case/detail/<slug>/', views.case_detail, name='case_detail'),
    # update submitted case
    path('case/update/<slug>/', views.case_update, name='case_update'),
    # delete case (not used, but retained for future possible use)
    # path('case/delete/<slug>/', views.case_delete, name='delete'),

#    path('case/upload_image', views.ImageView.as_view(), name='upload image')
]