from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.db import models
from django.utils import timezone

from .models import Thread, Message, ThreadUser
from .forms import MessageForm
from django.contrib.auth.models import User


@login_required
def thread_list(request):
    threads = request.user.threads.annotate(
        unread_count=Count('messages', filter=Q(messages__timestamp__gt=ThreadUser.objects.filter(
            user=request.user, thread=models.OuterRef('pk')).values('last_read')[:1]))
    )

    return render(request, 'messaging/thread_list.html', {'threads': threads})


@login_required
def thread_detail(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    if request.user not in thread.participants.all():
        return redirect('thread_list')

    thread_user, created = ThreadUser.objects.get_or_create(user=request.user, thread=thread)
    thread_user.last_read = timezone.now()
    thread_user.save()

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
    another_user = get_object_or_404(User, id=user_id)
    existing_thread = Thread.objects.filter(participants=request.user).filter(participants=another_user).first()

    if existing_thread:
        thread = existing_thread
    else:
        thread = Thread.objects.create()
        thread.participants.add(request.user, another_user)

    return redirect(f'/messaging/thread/{thread.pk}/')
