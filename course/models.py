from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField("Имя", max_length=256, blank=True, null=True)
    last_name = models.CharField("Фамилия", max_length=256, blank=True, null=True)
    picture = models.ImageField("Фотография", upload_to='customer/', default='/teacher.png', null=True, blank=True)
    email = models.EmailField("Адрес электронной почты", max_length=256, blank=True, null=True)
    telephone = models.CharField("Телефон", max_length=256, blank=True, null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

class Course(models.Model):
    name = models.CharField("Наименование опроса", max_length=256, null=True, blank=True)
    customers = models.ManyToManyField(User, verbose_name="Прошедшие тест", blank=True, null=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    ANSWER_CHOICES = [
        ('choice_1', 'Вариант ответа №1'),
        ('choice_2', 'Вариант ответа №2'),
        ('choice_3', 'Вариант ответа №3'),
        ('choice_4', 'Вариант ответа №4'),
    ]

    course = models.ForeignKey(Course, verbose_name="Наименование курса", on_delete=models.CASCADE, blank=True, null=True, related_name="question_course")
    name = models.CharField("Наименование вопроса", max_length=256, null=True, blank=True)
    mark = models.PositiveIntegerField("Оценка", default=0)
    choice_1 = models.CharField("Вариант ответа №1", max_length=256, null=True, blank=True)
    choice_2 = models.CharField("Вариант ответа №2", max_length=256, null=True, blank=True)
    choice_3 = models.CharField("Вариант ответа №3", max_length=256, null=True, blank=True)
    choice_4 = models.CharField("Вариант ответа №4", max_length=256, null=True, blank=True)
    answer = models.CharField("Правильный ответ", max_length=256, choices=ANSWER_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.name

class Result(models.Model):
    customer = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE, blank=True, null=True)
    course = models.ForeignKey(Course, verbose_name="Наименование курса", on_delete=models.CASCADE, blank=True, null=True, related_name="result_course")
    total_mark = models.PositiveIntegerField("Итоговая оценка", default=0)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.course.name) + " - " + self.customer.first_name + " " + self.customer.last_name

class Answer(models.Model):
    course = models.ForeignKey(Course, verbose_name="Наименование курса", on_delete=models.CASCADE, blank=True, null=True, related_name="answer_course")
    customer = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE, blank=True, null=True, related_name='answer_user')
    question = models.ForeignKey(Question, verbose_name="Вопрос", on_delete=models.CASCADE, blank=True, null=True, related_name='answer_question')
    answer = models.CharField('Ответ пользователя', max_length=256, null=True, blank=True)

    def __str__(self):
        return self.question.name + '(' + self.customer.first_name + " " + self.customer.last_name + '): ' + self.answer