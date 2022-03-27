from django.contrib import admin
from photo.models import Album, Photo

class PhotoInline(admin.StackedInline): # 앨범 객체 보여줄 때 객체에 연결된 사진 객체들을 같이 보여줌
    model = Photo
    extra = 2   # 기본적으로 입력할 수 있는 Photo 테이블 객체의 수는 2개

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    inlines = (PhotoInline,)
    list_display = ('id', 'name', 'description')

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'upload_dt')
