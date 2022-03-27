from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager
from photo.fields import ThumbnailImageField

class Post(models.Model):
    title = models.CharField(verbose_name='TITLE', max_length=50)
    slug = models.SlugField('SLUG', unique=True, allow_unicode=True, help_text='one word for title alias.')
    # 제목의 별칭, unique: 기본키로 사용하기 위해, allow_unicode: 한글 처리
    description = models.CharField('DESCRIPTION', max_length=100, blank=True, help_text='simple description text.')
    content = models.TextField('CONTENT')
    create_dt = models.DateTimeField('CREATE DATE', auto_now_add=True)
    modify_dt = models.DateTimeField('MODIFY DATE', auto_now=True)
    tags = TaggableManager(blank=True)

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        db_table = 'blog_posts' # db에 저장되는 테이블명 default: 앱명_모델클래스명
        ordering = ('-modify_dt',) # 모델 객체 리스트 출력 시 modify_dt 컬럼을 내림차순으로 정렬

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=(self.slug,))

    def get_previous(self):
        return self.get_previous_by_modify_dt() # 장고 내장 함수를 이용해 modify_dt 컬럼 기준으로 이전 포스트를 반환

    def get_next(self):
        return self.get_next_by_modify_dt() # 장고 내장 함수를 이용해 modify_dt 컬럼 기준으로 다음 포스트를 반환


