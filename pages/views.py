from django.shortcuts import render, get_object_or_404

from rest.models import Room


# Create your views here.


def charts(request, *args, **kwargs):
    rooms_list = Room.objects.all()
    room = get_object_or_404(Room, name=kwargs['room_name'])
    return render(request, "charts.html",
                              {
                                  'room_name': kwargs['room_name'],
                                  'rooms': rooms_list
                              }
                  )


def manager(request):
    rooms_list = Room.objects.all()
    return render(request, "manager.html", {
        'rooms': rooms_list
    })
