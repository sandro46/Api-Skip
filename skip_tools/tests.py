from skip_tools.models import Task
from rest_framework.test import APIClient
import pytest

client = APIClient()



# If your tests need to use the database and want to use pytest
# function test approach, you need to `mark` it.
@pytest.mark.django_db
def test_get_tasks_returns_json_with_tasks():
    response = client.get('/tasks')
    assert response.status_code == 200
