import asyncio

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import engine, Base
from app.main import app
from app.models.company_model import Company
from app.models.user_model import User


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def test_client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture(autouse=True, scope='session')
async def create_test_database():
    test_user_data_1 = {
        "user_email": "test@test.com",
        "hashed_password": "$2b$05$N9H7SJ72n0QZXSbwsduiIuHvFybPbapD9tM1o1vkqKSbg5VokRD4S",
        "user_firstname": "Test",
        "user_lastname": "User",
        "user_city": "User",
        "user_phone": "+44 7911 123456",
        "user_avatar": "User",
    }

    test_user_data_2 = {
        "user_email": "test_two@test.com",
        "hashed_password": "$2b$05$N9H7SJ72n0QZXSbwsduiIuHvFybPbapD9tM1o1vkqKSbg5VokRD4S",
        "user_firstname": "Test",
        "user_lastname": "User",
        "user_city": "User",
        "user_phone": "User",
        "user_avatar": "User",
    }

    test_company_data = {
        "company_owner_id": 1,
        "company_name": "string",
        "company_title": "string",
        "company_description": "string",
        "company_city": "string",
        "company_phone": "string",
        "company_links": "string",
        "company_avatar": "string"
    }

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine) as session:
        test_user = User(**test_user_data_1)
        test_user_two = User(**test_user_data_2)
        test_company = Company(**test_company_data)
        session.add(test_user)
        session.add(test_user_two)
        await session.commit()
        session.add(test_company)
        await session.commit()

    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
