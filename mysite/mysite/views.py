from django.views.generic import TemplateView, CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import AccessMixin  # 뷰 처리 진입 단계에서 적절한 권한을 갖추었는지 판별하는 믹스인 클래스

class HomeView(TemplateView):
    template_name = 'home.html'

class UserCreateView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register_done') # 폼에 입력된 내용에 에러가 없고 테이블 레코드 생성이 완료되면 이동할 URL

class UserCreateDoneTV(TemplateView):
    template_name = 'registration/register_done.html'

class OwnerOnlyMixin(AccessMixin):
    raise_exception = True  # 소유자가 아닌 경우, True면 403 익셉션 처리, False면 로그인 페이지로 리다이렉트
    permission_denied_message = "Owner only can update/delete the object"   # 403 응답 시 보여주는 메세지

    # bookmark/views 에서는 form 함수 파라미터에 request 안넣고 self.request를 썼지만 dispatch에서는 함수 내에서 필요해서 가져옴
    def dispatch(self, request, *arg, **kwargs):    # get 처리 이전 단계, 소유자 여부를 판단하는 단계
        obj = self.get_object() # 대상이 되는 객체를 테이블로부터 가져옴

        if request.user != obj.owner:   # 현재의 사용자와 객체의 작성자 비교
            return self.handle_no_permission()  # 위에 지정한 403 익셉션 발생
        return super().dispatch(request, *arg, **kwargs)    # 같으면 상위 클래스 dispatch 호출하여 정상처리








        
