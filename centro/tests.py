from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.urls import resolve

# Import models
from .models import Center, ActivityForKnowledge, GroupTypeForKnowledge, FoodForKnowledge, TransportForKnowledge, Knowledge
from django.contrib.auth.models import User, Permission
from usuario.models import User as Profile

# Import views
from .views import CenterUpdateView, CenterCreateView, CenterListView, CenterDetailView, CreateKnowledge


def create_user():
    return User.objects.create_user(
        username='juliohurtado',
        first_name="Julio",
        last_name='Hurtado',
        email='juliohurtado@email.com',
        is_active=True,
        password='examplePass'
    )


def create_profile(user):
    return Profile.objects.create(
        user=user,
        has_add_center=True,
        reason_to_validate='Loremp insup'
    )


def create_center(profile):
    return Center.objects.create(
        name='Center Name',
        addres='-2.251579, -78.132993',
        aditional_information='Lorem ipsum dolor sit amet, consectetuer adipiscing elit.',
        user=profile,
    )


class HomeTestCase(TestCase):
    def setUp(self):
        self.url = reverse('Center:home')
        user = create_user()
        self.client = Client()

    def test_unlogged_user_can_view_home_page(self):
        response = self.client.get(self.url)
        view = resolve(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(view.func.view_class, CenterListView)

    def test_logged_user_can_view_home_page(self):
        self.client.login(username='juliohurtado', password='examplePass')
        self.test_unlogged_user_can_view_home_page()


class HomeFreeTestCase(HomeTestCase):
    def setUp(self):
        super(HomeTestCase, self).setUp()
        self.url = reverse('Center:home_free')


class CenterDetailTestCase(TestCase):
    def setUp(self):
        user = create_user()
        profile = create_profile(user)
        center = create_center(profile)
        self.url = reverse('Center:center_detail', kwargs={'slug': center.slug})
        self.client = Client()

    def test_unlogged_user_can_view_detail_center(self):
        response = self.client.get(self.url)
        view = resolve(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(view.func.view_class, CenterDetailView)

    def test_logged_user_can_view_detail_center(self):
        self.client.login(username='juliohurtado', password='examplePass')
        self.test_unlogged_user_can_view_detail_center()

    def test_detail_center_404(self):
        self.url = reverse('Center:center_detail', kwargs={'slug': 'errorslug'})
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 404)


class CenterCreateTestCase(TestCase):
    def setUp(self):
        user = create_user()
        self.profile = create_profile(user)
        self.permissions = Permission.objects.get(name='Puede Crear Centros Turísticos')
        self.client = Client()
        self.url = reverse('Center:center_create')

    def test_user_with_permission_can_create_center(self):
        self.client.login(username='juliohurtado', password='examplePass')
        self.profile.user.user_permissions.add(self.permissions)
        response = self.client.get(self.url)
        view = resolve(self.url)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(view.func.view_class, CenterCreateView)

    def test_user_without_permission_cant_create_center(self):
        self.client.login(username='juliohurtado', password='examplePass')
        response = self.client.get(self.url)
        view = resolve(self.url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(view.func.view_class, CenterCreateView)


class CenterUpdateTestCase(TestCase):
    def setUp(self):
        user = create_user()
        self.profile = create_profile(user)
        self.permissions = Permission.objects.get(name='Puede Crear Centros Turísticos')
        self.client = Client()
        self.center = create_center(self.profile)
        self.url = reverse('Center:center_edit')

    def test_user_with_created_can_edit_center_get(self):
        self.client.login(username='juliohurtado', password='examplePass')
        response = self.client.get(self.url)
        view = resolve(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, self.center.name)
        self.assertEquals(view.func.view_class, CenterUpdateView)

    def test_user_without_created_center_cant_edit_a_center(self):
        otheruser = User.objects.create_user(
            username='cesarjerves',
            first_name="Cesar",
            last_name='Jerves',
            email='cesarjerves@email.com',
            is_active=True,
            password='examplePass'
        )
        profile = Profile.objects.create(
            user=otheruser,
            has_add_center=True,
            reason_to_validate='Loremp insup'
        )
        self.client.login(username='cesarjerves', password='examplePass')
        response = self.client.get(self.url)
        view = resolve(self.url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(view.func.view_class, CenterUpdateView)

    def test_user_unlogged_cant_edit_center(self):
        response = self.client.get(self.url)
        view = resolve(self.url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(view.func.view_class, CenterUpdateView)

    def test_user_with_permission_can_edit_center_post(self):
        self.client.login(username='juliohurtado', password='examplePass')
        new_name = self.center.name + 'other.'
        data = {'name': new_name, 'addres': self.center.addres, 'aditional_information': self.center.aditional_information, }
        response = self.client.post(self.url, data=data)
        view = resolve(self.url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.wsgi_request._post['name'], new_name)


class KnowledgeCreateTestCase(TestCase):
    def setUp(self):
        user = create_user()
        self.profile = create_profile(user)
        self.center = create_center(self.profile)
        permissions = Permission.objects.get(name='Puede Crear Centros Turísticos')
        user.user_permissions.add(permissions)
        self.url = reverse('Center:knowledge_create')

    def test_create_knowledge_with_created_center(self):
        self.client.login(username='juliohurtado', password='examplePass')
        response = self.client.get(self.url)
        view = resolve(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, self.center.name)

    def test_create_knowledge_without_created_center(self):
        response = self.client.get(self.url)
        view = resolve(self.url)
        self.assertEquals(response.status_code, 302)


class KnowledgeUpdateTestCase(KnowledgeCreateTestCase):
    def setUp(self):
        self.url = reverse('Center:knowledge_update')
        super(KnowledgeUpdateTestCase, self).setUp()


class PollTestCase(TestCase):
    def setUp(self):
        user = create_user()
        self.profile = create_profile(user)
        self.center = create_center(self.profile)
        self.url = reverse('Center:encuesta')

    def test_user_can_view_test_get(self):
        self.client.login(username='juliohurtado', password='examplePass')
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Conformación del grupo de Turistas")
        self.assertContains(response, "Actividades que desea desarrollar")
        self.assertContains(response, "Método de transporte preferido")
        self.assertContains(response, "Comida preferida")
        self.assertContains(response, "Dinero máximo por persona")

    def test_user_can_view_test_post(self):
        self.client.login(username='juliohurtado', password='examplePass')
        response = self.client.get(self.url)
        view = resolve(self.url)
        self.client.login(username='juliohurtado', password='examplePass')

        self.activity = ActivityForKnowledge.objects.create(name='Actividad 1')
        self.group = GroupTypeForKnowledge.objects.create(name='Group 1')
        self.food = FoodForKnowledge.objects.create(name='Food 1')
        self.transport = TransportForKnowledge.objects.create(name='Transport 1')

        self.knowledge = Knowledge.objects.create(center=self.center, money_per_person=10)
        self.knowledge.activities.add(self.activity)
        self.knowledge.group_type.add(self.group)
        self.knowledge.food.add(self.food)
        self.knowledge.transport.add(self.transport)

        data = {
            'group_type': self.group.id,
            'activity': self.activity.id,
            'transport': self.transport.id,
            'food': self.food.id,
            'money_per_people': self.knowledge.money_per_person,
        }
        response = self.client.post(self.url, data=data)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response._headers['location'][1], '/encuesta/1/')
        response2 = self.client.get(response._headers['location'][1])
        self.assertEquals(response2.status_code, 200)
        self.assertContains(response2, "El sistema le recomienda visitar el destino turístico Center Name")

    def test_not_authenticated_user_cant_view_test(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)
