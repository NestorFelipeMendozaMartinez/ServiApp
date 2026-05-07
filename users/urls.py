from django.urls import path
from .views import RegisterView, ProfileView, UserListView, LoginView, ProviderListView, PublicProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('providers/', ProviderListView.as_view(), name='provider-list'),
    path('providers/<int:user_id>/', PublicProfileView.as_view(), name='public-profile'),
    path('admin/users/', UserListView.as_view(), name='admin-user-list'),
]
