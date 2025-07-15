from django.db import models
from django.contrib.auth.models import User

class DevTool(models.Model):
    name = models.CharField("이름", max_length=100)
    kind = models.CharField("종류", max_length=100)
    content = models.TextField("설명")

    def __str__(self):
        return self.name

class Idea(models.Model):
    title = models.CharField("제목", max_length=200)
    image = models.ImageField("이미지", blank=True, null=True, upload_to='ideas/%Y/%m/%d')
    content = models.TextField("내용")
    interest = models.IntegerField("관심도", default=0)
    devtool = models.ForeignKey(DevTool, on_delete=models.CASCADE, verbose_name="개발툴")

    def __str__(self):
        return self.title
    
class IdeaStar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.idea.title}"