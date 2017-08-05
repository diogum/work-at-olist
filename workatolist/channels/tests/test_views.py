from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from ..utils import create_channel, create_category_in_channel


class CategoryViewTestCase(APITestCase):
    """CategoryView tests"""

    def test__list(self):
        """Test the list endpoint"""
        channel = create_channel('Channel')
        create_category_in_channel('Category A', channel=channel)
        create_category_in_channel('Category B', channel=channel)

        url = reverse('api:categories-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 2)

    def test__detail_not_found(self):
        """Must return not found if the requested resource does not exists"""
        url = reverse('api:categories-detail', kwargs={'reference_id': 'channel-books'})
        response = self.client.get(url)
        expected_data = {'detail': 'Not found.'}

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, expected_data)

    def test__detail_found(self):
        """Must return the requested resource"""
        channel = create_channel('Channel')
        create_category_in_channel('Books', channel=channel)
        url = reverse('api:categories-detail', kwargs={'reference_id': 'channel-books'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 6)


class ChannelViewTestCase(APITestCase):
    """ChannelView tests"""

    def test__list(self):
        """Test the list endpoint"""
        create_channel('Channel A')
        create_channel('Channel B')

        url = reverse('api:channels-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 2)

    def test__detail_not_found(self):
        """Must return not found if the requested resource does not exists"""
        url = reverse('api:channels-detail', kwargs={'reference_id': 'channel'})
        response = self.client.get(url)
        expected_data = {'detail': 'Not found.'}

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, expected_data)

    def test__detail_found(self):
        """Must return the requested resource"""
        create_channel('Channel')
        url = reverse('api:channels-detail', kwargs={'reference_id': 'channel'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
