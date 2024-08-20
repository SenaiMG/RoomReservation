from django.shortcuts import redirect, render,get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from rooms.models import  *
from rooms.forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rooms.service import RoomService

class RoomListView(View):
    template_name = 'rooms/classrooms.html'
    paginate_by = 10  

    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('search', '')
        page = request.GET.get('page', 1)
        per_page = self.paginate_by
        
        if search_query:
            rooms = RoomService.search_rooms(search_query, page=page, per_page=per_page)
        else:
            rooms = RoomService.list_all_rooms(page=page, per_page=per_page)
        
        form = RoomsForm()
        return render(request, self.template_name, {'rooms': rooms, 'form': form, 'search_query': search_query})

class RoomCreateView(View):
    def post(self, request, *args, **kwargs):
        form = RoomsForm(request.POST)
        if form.is_valid():
            RoomService.create_new_room(form.cleaned_data['name'])
            messages.success(request, "Sala criada com sucesso!")
            return redirect('all_rooms')
        else:
            messages.error(request, "Erro ao criar a sala.")
        return redirect('all_rooms')

class RoomUpdateView(View):
    def post(self, request, rooms_id, *args, **kwargs):
        form = RoomsForm(request.POST)
        if form.is_valid():
            RoomService.update_existing_room(rooms_id, form.cleaned_data['name'])
            messages.success(request, "Sala atualizada com sucesso!")
        else:
            messages.error(request, "Erro ao atualizar a sala.")
        return redirect('all_rooms')


class RoomDeleteView(View):
    def get(self, request, rooms_id, *args, **kwargs):
        RoomService.delete_room(rooms_id)
        messages.success(request, "Sala deletada com sucesso!")
        return redirect('all_rooms')







    