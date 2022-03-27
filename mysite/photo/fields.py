# 커스텀 필드를 작성하는 곳
import os
from PIL import Image   # 파이썬 이미지 처리 라이브러리 
from django.db.models.fields.files import ImageField, ImageFieldFile

class ThumbnailImageFieldFile(ImageFieldFile):  # 파일 시스템에 직접 파일을 쓰고 지우는 작업을 함
    def _add_thumb(s):  # 기존 이미지 파일명을 썸네일 이미지 파일명으로 만들어줌
        parts = s.split(".")
        parts.insert(-2, "thumb")
        if parts[-1].lower() not in ['jpeg', 'jpg']:
            parts[-1] = 'jpg'
        return ".".join(parts)

    @property   # 메소드를 멤버변수처럼 사용해줌
    def thumb_path(self):
        return self._add_thumb(self.path)

    @property
    def thumb_url(self):
        return self._add_thumb(self.url)

    def save(self, name, content, save=True):   # 파일시스템에 파일을 저장하고 생성하는 메소드
        super().save(name, content, save)   # 부모 클래스를 통해 원본이미지 저장

        # 원본 이미지로부터 썸네일 이미지 생성
        img = Image.open(self.path)
        size = (self.field.thumb_width, self.field.thumb_height)    # 썸네일 크기의 최대값을 필드옵션으로 지정
        img.thumbnail(size)
        background = Image.new('RGB', size, (255, 255, 255))
        box = (int((size[0] - img.size[0]) / 2), int((size[1] - img.size[1]) / 2))  # 왼쪽 모서리부터 시작해서 어떤 좌표에 위치 시킬지
        background.paste(img, box)  # 썸네일과 백그라운드 이미지를 합쳐서 썸네일 이미지를 만듬
        background.save(self.thumb_path, "JPEG")    # 형식 지정해서 thumb_path 경로에 저장

    def delete(self, save=True):    # 메소드 호출 시 원본 이미지 뿐만 아니라 썸네일 이미지도 같이 삭제 되도록 설정
        if os.path.exists(self.thumb_path):
            os.remove(self.thumb_path)
        super().delete(save)

class ThumbnailImageField(ImageField):  # 장고 모델 정의에 사용하는 필드 역할
    attr_class = ThumbnailImageFieldFile    # FileField 클래스를 정의할 때 그에 상응하는 File 처리 클래스를 attr_class 속성에 지정해야함

    def __init__(self, verbose_name=None, thumb_width=128, thumb_height=128, **kwargs): # 필드에 별칭을 주거나 이미지 최대 크기 지정 가능
        self.thumb_width, self.thumb_height = thumb_width, thumb_height
        super().__init__(verbose_name, **kwargs)



