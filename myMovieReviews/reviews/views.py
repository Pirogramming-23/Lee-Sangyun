from django.shortcuts import render, redirect, get_object_or_404
from .models import Review
from .forms import ReviewForm

def review_list(request):
    reviews = Review.objects.all().order_by('-created_at')
    context = {'reviews': reviews}
    return render(request, 'reviews/review_list.html', context)

def review_detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    running_time_in_minutes = review.running_time
    formatted_time = ""
    if running_time_in_minutes:
        hours = running_time_in_minutes // 60
        minutes = running_time_in_minutes % 60
        
        if hours > 0 and minutes > 0:
            formatted_time = f"{hours}시간 {minutes}분"
        elif hours > 0:
            formatted_time = f"{hours}시간"
        else:
            formatted_time = f"{minutes}분"
    context = {
        'review': review,
        'running_time_display': formatted_time,
    }
    return render(request, 'reviews/review_detail.html', context)

def review_create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reviews:list')
    else:
        form = ReviewForm()
    
    context = {
        'form': form,
        'page_title': 'Movie review 작성 🍿'
    }
    return render(request, 'reviews/review_form.html', context)

def review_update(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('reviews:detail', pk=review.pk)
    else:
        form = ReviewForm(instance=review)
        
    context = {
        'form': form,
        'page_title': 'Movie review 수정 📝'
    }
    return render(request, 'reviews/review_form.html', context)

def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        review.delete()
        return redirect('reviews:list')
    return redirect('reviews:detail', pk=pk)
