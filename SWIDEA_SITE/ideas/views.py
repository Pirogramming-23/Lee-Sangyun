from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Idea, DevTool

def idea_list(request):
    sort = request.GET.get('sort', 'latest') 
    if sort == 'name':
        ideas = Idea.objects.all().order_by('title')
    elif sort == 'interest':
        ideas = Idea.objects.all().order_by('-interest')
    elif sort == 'latest':
        ideas = Idea.objects.all().order_by('-pk')
    else: 
        ideas = Idea.objects.all().order_by('pk')

    paginator = Paginator(ideas, 4) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    devtools = DevTool.objects.all()
    
    return render(request, 'ideas/idea_list.html', {'page_obj': page_obj, 'sort': sort, 'devtools': devtools})

def idea_detail(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    return render(request, 'ideas/idea_detail.html', {'idea': idea})

def idea_create(request):
    if request.method == 'POST':
        Idea.objects.create(
            title=request.POST['title'],
            content=request.POST['content'],
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
    if request.method == 'POST':
        idea = get_object_or_404(Idea, pk=pk)
        action = request.POST.get('action') 
        if action == 'plus':
            idea.interest += 1
        elif action == 'minus' and idea.interest > 0:
            idea.interest -= 1
        idea.save()
        return JsonResponse({'interest': idea.interest})
    return JsonResponse({'status': 'error'}, status=400)


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