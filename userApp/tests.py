from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import UserProfile, EmergencyContact, HealthInfo, Notification
from .forms import UserRegistrationForm, UserProfileForm, EmergencyContactForm, HealthInfoForm

class UserAuthTests(TestCase):
    def setUp(self):
        """测试前的准备工作"""
        self.client = Client()
        self.test_user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.login_url = reverse('user:login')
        self.register_url = reverse('user:register')
        self.profile_url = reverse('user:profile')

    def test_user_registration(self):
        """测试用户注册"""
        data = {
            'username': 'newuser',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 302)  # 重定向到个人资料页面
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_login(self):
        """测试用户登录"""
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # 重定向到首页
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_user_logout(self):
        """测试用户注销"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('user:logout'))
        self.assertEqual(response.status_code, 302)  # 重定向到首页
        self.assertFalse('_auth_user_id' in self.client.session)

class UserProfileTests(TestCase):
    def setUp(self):
        """测试前的准备工作"""
        self.client = Client()
        self.test_user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')

    def test_profile_view(self):
        """测试个人资料页面访问"""
        response = self.client.get(reverse('user:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/profile.html')

    def test_profile_update(self):
        """测试更新个人资料"""
        data = {
            'phone': '1234567890',
            'address': '测试地址',
            'birth_date': '2000-01-01'
        }
        response = self.client.post(reverse('user:profile'), data)
        self.assertEqual(response.status_code, 302)  # 重定向到个人资料页面
        profile = UserProfile.objects.get(user=self.test_user)
        self.assertEqual(profile.address, '测试地址')

class EmergencyContactTests(TestCase):
    def setUp(self):
        """测试前的准备工作"""
        self.client = Client()
        self.test_user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')

    def test_add_emergency_contact(self):
        """测试添加紧急联系人"""
        data = {
            'name': '测试联系人',
            'relationship': '亲属',
            'phone': '1234567890'
        }
        response = self.client.post(reverse('user:emergency_contacts'), data)
        self.assertEqual(response.status_code, 302)  # 重定向到紧急联系人列表
        self.assertTrue(EmergencyContact.objects.filter(user=self.test_user).exists())

    def test_delete_emergency_contact(self):
        """测试删除紧急联系人"""
        contact = EmergencyContact.objects.create(
            user=self.test_user,
            name='测试联系人',
            relationship='亲属',
            phone='1234567890'
        )
        response = self.client.post(reverse('user:delete_emergency_contact', args=[contact.id]))
        self.assertEqual(response.status_code, 302)  # 重定向到紧急联系人列表
        self.assertFalse(EmergencyContact.objects.filter(id=contact.id).exists())

class HealthInfoTests(TestCase):
    def setUp(self):
        """测试前的准备工作"""
        self.client = Client()
        self.test_user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')

    def test_update_health_info(self):
        """测试更新健康信息"""
        data = {
            'blood_type': 'A',
            'allergies': '无',
            'medical_conditions': '无',
            'medications': '无'
        }
        response = self.client.post(reverse('user:health_info'), data)
        self.assertEqual(response.status_code, 302)  # 重定向到健康信息页面
        health_info = HealthInfo.objects.get(user=self.test_user)
        self.assertEqual(health_info.blood_type, 'A')

class NotificationTests(TestCase):
    def setUp(self):
        """测试前的准备工作"""
        self.client = Client()
        self.test_user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        self.notification = Notification.objects.create(
            user=self.test_user,
            title='测试通知',
            message='这是一条测试通知',
            notification_type='info'
        )

    def test_notification_list(self):
        """测试通知列表页面"""
        response = self.client.get(reverse('user:notifications'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/notifications.html')
        self.assertContains(response, '测试通知')

    def test_mark_all_notifications_read(self):
        """测试标记所有通知为已读"""
        response = self.client.post(reverse('user:mark_all_notifications_read'))
        self.assertEqual(response.status_code, 302)  # 重定向到通知列表
        notification = Notification.objects.get(id=self.notification.id)
        self.assertTrue(notification.is_read)
