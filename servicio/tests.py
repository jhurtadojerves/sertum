from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.urls import resolve

# Import models

from .models import Service
from centro.models import ServiceCenter

from django.contrib.auth.models import Permission

from centro.tests import create_center, create_profile, create_user


class ServiceListTestCase(TestCase):
    def setUp(self):
        self.user = create_user()
        self.profile = create_profile(self.user)
        self.center = create_center(self.profile)
        self.url = reverse('Service:service_list')
        self.services = (
            Service.objects.create(name='Servicio 1'),
            Service.objects.create(name='Servicio 2'),
            Service.objects.create(name='Servicio 3'),
            Service.objects.create(name='Servicio 4'),
            Service.objects.create(name='Servicio 5'),
        )

    def test_anonymous_user_can_see_services_list(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        for service in self.services:
            self.assertContains(response, service.name)

    def test_logued_user_can_see_services_list(self):
        self.client.login(username='juliohurtado', password='examplePass')
        self.test_anonymous_user_can_see_services_list()


class CenterListWithServiceTestCase(TestCase):
    def setUp(self):
        self.user = create_user()
        self.profile = create_profile(self.user)
        self.center = create_center(self.profile)
        self.service = Service.objects.create(name='Piscinas')
        self.url = reverse('Service:center_service_list', kwargs={'slug': self.service.slug})

    def test_anonymous_user_can_see_centers_list_with_a_service(self):
        ServiceCenter.objects.create(center=self.center, service=self.service, cost=25,
                                     observation='Generic Observation')
        response = self.client.get(self.url)
        self.assertContains(response, self.center.name)

    def test_user_can_see_centers_list_with_a_service(self):
        self.client.login(username='juliohurtado', password='examplePass')
        self.test_anonymous_user_can_see_centers_list_with_a_service()


class CreateServiceTestCase(TestCase):
    def setUp(self):
        self.user = create_user()
        self.profile = create_profile(self.user)
        self.center = create_center(self.profile)
        self.service = Service.objects.create(name='Piscinas')
        self.url = reverse('Service:service_create')
        self.permissions = Permission.objects.get(name='Puede Crear Centros Turísticos')

    def test_user_without_permission_cant_create_user(self):
        self.client.login(username='juliohurtado', password='examplePass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  # Redirige al login

    def test_user_with_permission_can_create_user_get(self):
        self.client.login(username='juliohurtado', password='examplePass')
        self.profile.user.user_permissions.add(self.permissions)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Crear servicios')

    def test_user_with_permission_can_create_user_post(self):
        self.client.login(username='juliohurtado', password='examplePass')
        self.profile.user.user_permissions.add(self.permissions)
        data = {
            'service': self.service.id,
            'cost': 10,
            'observation': 'Generic Observation'
        }
        response = self.client.post(self.url, data=data)
        self.assertContains(response)
