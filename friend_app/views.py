from django.shortcuts import render
from .models import FriendlyUser, Friendship
from django.http import Http404, HttpResponseRedirect, HttpResponseBadRequest
from operator import attrgetter
from django.utils import timezone
from django.urls import reverse
from django.db.models import Q


def get_friends(user):
    def get_f1(friendship):
        return friendship.friend1

    def get_f2(friendship):
        return friendship.friend2

    return list(map(get_f2, user.friend1.all())) + list(map(get_f1, user.friend2.all()))


def user_list(request):
    users = FriendlyUser.objects.order_by('username')
    return render(request, 'friend_app/list.html', {'users': users})


def user_retrieve(request, friendly_user_id):
    try:
        u = FriendlyUser.objects.get(id=friendly_user_id)
    except:
        raise Http404('Page not found')

    friends = sorted(get_friends(u), key=attrgetter('username'))

    return render(request, 'friend_app/retrieve.html', {'user': u, 'friends': friends})


def start_friendship(request, user_id_1):
    user_id_2 = request.POST["friend_id"]
    try:
        u1 = FriendlyUser.objects.get(id=user_id_1)
        u2 = FriendlyUser.objects.get(id=user_id_2)
    except:
        return HttpResponseBadRequest('User not in database')

    if u2 == u1:
        return HttpResponseBadRequest('Friendship requires two distinct users')

    if u1 not in get_friends(u2):
        date = timezone.now()
        Friendship(friend1=u1, friend2=u2, date=date).save()

    return HttpResponseRedirect(reverse('friend_app:retrieve', args=(user_id_1,)))


def end_friendship(request, user_id_1):
    user_id_2 = request.POST["friend_id"]
    try:
        u1 = FriendlyUser.objects.get(id=user_id_1)
        u2 = FriendlyUser.objects.get(id=user_id_2)
    except:
        return HttpResponseBadRequest('User not in database')

    if u1 in get_friends(u2):
        Friendship.objects.get(Q(friend1=u1, friend2=u2) | Q(friend1=u2, friend2=u1)).delete()

    return HttpResponseRedirect(reverse('friend_app:retrieve', args=(user_id_1,)))
