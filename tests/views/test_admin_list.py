from django.contrib.auth.models import User, Permission

from ..test_case import AppTestCase


class AdminListViewTestCase(AppTestCase):
    fixtures = ['test.json']

    def setUp(self):
        self.user = User.objects.create_user('user', 'user@test.com', 'password', is_staff=True)
        self.access_admin = Permission.objects.get(codename='access_admin')
        self.add_perm = Permission.objects.get(codename='add_form')
        self.change_perm = Permission.objects.get(codename='change_form')
        self.client.login(username='user', password='password')

    def test_get_responds(self):
        self.user.user_permissions.add(self.access_admin, self.add_perm)
        response = self.client.get('/cms/wagtailstreamforms/form/')
        self.assertEqual(response.status_code, 200)

    def test_copy_button_uses_add_perm(self):
        self.user.user_permissions.add(self.access_admin, self.change_perm)

        response = self.client.get('/cms/wagtailstreamforms/form/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('title="Copy this Form">Copy</a>', str(response.content))

        self.user.user_permissions.add(self.access_admin, self.add_perm)

        response = self.client.get('/cms/wagtailstreamforms/form/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('title="Copy this Form">Copy</a>', str(response.content))
