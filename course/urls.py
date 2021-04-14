from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='main-page'),
    path('login/admin/', views.LoginAdminView.as_view(), name='login-admin'),
    path('login/user/', views.LoginUserView.as_view(), name='login'),
    path('user/logout/', views.UserLogoutView.as_view(), name='logout-user'),
    path('register/', views.SignUpView.as_view(), name='register'),
    path('user/dashboard/', views.UserHomeView.as_view(), name='user-dashboard'),
    path('user/courses/', views.UserCoursesView.as_view(), name='user-courses'),
    path('user/course/<slug:slug>/', views.UserCourseView.as_view(), name='user-course'),
    path('admin_user/results/', views.AdminResultsView.as_view(), name='admin-results'),
    path('admin_user/result/<slug:slug>/', views.AdminResultView.as_view(), name='admin-result'),
    path('admin_user/dashboard/', views.AdminDashboardView.as_view(), name='admin-dashboard'),
]