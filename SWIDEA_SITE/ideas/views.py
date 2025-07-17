from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from .models import Idea, DevTool, IdeaStar
from django.template.loader import render_to_string

def idea_list(request):
    sort = request.GET.get('sort', 'latest')
    search_term = request.GET.get('search_term', '')
    devtool_filter = request.GET.get('devtool_filter', '')

    ideas = Idea.objects.all()

    if search_term:
        ideas = ideas.filter(title__icontains=search_term)
    if devtool_filter:
        ideas = ideas.filter(devtool__id=devtool_filter)

    if sort == 'interest':
        ideas = ideas.order_by('-interest', '-pk')
    elif sort == 'star':
        ideas = ideas.annotate(star_count=Count('ideastar')).order_by('-star_count', '-pk')
    elif sort == 'name':
        ideas = ideas.order_by('title')
    else: 
        ideas = ideas.order_by('-pk')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            starred_idea_ids = IdeaStar.objects.filter(user=request.user).values_list('idea_id', flat=True)
            for idea in ideas:
                idea.is_starred = idea.id in starred_idea_ids
        
        html = render_to_string(
            'ideas/partials/idea_card_list.html',
            {'ideas': ideas}
        )
        return JsonResponse({'html': html})

    paginator = Paginator(ideas, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.user.is_authenticated:
        starred_idea_ids = IdeaStar.objects.filter(user=request.user).values_list('idea_id', flat=True)
        for idea in page_obj:
            idea.is_starred = idea.id in starred_idea_ids

    devtools = DevTool.objects.all()
    context = {
        'page_obj': page_obj,
        'devtools': devtools,
        'sort': sort,
        'search_term': search_term,
        'devtool_filter': devtool_filter,
    }
    return render(request, 'ideas/idea_list.html', context)

def idea_detail(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    
    if request.user.is_authenticated:
        idea.is_starred = IdeaStar.objects.filter(user=request.user, idea=idea).exists()
    
    return render(request, 'ideas/idea_detail.html', {'idea': idea})

def idea_create(request):
    if request.method == 'POST':
        Idea.objects.create(
            title=request.POST['title'],
            content=request.POST['content'],
            interest=int(request.POST.get('interest', 0)),
            devtool=get_object_or_404(DevTool, pk=request.POST['devtool']),
            image=request.FILES.get('image'),
        )
        return redirect('ideas:idea_list')
    else:
        devtools = DevTool.objects.all()
        return render(request, 'ideas/idea_form.html', {'devtools': devtools})

def idea_update(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    if request.method == 'POST':
        idea.title = request.POST['title']
        idea.content = request.POST['content']
        idea.interest = int(request.POST.get('interest', 0))
        idea.devtool = get_object_or_404(DevTool, pk=request.POST['devtool'])
        if request.FILES.get('image'):
            idea.image = request.FILES.get('image')
        idea.save()
        return redirect('ideas:idea_detail', pk=idea.pk)
    else:
        devtools = DevTool.objects.all()
        return render(request, 'ideas/idea_form.html', {'idea': idea, 'devtools': devtools})

def idea_delete(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    idea.delete()
    return redirect('ideas:idea_list')

def update_interest(request, pk):
    if request.method != 'POST':
        return JsonResponse({'status': 'error'}, status=400)
    idea = get_object_or_404(Idea, pk=pk)
    action = request.POST.get('action')
    if action == 'plus':
        idea.interest += 1
    elif action == 'minus' and idea.interest > 0:
        idea.interest -= 1
    idea.save()
    return JsonResponse({'interest': idea.interest})

@login_required
def toggle_star(request, pk):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
    
    idea = get_object_or_404(Idea, pk=pk)
    user = request.user
    
    star, created = IdeaStar.objects.get_or_create(user=user, idea=idea)
    
    if created:
        is_starred = True
    else:
        star.delete()
        is_starred = False
        
    return JsonResponse({'is_starred': is_starred})

def devtool_list(request):
    devtools = DevTool.objects.all()
    return render(request, 'ideas/devtool_list.html', {'devtools': devtools})

def devtool_detail(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    related_ideas = Idea.objects.filter(devtool=devtool)
    return render(request, 'ideas/devtool_detail.html', {'devtool': devtool, 'related_ideas': related_ideas})

def devtool_create(request):
    if request.method == 'POST':
        DevTool.objects.create(
            name=request.POST['name'],
            kind=request.POST['kind'],
            content=request.POST['content'],
        )
        return redirect('ideas:devtool_list')
    return render(request, 'ideas/devtool_form.html')

def devtool_update(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    if request.method == 'POST':
        devtool.name = request.POST['name']
        devtool.kind = request.POST['kind']
        devtool.content = request.POST['content']
        devtool.save()
        return redirect('ideas:devtool_detail', pk=devtool.pk)
    return render(request, 'ideas/devtool_form.html', {'devtool': devtool})

def devtool_delete(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    devtool.delete()
    return redirect('ideas:devtool_list')