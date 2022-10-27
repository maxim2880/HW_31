import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.utils import json


@pytest.mark.django_db
def test_create_ad(api_client, user, ad):
    data = {
        'name': 'Fmcccccccccccc',
        'author': user.id,
        'price': 1,
    }
    url = reverse('ad_create')
    res = api_client.post(
        url,
        data=json.dumps(data),
        content_type='application/json',
    )
    res_data = res.json()
    assert res_data['name'] == data['name']
    assert res_data['price'] == data['price']
    assert res_data['author'] == data['author']


@pytest.mark.django_db
def test_list_ads(api_client, ad):
    url = reverse('ad_list')
    res = api_client.get(url)
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_ad_by_id(api_client, ad):
    url = reverse('ad_detail', kwargs={'pk': ad.id})
    res = api_client.get(url)
    assert res.status_code == status.HTTP_200_OK
    assert res.json()['id'] == ad.id
