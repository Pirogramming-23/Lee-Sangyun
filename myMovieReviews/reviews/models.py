from django.db import models
from django.urls import reverse

class Review(models.Model):
    GENRE_CHOICES = [
        ('Action', '액션'),
        ('Comedy', '코미디'),
        ('Drama', '드라마'),
        ('Horror', '공포'),
        ('Romance', '로맨스'),
        ('SF', 'SF'),
        ('Thriller', '스릴러'),
    ]

    title = models.CharField(max_length=100, verbose_name="영화 제목")
    release_year = models.IntegerField(verbose_name="개봉 년도")
    genre = models.CharField(max_length=10, choices=GENRE_CHOICES, verbose_name="장르")
    rating = models.FloatField(verbose_name="별점")
    director = models.CharField(max_length=50, verbose_name="감독")
    actors = models.CharField(max_length=200, verbose_name="주연")
    running_time = models.IntegerField(verbose_name="러닝타임 (분)")
    content = models.TextField(verbose_name="리뷰 내용")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('reviews:detail', kwargs={'pk': self.pk})