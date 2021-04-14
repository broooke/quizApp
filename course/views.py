from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, resolve_url

# Create your views here.
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView, CreateView, ListView, DetailView
from django.views.generic.base import View
from django.views.generic.edit import ProcessFormView
from django.views.decorators.csrf import csrf_protect

from .decorators import admin_only
from .forms import UserRegisterForm
from .models import Course, Result, Answer, Question
from django.contrib import messages

class HomeView(TemplateView):
    template_name = 'main/main.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return redirect('admin-dashboard')
            else:
                return redirect('user-dashboard')
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class LoginAdminView(LoginView):
    template_name = 'main/adminLogin.html'
    success_url = reverse_lazy('admin-dashboard')
    redirect_authenticated_user = True

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or resolve_url(settings.LOGIN_ADMIN_REDIRECT_URL)

    def form_valid(self, form):
        user = form.get_user()
        if user.is_staff:
            login(self.request, user)
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.add_message(self.request, messages.INFO, 'У вас нет прав для входа в "Админ" аккаунт.')
            return redirect('login')


class LoginUserView(LoginView):
    template_name = 'main/userLogin.html'
    success_url = reverse_lazy('user-dashboard')
    redirect_authenticated_user = True

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or resolve_url(settings.LOGIN_USER_REDIRECT_URL)

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_staff:
            login(self.request, user)
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.add_message(self.request, messages.INFO, 'У вас есть права для входа в "Админ аккаунт". Введите логин и пароль еще раз.')
            return redirect('login-admin')


class SignUpView(SuccessMessageMixin, CreateView):
   template_name = 'main/register.html'
   success_url = reverse_lazy('login')
   form_class = UserRegisterForm
   success_message = "Your profile was created successfully"


@method_decorator(login_required(login_url='login'), name='dispatch')
class UserHomeView(TemplateView):
    template_name = 'main/homeUser.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count_course'] = Course.objects.all().count()
        context['count_done_course'] = Result.objects.filter(customer=self.request.user).count()
        context['count_q'] = Question.objects.all().count()
        return context

@method_decorator(login_required(login_url='login'), name='dispatch')
class UserCoursesView(ListView):
    model = Course
    template_name = 'main/coursesUser.html'


@method_decorator(login_required(login_url='login'), name='dispatch')
class UserCourseView(DetailView):
    model = Course
    template_name = 'main/courseUser.html'
    slug_field = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = self.object.question_course.all()
        return context

    def post(self, request, *args, **kwargs):
        answer = request.POST
        obj = self.get_object()
        obj.customers.add(request.user)
        questions = obj.question_course.all()
        total_marks = 0
        id = 1
        for q in questions:
            answer_q = answer[str(id)]
            if answer_q == q.answer:
                total_marks+=q.mark
            Answer.objects.create(
                course = obj,
                customer = request.user,
                question = q,
                answer=answer_q,
            )
            id += 1

        Result.objects.create(
            customer = request.user,
            course = obj,
            total_mark = total_marks,
        )

        return redirect('user-courses')

@method_decorator(login_required(login_url='login-admin'), name='dispatch')
@method_decorator(admin_only, name='dispatch')
class AdminResultsView(ListView):
    model = Result
    template_name = 'main/resultsAdmin.html'

@method_decorator(login_required(login_url='login-admin'), name='dispatch')
@method_decorator(admin_only, name='dispatch')
class AdminResultView(DetailView):
    model = Result
    template_name = 'main/adminResult.html'
    slug_field = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.object.course
        qs = self.object.course.question_course.all()
        context['questions'] = qs
        answers = Answer.objects.filter(course=course, customer=self.object.customer)
        context['answers'] = answers
        return context

@method_decorator(login_required(login_url='login-admin'), name='dispatch')
@method_decorator(admin_only, name='dispatch')
class AdminDashboardView(TemplateView):
    template_name = 'main/adminDashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count_course'] = Course.objects.all().count()
        context['count_done_course'] = Result.objects.all().count()
        context['count_users'] = User.objects.all().count()
        return context


@method_decorator(login_required(login_url='login'), name='dispatch')
class UserLogoutView(LogoutView):
    next_page = reverse_lazy('main-page')




