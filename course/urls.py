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
    path('user/update/<slug:slug>/', views.UserUpdateView.as_view(), name='user-update'),
    path('admin_user/results/', views.AdminResultsView.as_view(), name='admin-results'),
    path('admin_user/result/<slug:slug>/', views.AdminResultView.as_view(), name='admin-result'),
    path('admin_user/dashboard/', views.AdminDashboardView.as_view(), name='admin-dashboard'),
    path('admin_user/users/', views.AdminUsersView.as_view(), name='admin-users'),
    path('admin_user/delete/user/<str:pk>/', views.DeleteUserView.as_view(), name='delete-user'),
    path('admin_user/courses/', views.AdminCoursesView.as_view(), name='admin-courses'),
    path('admin_user/course/<slug:slug>/', views.AdminCourseView.as_view(), name='admin-course'),
    path('admin_user/add/course/', views.AdminAddCourseView.as_view(), name='admin-add-course'),
    path('admin_user/questions/', views.AdminQuestionsView.as_view(), name='admin-questions'),
    path('admin_user/question/add/', views.AdminAddQuestionView.as_view(), name='admin-add-q'),
    path('admin_user/question/update/<slug:slug>/', views.AdminUpdateQuestionView.as_view(), name='admin-update-q'),
    path('admin_user/question/delete/<str:pk>/', views.DeleteQuestionView.as_view(), name='admin-delete-q'),
]