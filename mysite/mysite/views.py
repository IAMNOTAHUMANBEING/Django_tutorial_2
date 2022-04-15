from django.views.generic import TemplateView, CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

class HomeView(TemplateView):
    template_name = 'home.html'

class UserCreateView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register_done') # 폼에 입력된 내용에 에러가 없고 테이블 레코드 생성이 완료되면 이동할 URL

class UserCreateDoneTV(TemplateView):
    template_name = 'registration/register_done.html'