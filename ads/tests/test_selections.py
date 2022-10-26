import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.utils import json


@pytest.mark.django_db
def test_create_selection(api_client, user, ad):
    data = {
        'name': 'Fmccccccccccccc',
        'owner': user.id,
        'items': [ad.id],
    }
    url = reverse('selection_create')
    res = api_client.post(
        url,
        data=json.dumps(data),
        content_type='application/json',
    )
    res_data = res.json()
    assert res.status_code == status.HTTP_201_CREATED
    assert res_data['name'] == data['name']
    assert res_data['owner'] == data['owner']
