from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Review
from .forms import ReviewForm

# 리뷰 리스트
class ReviewListView(ListView):
    model = Review
    context_object_name = 'reviews'
    template_name = 'reviews/review_list.html'
    ordering = ['-created_at']

# 리뷰 상세
class ReviewDetailView(DetailView):
    model = Review
    context_object_name = 'review'
    template_name = 'reviews/review_detail.html'

# 리뷰 작성
class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'
    success_url = reverse_lazy('reviews:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Movie review'
        return context

# 리뷰 수정
class ReviewUpdateView(UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Movie review'
        return context

# 리뷰 삭제
class ReviewDeleteView(DeleteView):
    model = Review
    success_url = reverse_lazy('reviews:list')
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)