import asyncio
import os

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from models import User, Role, Job, Application
from security import get_password_hash

async def main():
    try:
        client = AsyncIOMotorClient("mongodb+srv://codemasters:codeMastersPass@intellihire.mroevwy.mongodb.net/?retryWrites=true&w=majority&appName=intellihire")
        await init_beanie(
            database=client.intellihire,
            document_models=[User, Job, Application]
        )

        admin_user = User(
            full_name="Test Admin",
            email="test@admin.com",
            hashed_password=get_password_hash("adminpassword"),
            role=Role.ADMIN
        )

        await admin_user.insert()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    asyncio.run(main())

        