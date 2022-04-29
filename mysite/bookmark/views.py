from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from bookmark.models import Bookmark
from django.contrib.auth.mixins import LoginRequiredMixin   # @login_required() 데코레이터 기능을 클래스에 적용하기 위해
from django.urls import reverse_lazy    # url 패턴명을 인자로 받아서 URL 반환
from mysite.views import OwnerOnlyMixin # 소유자만 컨텐츠 수정이 가능하도록 하기 위해

class BookmarkLV(ListView):
    model = Bookmark

class BookmarkDV(DetailView):
    model = Bookmark

class BookmarkCreateView(LoginRequiredMixin, CreateView):   # LoginRequiredMixin을 상속받은 클래스는 로그인된 경우에만 접근가능
    model = Bookmark                                        # 안되어 있으면 로그인 페이지로 이동
    fields = ['title', 'url']
    success_url = reverse_lazy('bookmark:index')

    def form_valid(self, form): # 유효성 검사를 통과하면 form_valid 메소드를 호출하여 모델 instance를 생성하고 form 내용을 overwrite
        form.instance.owner = self.request.user
        return super().form_valid(form)

class BookmarkChangeLV(LoginRequiredMixin, ListView):
    template_name = 'bookmark/bookmark_change_list.html'

    def get_queryset(self):
        return Bookmark.objects.filter(owner=self.request.user)

class BookmarkUpdateView(OwnerOnlyMixin, UpdateView):
    model = Bookmark
    fields = ['title', 'url']
    success_url = reverse_lazy('bookmark:index')

class BookmarkDeleteView(OwnerOnlyMixin, DeleteView):
    model = Bookmark
    success_url = reverse_lazy('bookmark:index')


