from django.contrib import admin
from bookmark.models import Bookmark

@admin.register(Bookmark)
# 위랑 같은 표현 admin.site.register(Bookmark, BookmarkAdmin)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'url')


