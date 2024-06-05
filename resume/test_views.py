import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Resume

pytestmark = pytest.mark.django_db(transaction=True)


@pytest.mark.asyncio
async def test_get_all_resume():
    client = APIClient()
    response = await client.get('/api/resumes/')
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_resume():
    client = APIClient()
    user = await User.objects.create_user(username='testuser', password='password')
    token = await Token.objects.create(user=user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    
    data = {
        "user": user.id,
        "company": "Test Company",
        "school": "Test School",
        "college": "Test College",
        "achievement": "Test Achievement",
        "hobbies": "Test Hobbies"
    }
    
    response = await client.post('/api/resumes/', data, format='json')
    assert response.status_code == 201
    assert response.data['company'] == "Test Company"


@pytest.mark.asyncio
async def test_get_specific_resume():
    client = APIClient()
    user = await User.objects.create_user(username='testuser', password='password')
    resume = await Resume.objects.create(
        user=user, company="Test Company", school="Test School", college="Test College", 
        achievement="Test Achievement", hobbies="Test Hobbies"
    )
    
    response = await client.get(f'/api/resumes/{resume.id}/')
    assert response.status_code == 200
    assert response.data['company'] == "Test Company"


@pytest.mark.asyncio
async def test_update_resume():
    client = APIClient()
    user = await User.objects.create_user(username='testuser', password='password')
    resume = await Resume.objects.create(
        user=user, company="Test Company", school="Test School", college="Test College", 
        achievement="Test Achievement", hobbies="Test Hobbies"
    )
    
    data = {
        "company": "Updated Company",
        "school": "Updated School",
        "college": "Updated College",
        "achievement": "Updated Achievement",
        "hobbies": "Updated Hobbies"
    }
    
    response = await client.put(f'/api/resumes/{resume.id}/', data, format='json')
    assert response.status_code == 202
    assert response.data['company'] == "Updated Company"


@pytest.mark.asyncio
async def test_delete_resume():
    client = APIClient()
    user = await User.objects.create_user(username='testuser', password='password')
    resume = await Resume.objects.create(
        user=user, company="Test Company", school="Test School", college="Test College", 
        achievement="Test Achievement", hobbies="Test Hobbies"
    )
    
    response = await client.delete(f'/api/resumes/{resume.id}/')
    assert response.status_code == 204
