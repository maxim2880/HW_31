from django.urls import path

from ads import views

urlpatterns = [

    path('', views.AdsListView.as_view(), name='ad_list'),
    path('<int:pk>/', views.AdsDetailView.as_view(), name='ad_detail'),
    path('create/', views.AdsCreateView.as_view(), name='ad_create'),
    path('<int:pk>/update/', views.AdsUpdateView.as_view()),
    path('<int:pk>/delete/', views.AdsDeleteView.as_view()),
    path('<int:pk>/image/', views.AdsImageView.as_view())
]
