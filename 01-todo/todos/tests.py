from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Todo


class TodoModelTests(TestCase):
    """Test cases for the Todo model"""
    
    def setUp(self):
        """Set up test data"""
        self.todo = Todo.objects.create(
            title="Test Todo",
            description="Test Description",
            due_date=timezone.now() + timedelta(days=1)
        )
    
    def test_todo_creation(self):
        """Test creating a TODO item"""
        self.assertEqual(self.todo.title, "Test Todo")
        self.assertEqual(self.todo.description, "Test Description")
        self.assertFalse(self.todo.resolved)
        self.assertIsNotNone(self.todo.created_at)
        self.assertIsNotNone(self.todo.updated_at)
    
    def test_todo_str_representation(self):
        """Test string representation of TODO"""
        self.assertEqual(str(self.todo), "Test Todo")
    
    def test_todo_default_resolved_status(self):
        """Test that new TODOs are not resolved by default"""
        new_todo = Todo.objects.create(title="New Todo")
        self.assertFalse(new_todo.resolved)
    
    def test_todo_with_due_date(self):
        """Test TODO with due date"""
        self.assertIsNotNone(self.todo.due_date)
        self.assertGreater(self.todo.due_date, timezone.now())
    
    def test_todo_without_due_date(self):
        """Test TODO without due date (optional)"""
        todo_no_date = Todo.objects.create(
            title="No Date Todo",
            description="No due date"
        )
        self.assertIsNone(todo_no_date.due_date)
    
    def test_todo_resolved_status_change(self):
        """Test changing resolved status"""
        self.assertFalse(self.todo.resolved)
        self.todo.resolved = True
        self.todo.save()
        self.assertTrue(self.todo.resolved)
        
        # Verify from database
        updated_todo = Todo.objects.get(pk=self.todo.pk)
        self.assertTrue(updated_todo.resolved)
    
    def test_todo_ordering(self):
        """Test that TODOs are ordered by creation date (newest first)"""
        todo1 = Todo.objects.create(title="First Todo")
        todo2 = Todo.objects.create(title="Second Todo")
        todo3 = Todo.objects.create(title="Third Todo")
        
        todos = Todo.objects.all()
        self.assertEqual(todos[0].title, "Third Todo")
        self.assertEqual(todos[1].title, "Second Todo")
        self.assertEqual(todos[2].title, "First Todo")


class TodoViewTests(TestCase):
    """Test cases for TODO views and operations"""
    
    def setUp(self):
        """Set up test client and test data"""
        self.client = Client()
        self.todo1 = Todo.objects.create(
            title="Todo 1",
            description="Description 1",
            due_date=timezone.now() + timedelta(days=1),
            resolved=False
        )
        self.todo2 = Todo.objects.create(
            title="Todo 2",
            description="Description 2",
            due_date=timezone.now() + timedelta(days=2),
            resolved=True
        )
    
    def test_todo_list_view(self):
        """Test viewing list of all TODOs"""
        response = self.client.get(reverse('todo_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Todo 1")
        self.assertContains(response, "Todo 2")
    
    def test_todo_list_filter_resolved(self):
        """Test filtering TODOs by resolved status"""
        response = self.client.get(reverse('todo_list') + '?status=resolved')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Todo 2")
        # Todo 1 should not be in resolved filter
        todos = response.context['todos']
        self.assertEqual(todos.count(), 1)
        self.assertTrue(todos[0].resolved)
    
    def test_todo_list_filter_pending(self):
        """Test filtering TODOs by pending status"""
        response = self.client.get(reverse('todo_list') + '?status=pending')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Todo 1")
        # Todo 2 should not be in pending filter
        todos = response.context['todos']
        self.assertEqual(todos.count(), 1)
        self.assertFalse(todos[0].resolved)
    
    def test_create_todo(self):
        """Test creating a new TODO"""
        initial_count = Todo.objects.count()
        response = self.client.post(reverse('todo_create'), {
            'title': 'New Todo',
            'description': 'New Description',
            'due_date': (timezone.now() + timedelta(days=3)).strftime('%Y-%m-%d %H:%M:%S')
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertEqual(Todo.objects.count(), initial_count + 1)
        
        new_todo = Todo.objects.get(title='New Todo')
        self.assertEqual(new_todo.description, 'New Description')
        self.assertFalse(new_todo.resolved)
    
    def test_create_todo_without_due_date(self):
        """Test creating TODO without due date"""
        initial_count = Todo.objects.count()
        response = self.client.post(reverse('todo_create'), {
            'title': 'Todo Without Date',
            'description': 'No date specified'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Todo.objects.count(), initial_count + 1)
        
        new_todo = Todo.objects.get(title='Todo Without Date')
        self.assertIsNone(new_todo.due_date)
    
    def test_update_todo(self):
        """Test editing/updating a TODO"""
        response = self.client.post(
            reverse('todo_update', kwargs={'pk': self.todo1.pk}),
            {
                'title': 'Updated Todo',
                'description': 'Updated Description',
                'due_date': (timezone.now() + timedelta(days=5)).strftime('%Y-%m-%d %H:%M:%S'),
                'resolved': False
            }
        )
        self.assertEqual(response.status_code, 302)
        
        updated_todo = Todo.objects.get(pk=self.todo1.pk)
        self.assertEqual(updated_todo.title, 'Updated Todo')
        self.assertEqual(updated_todo.description, 'Updated Description')
    
    def test_update_todo_mark_resolved(self):
        """Test marking TODO as resolved through update view"""
        response = self.client.post(
            reverse('todo_update', kwargs={'pk': self.todo1.pk}),
            {
                'title': self.todo1.title,
                'description': self.todo1.description,
                'due_date': self.todo1.due_date.strftime('%Y-%m-%d %H:%M:%S'),
                'resolved': True
            }
        )
        self.assertEqual(response.status_code, 302)
        
        updated_todo = Todo.objects.get(pk=self.todo1.pk)
        self.assertTrue(updated_todo.resolved)
    
    def test_delete_todo(self):
        """Test deleting a TODO"""
        initial_count = Todo.objects.count()
        todo_id = self.todo1.pk
        
        response = self.client.post(
            reverse('todo_delete', kwargs={'pk': todo_id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Todo.objects.count(), initial_count - 1)
        
        # Verify TODO no longer exists
        with self.assertRaises(Todo.DoesNotExist):
            Todo.objects.get(pk=todo_id)
    
    def test_toggle_resolved_status(self):
        """Test toggling TODO resolved status"""
        initial_status = self.todo1.resolved
        
        response = self.client.get(
            reverse('todo_toggle', kwargs={'pk': self.todo1.pk})
        )
        self.assertEqual(response.status_code, 302)
        
        self.todo1.refresh_from_db()
        self.assertEqual(self.todo1.resolved, not initial_status)
        
        # Toggle again
        response = self.client.get(
            reverse('todo_toggle', kwargs={'pk': self.todo1.pk})
        )
        self.todo1.refresh_from_db()
        self.assertEqual(self.todo1.resolved, initial_status)
    
    def test_create_todo_get_request(self):
        """Test GET request to create view shows form"""
        response = self.client.get(reverse('todo_create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'title')
        self.assertContains(response, 'description')
    
    def test_update_todo_get_request(self):
        """Test GET request to update view shows pre-filled form"""
        response = self.client.get(
            reverse('todo_update', kwargs={'pk': self.todo1.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.todo1.title)
    
    def test_delete_nonexistent_todo(self):
        """Test deleting a TODO that doesn't exist"""
        response = self.client.post(
            reverse('todo_delete', kwargs={'pk': 99999})
        )
        self.assertEqual(response.status_code, 404)
    
    def test_update_nonexistent_todo(self):
        """Test updating a TODO that doesn't exist"""
        response = self.client.post(
            reverse('todo_update', kwargs={'pk': 99999}),
            {'title': 'Test'}
        )
        self.assertEqual(response.status_code, 404)
