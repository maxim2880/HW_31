from django.urls import path

from ads import views

urlpatterns = [
    path('', views.SelectionListView.as_view(), name='selection_list'),
    path('<int:pk>/', views.SelectionDetailView.as_view()),
    path('create/', views.SelectionCreateView.as_view(), name='selection_create'),
    path('<int:pk>/update/', views.SelectionUpdateView.as_view()),
    path('<int:pk>/delete/', views.SelectionDeleteView.as_view()),

]