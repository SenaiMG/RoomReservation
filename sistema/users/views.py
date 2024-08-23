from django.shortcuts import redirect, render
from django.contrib import messages
from django.utils.decorators import method_decorator
from .decorators import *
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .service import UserService
from .forms import *



class CustomLoginView(View):
    form_class = EmailLoginForm
    template_name = 'users/login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login realizado com sucesso!")
                if user.user_type == 'teacher':
                    return redirect('teacher_dashboard') 
                elif user.user_type == 'manager':
                    return redirect('manager_dashboard')  
            else:
                messages.error(request, "Email ou senha incorretos")
        return render(request, self.template_name, {'form': form})


@method_decorator(user_is_manager, name='dispatch')
class UserListView(View):
    template_name = 'users/manager/user_list.html'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('search', '')
        page = request.GET.get('page', 1)
        
        if search_query:
            users = UserService.search_users(search_query, page=page, per_page=self.paginate_by)
        else:
            users = UserService.list_all_users(page=page, per_page=self.paginate_by)

        return render(request, self.template_name, {'users': users, 'search_query': search_query})


@method_decorator(user_is_manager, name='dispatch')
class UserCreateView(CreateView):
    template_name = 'users/manager/user_register.html'
    form_class = UserForm
    success_url = reverse_lazy('user_list')

    def form_valid(self, form):
        messages.success(self.request, "Usuário criado com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Ocorreu um erro ao criar o usuário.")
        return super().form_invalid(form)


@method_decorator(user_is_manager, name='dispatch')
class UserUpdateView(UpdateView):
    template_name = 'users/manager/user_register.html'
    form_class = UserForm
    success_url = reverse_lazy('user_list')

    def get_object(self):
        user_id = self.kwargs['pk']
        return UserService.get_user_details(user_id)

    def form_valid(self, form):
        UserService.update_existing_user(self.object.id, **form.cleaned_data)
        messages.success(self.request, "Usuário atualizado com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Ocorreu um erro ao atualizar o usuário.")
        return super().form_invalid(form)


@method_decorator(user_is_manager, name='dispatch')    
class UserDeleteView(DeleteView):
    success_url = reverse_lazy('user_list')  # Redirecionar após exclusão

    def get_object(self):
        user_id = self.kwargs['pk']
        return UserService.get_user_details(user_id)

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        UserService.delete_user(user.id)
        messages.success(request, "Usuário excluído com sucesso!")
        return super().delete(request, *args, **kwargs)


@method_decorator(user_is_manager, name='dispatch')
class DashboardManagerPage(View):
    template_name = 'users/manager/dashboard.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


@method_decorator(user_is_teacher, name='dispatch')
class DashboardTeacherPage(View):
    template_name = 'users/teacher/dashboard.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


@method_decorator(user_is_manager_or_teacher, name='dispatch')
class UserProfileView(View):
    template_name = 'users/profile.html'

    def get(self, request):
        form = ProfileForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect('profile')
        else:
            messages.error(request, "Ocorreu um erro ao atualizar o perfil.")
            return render(request, self.template_name, {'form': form})
    







