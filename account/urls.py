from django.urls import path
from .views import RegisterView, LoginView, ProfileView, AllUserDetailsView

urlpatterns = [
    path("api/register", RegisterView.as_view(), name='register'),
    path("api/login", LoginView.as_view(), name='login'),
    path("api/profile", ProfileView.as_view(), name='profile'),
    path("api/admin/users", AllUserDetailsView.as_view(), name='admin-users'),
]
