from django.urls import path
from library_app.users import views

urlpatterns = [
    path('', views.UserListView.as_view(),
         name='user_list'),
    path('create/', views.UserCreateView.as_view(),
         name='user_create'),
    path('<int:pk>/update/', views.UserUpdateView.as_view(),
         name='user_update'),
    path('<int:pk>/delete/', views.UserDeleteView.as_view(),
         name='user_delete'),
    path('<int:pk>', views.UserPageView.as_view(),
         name='user_page')
]
