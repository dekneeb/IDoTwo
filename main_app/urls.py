from django.urls import path
from . import views


urlpatterns=[ 
    path('', views.Home.as_view(), name='home'),
    path('about/', views.About.as_view(), name='about'),
    path('items/new', views.ItemCreate.as_view(), name='item_create'),
    path('items/', views.ItemList.as_view(), name='items_list'),
    path('post/<int:pk>', views.PostDetail.as_view(), name='post_detail'),
    path('post/<int:pk>/update', views.PostUpdate.as_view(), name='post_update'),
    path('post/<int:pk>/', views.PostDelete.as_view(), name='post_delete'),
    path('accounts/signup', views.Signup.as_view(), name='signup'),
    path('post<int:pk>/add_photo/', views.AddPhoto.as_view(), name="add_photo")
]