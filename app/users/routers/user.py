from fastapi import APIRouter

router = APIRouter()


@router.post("/signup")
async def create_user():
    return "hello world"
