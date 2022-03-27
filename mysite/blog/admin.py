from django.contrib import admin
from blog.models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'modify_dt', 'tag_list')
    list_filter = ('modify_dt',)
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}  # slug 필드가 타이틀로 미리 채워져 있게 설정

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')   # prefetch_related는 N:N 관계에서 쿼리 횟수를 줄여 성능을 높일 때 사용

    def tag_list(self, obj):    # list_display에 외부 패키지 클래스는 등록할 수 없으므로 직접 정의해서 등록
        return ', '.join(o.name for o in obj.tags.all())
