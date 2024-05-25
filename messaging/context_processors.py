from .models import ThreadUser, Thread, Message
from django.db.models import Q, Count, OuterRef, Subquery

def new_messages(request):
    if not request.user.is_authenticated:
        return {'new_messages': 0}

    last_read_subquery = ThreadUser.objects.filter(
        user=request.user,
        thread=OuterRef('pk')
    ).values('last_read')[:1]

    threads = Thread.objects.filter(
        participants=request.user  # Assuming 'participants' is the correct field
    ).annotate(
        unread_count=Count('messages', filter=Q(messages__timestamp__gt=Subquery(last_read_subquery)))
    ).order_by('-created')

    new_messages_count = sum(thread.unread_count for thread in threads)

    return {'new_messages': new_messages_count}