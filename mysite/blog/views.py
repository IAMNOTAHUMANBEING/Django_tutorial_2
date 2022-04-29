from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView, FormView, CreateView, UpdateView, DeleteView
from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView
from django.views.generic.dates import DayArchiveView, TodayArchiveView
from django.conf import settings
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from mysite.views import OwnerOnlyMixin

from blog.models import Post
from blog.forms import PostSearchForm


# ListView
class PostLV(ListView):
    model = Post
    template_name = 'blog/post_all.html'
    context_object_name = 'posts'
    paginate_by = 2

# DetailView
class PostDV(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['disqus_short'] = f"{settings.DISQUS_SHORTNAME}"
        context['disqus_id'] = f"post-{self.object.id}-{self.object.slug}"
        context['disqus_url'] = f"{settings.DISQUS_MY_DOMAIN}{self.object.get_absolute_url()}"
        context['disqus_title'] = f"{self.object.slug}"
        return context

# ArchiveView
class PostAV(ArchiveIndexView): # 테이블에서 객체리스트를 받아와 날짜 최신순으로 출력
    model = Post
    date_field = 'modify_dt'

class PostYAV(YearArchiveView): # 테이블에서 연도를 기준으로 객체리스트를 가져와 객체들이 속한 월을 출력
    model = Post
    date_field = 'modify_dt'    # 수정날짜가 YYYY 연도인 포스트를 검색해 그 포스트의 변경 월을 출력
    make_object_list = True     # 해당 연도에 해당하는 객체의 리스트를 만들어서 템플릿에 넘겨줌

class PostMAV(MonthArchiveView): # 테이블에서 연월을 기준으로 객체리스트를 가져와 출력
    model = Post
    date_field = 'modify_dt'

class PostDAV(DayArchiveView):  # 테이블에서 연월일을 기준으로 객체리스트를 가져와 출력
    model = Post
    date_field = 'modify_dt'

class PostTAV(TodayArchiveView): # 테이블에서 날짜가 오늘인 객체 리스트 가져와 출력
    model = Post
    date_field = 'modify_dt'

class TagCloudTV(TemplateView):
    template_name = 'taggit/taggit_cloud.html'

class TaggedObjectLV(ListView):
    template_name = 'taggit/taggit_post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(tags__name=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag'] # URL에서 넘어온 값 추출
        return context

class SearchFormView(FormView): # 폼 뷰는 GET요청인 경우 폼을 화면에 보여주고 사용자의 입력을 기다림. 입력 후 제출하면 POST요청으로 접수되어
    form_class = PostSearchForm # FormView 클래스에서 유효성 검사를 함. 데이터가 유효한 경우 form_valid 함수 실행한 후 적절한 URL로 리다이렉트
    template_name = 'blog/post_search.html'

    def form_valid(self, form):
        searchWord = form.cleaned_data['search_word']   # 유효성 검사를 통과하면 입력한 데이터가 clead_data 사전에 저장됨
        post_list = Post.objects.filter(Q(title__icontains=searchWord) | Q(description__icontains=searchWord)).distinct()
        # Q 객체는 filter 함수의 매칭조건을 다양하게 줄 수 있게 해준다. icontains 연산자는 대소문자를 구분하지 않고 검색, distinct는 중복X

        context = {}
        context['form'] = form
        context['search_term'] = searchWord
        context['object_list'] = post_list

        return render(self.request, self.template_name, context)
        # 단축함수 render는 템플릿 파일과 컨텍스트 변수를 처리해 최종적으로 HttpResponse 객체를 반환
        # form_valid 함수는 보통 리다이렉트 처리를 위해 HttpResponseRedirect 객체를 반환하지만 여기서는 재정의하여 리다이렉트 사용 X

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'slug', 'description', 'content', 'tags']
    initial = {'slug': 'auto-filling-do-not-input'} # slug는 title 필드로부터 자동으로 채워지는 필드임으로 메세지 삽입, Post모델 정의에 있는 save 함수에서 수행
    # fields = ['title', 'description', 'content', 'tags'] # fields에서 제외하는 방법도 있음
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class PostChangeLV(LoginRequiredMixin, ListView):
    template_name = 'blog/post_change_list.html'

    def get_queryset(self):
        return Post.objects.filter(owner=self.request.user)

class PostUpdateView(OwnerOnlyMixin, UpdateView):
    model = Post
    fields = ['title', 'slug', 'description', 'content', 'tags']
    success_url = reverse_lazy('blog:index')

class PostDeleteView(OwnerOnlyMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:index')
