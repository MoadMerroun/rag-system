from fastapi import APIRouter

routers = APIRouter()

@routers.post( "/upload" )
async def upload():
    return { "message": "Upload endpoint" }
