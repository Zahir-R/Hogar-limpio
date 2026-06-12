from fastapi import APIRouter, Depends, UploadFile, File
from models.schemas import UserSignup, ProfileUpdate
from services.user_service import UserService
from shared.auth import get_current_user

router = APIRouter(tags=["auth"])
user_service = UserService()


@router.get("/users/me")
async def read_user_me(user: dict = Depends(get_current_user)):
    return {"uid": user["uid"], "email": user.get("email"), "role": user.get("role")}


@router.post("/users/signup-sync")
async def sync_user(data: UserSignup):
    return user_service.sync_user(data)


@router.get("/api/users/profile")
async def get_profile(current_user: dict = Depends(get_current_user)):
    return user_service.get_profile(current_user["uid"])


@router.put("/api/users/profile")
async def update_profile(data: ProfileUpdate, current_user: dict = Depends(get_current_user)):
    return user_service.update_profile(current_user["uid"], data)


@router.post("/api/users/profile/photo")
async def upload_profile_photo(file: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    return await user_service.upload_photo(current_user["uid"], file)
