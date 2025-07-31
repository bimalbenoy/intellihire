from fastAPI import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

app=FastAPI()
@app.on_event("startup")
async def app_init():

    client=AsyncIOMotorClient("mongodb+srv://codemasters:codeMastersPass@intellihire.mroevwy.mongodb.net/?retryWrites=true&w=majority&appName=intellihire")

    await init_beanie(database=client.intellihire, document_models=[User, Job, Application])