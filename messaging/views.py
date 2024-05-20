from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Thread, Message
from .forms import MessageForm
from django.contrib.auth.models import User


@login_required
def thread_list(request):
    threads = request.user.threads.all()
    return render(request, 'messaging/thread_list.html', {'threads': threads})


@login_required
def thread_detail(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    if request.user not in thread.participants.all():
        return redirect('thread_list')
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.thread = thread
            message.sender = request.user
            message.save()
            return redirect(f'/messaging/thread/{thread.pk}/')
    else:
        form = MessageForm()

    return render(request, 'messaging/thread_detail.html', {'thread': thread, 'form': form})


@login_required
def start_thread(request, user_id):
    user = User.objects.get(id=user_id)

    existing_threads = Thread.objects.filter(Q(participants=request.user) & Q(participants=user)
                        ).distinct().first()
    
    if existing_threads:
        thread = existing_threads
    else:
        thread = Thread.objects.create()
        thread.participants.add(request.user, user)
    return redirect(f'/messaging/thread/{thread.pk}/')