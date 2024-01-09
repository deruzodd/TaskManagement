from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from .views import create_task, detail, edit, delete, post_comment
from .models import Task, Comment
from accounts.models import Team

''' Test urls '''


class URLTestClass(SimpleTestCase):
    def test_create_task_url(self):
        url = reverse('tasks:create')
        self.assertEqual(resolve(url).func, create_task)

    def test_detail_url(self):
        url = reverse('tasks:detail', args=[1])
        self.assertEqual(resolve(url).func, detail)

    def test_edit_url(self):
        url = reverse('tasks:edit')
        self.assertEqual(resolve(url).func, edit)

    def test_delete_url(self):
        url = reverse('tasks:delete', args=[1])
        self.assertEqual(resolve(url).func, delete)

    def test_comment_url(self):
        url = reverse('tasks:comment', args=[1])
        self.assertEqual(resolve(url).func, post_comment)


''' Test views '''


class ViewsTestClass(TestCase):

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('accounts:login')
        self.create_task_url = reverse('tasks:create')
        self.edit_task_url = reverse('tasks:edit')
        self.credentials = {
            'username': 'shubhadeep',
            'password': 'deep1234'
        }
        self.test_user = User.objects.create_user(**self.credentials)

    def test_create_task_view_GET(self):
        """
        Check view when user is not logged in
        """
        response = self.client.get(self.create_task_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

        """
        Check view when user is logged in
        """
        self.client.post(self.login_url, self.credentials, follow=True)
        response = self.client.get(self.create_task_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create.html')

    def test_create_task_view_POST(self):
        test_task = {
            'title': 'Task 1',
            'description': 'Task 1 body',
            'status': 'Planned',
            'assignee': [self.test_user]
        }

        """
        Create task after login
        """
        self.client.post(self.login_url, self.credentials, follow=True)
        response = self.client.post(
            self.create_task_url, data=test_task, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.client.logout()

        """
        Create task with invalid fields
        """
        test_task['team_id'] = 2
        self.client.post(self.login_url, self.credentials, follow=True)
        response = self.client.post(
            self.create_task_url, data=test_task, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.client.logout()

        """
        Create task with team
        """
        test_team = Team.objects.create(
            team_name='Team 1')
        test_team.members.add(self.test_user)
        test_team_id = test_team.id

        test_task['title'] = 'Task 2'
        test_task['team_id'] = test_team_id
        self.client.post(self.login_url, self.credentials, follow=True)
        response = self.client.post(
            self.create_task_url, data=test_task, follow=True)

        task = Task.objects.get(title='Task 2')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'team_detail.html')
        self.assertEqual(task.team, test_team)
        self.client.logout()

    def test_detail_task_view(self):
        test_task = {
            'title': 'Task 1',
            'description': 'Task 1 body',
            'status': 'Planned',
            'assignee': [self.test_user]
        }

        url = reverse('tasks:detail', args=[1])

        """
        Check view when user is not logged in
        """
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

        """
        Check view when user is logged in, with invalid task_id
        """
        self.client.post(self.login_url, self.credentials, follow=True)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

        """
        Create task after login
        """
        self.client.post(self.login_url, self.credentials, follow=True)
        self.client.post(self.create_task_url, data=test_task, follow=True)

        task = Task.objects.get(title='Task 1')
        task_id = task.id

        url = reverse('tasks:detail', args=[task_id])

        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'detail.html')
        self.client.logout()

        '''
        Check if another user can view task
        '''
        test_creds_2 = {
            'username': 'priyansh',
            'password': 'deep1234'
        }
        test_user_2 = User.objects.create_user(**test_creds_2)

        self.client.post(self.login_url, test_creds_2, follow=True)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

        del test_user_2
        task.delete()

    def test_edit_task_view_GET(self):
        """
        Check view without login
        """
        response = self.client.get(self.edit_task_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

        '''
        Check view after login
        '''
        self.client.login(**self.credentials)
        response = self.client.get(self.edit_task_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_edit_task_view_POST(self):
        test_task = {
            'title': 'Task 1',
            'description': 'Task 1 body',
            'status': 'Planned',
            'assignee': [self.test_user]
        }

        '''
        Pass invalid task_id
        '''
        self.client.login(**self.credentials)
        response = self.client.post(self.edit_task_url, {
            'task_id': 101
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

        '''
        Pass valid task_id
        '''
        self.client.post(self.create_task_url, data=test_task, follow=True)

        task = Task.objects.get(title="Task 1")
        task_id = task.id

        response = self.client.post(self.edit_task_url, {
            'task_id': task_id,
            'title': 'Task 2',
            'description': task.description,
            'status': 'Done'
        }, follow=True)

        new_task = Task.objects.get(pk=task_id)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertEqual(new_task.title, 'Task 2')
        self.assertEqual(new_task.status, 'Done')

        new_task.delete()

    def test_delete_task_view(self):
        test_task = {
            'title': 'Task 1',
            'description': 'Task 1 body',
            'status': 'Planned',
            'assignee': [self.test_user]
        }

        '''
        Check view without login
        '''
        url = reverse('tasks:delete', args=[1])
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

        '''
        Check view with login, but invalid task_id
        '''
        url = reverse('tasks:delete', args=[1])
        self.client.login(**self.credentials)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

        '''
        Check view with login, and valid task_id
        '''
        self.client.post(self.create_task_url, data=test_task, follow=True)

        task = Task.objects.get(title="Task 1")
        task_id = task.id

        url = reverse('tasks:delete', args=[task_id])

        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertQuerysetEqual(
            Task.objects.all(),
            []
        )

        '''
        Check if another user can delete task
        '''
        test_creds_2 = {
            'username': 'priyansh',
            'password': 'deep1234'
        }
        test_user_2 = User.objects.create_user(**test_creds_2)

        self.client.login(**self.credentials)
        self.client.post(self.create_task_url, data=test_task, follow=True)
        self.client.logout()

        self.client.post(self.login_url, test_creds_2, follow=True)

        task = Task.objects.get(title="Task 1")
        task_id = task.id

        url = reverse('tasks:delete', args=[task_id])

        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertQuerysetEqual(
            Task.objects.all(),
            ['<Task: Task 1>']
        )

        del test_user_2

    def test_comment_view(self):
        test_task = {
            'title': 'Task 1',
            'description': 'Task 1 body',
            'status': 'Planned',
            'assignee': [self.test_user]
        }

        url = reverse('tasks:comment', args=[1])

        '''
        Check view without login
        '''
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

        '''
        Check view after login with invalid task_id
        '''
        self.client.login(**self.credentials)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

        '''
        Check view with login, and valid task_id
        '''
        self.client.post(self.create_task_url, data=test_task, follow=True)

        task = Task.objects.get(title="Task 1")
        task_id = task.id

        url = reverse('tasks:comment', args=[task_id])

        response = self.client.post(
            url, {'comment': 'This is a comment'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'detail.html')
        self.client.logout()

        '''
        Check if another user (except creator, assigned) can 
        comment on  task
        '''
        test_creds_2 = {
            'username': 'priyansh',
            'password': 'deep1234'
        }
        test_user_2 = User.objects.create_user(**test_creds_2)

        self.client.post(self.login_url, test_creds_2, follow=True)
        response = self.client.post(
            url, {'comment': 'This is a new comment'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertQuerysetEqual(
            Comment.objects.all(),
            ['<Comment: This is a comment>']
        )

        del test_user_2
