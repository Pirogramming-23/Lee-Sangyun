from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Idea, DevTool # IdeaStar는 더 이상 사용하지 않습니다.

def idea_list(request):
    sort = request.GET.get('sort', 'latest')

    if sort == 'interest':
        ideas = Idea.objects.order_by('-interest', '-pk')
    elif sort == 'name':
        ideas = Idea.objects.all().order_by('title')
    else: # latest
        ideas = Idea.objects.all().order_by('-pk')

    paginator = Paginator(ideas, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 세션에서 찜한 아이디어 ID 목록을 가져옵니다.
    starred_idea_ids = request.session.get('starred_ideas', [])
    for idea in page_obj:
        idea.is_starred = idea.id in starred_idea_ids

    context = {
        'page_obj': page_obj,
        'sort': sort,
    }
    return render(request, 'ideas/idea_list.html', context)

def idea_detail(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    # 상세 페이지에서도 세션을 확인하여 찜 여부를 전달합니다.
    starred_idea_ids = request.session.get('starred_ideas', [])
    idea.is_starred = idea.id in starred_idea_ids
    
    return render(request, 'ideas/idea_detail.html', {'idea': idea})

def idea_create(request):
    if request.method == 'POST':
        Idea.objects.create(
            title=request.POST['title'],
            content=request.POST['content'],
            # ## 이 부분을 추가해야 합니다 ##
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
        idea.devtool = get_object_or_404(DevTool, pk=request.POST['devtool'])
        # ## 이 부분을 추가해야 합니다 ##
        idea.interest = int(request.POST.get('interest', 0))
        
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

def toggle_star(request, pk):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

    # 세션에서 찜 목록을 가져오거나, 없으면 빈 리스트로 시작합니다.
    starred_ideas = request.session.get('starred_ideas', [])
    
    # 찜 상태를 토글합니다.
    if pk in starred_ideas:
        starred_ideas.remove(pk)
        is_starred = False
    else:
        starred_ideas.append(pk)
        is_starred = True
    
    # 변경된 목록을 다시 세션에 저장합니다.
    request.session['starred_ideas'] = starred_ideas

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