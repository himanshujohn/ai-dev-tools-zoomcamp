from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Todo


class TodoListView(ListView):
    model = Todo
    template_name = 'todos/todo_list.html'
    context_object_name = 'todos'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        if status == 'resolved':
            return queryset.filter(resolved=True)
        elif status == 'pending':
            return queryset.filter(resolved=False)
        return queryset


class TodoCreateView(CreateView):
    model = Todo
    template_name = 'todos/todo_form.html'
    fields = ['title', 'description', 'due_date']
    success_url = reverse_lazy('todo_list')


class TodoUpdateView(UpdateView):
    model = Todo
    template_name = 'todos/todo_form.html'
    fields = ['title', 'description', 'due_date', 'resolved']
    success_url = reverse_lazy('todo_list')


class TodoDeleteView(DeleteView):
    model = Todo
    template_name = 'todos/todo_confirm_delete.html'
    success_url = reverse_lazy('todo_list')


def toggle_resolved(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.resolved = not todo.resolved
    todo.save()
    return redirect('todo_list')
