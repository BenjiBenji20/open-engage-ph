from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import shutil
import os

from app.db.db_session import get_async_db
from app.utils.db_look_up_utils import upload_photo

upload_router = APIRouter(prefix="/photos", tags=["Upload photos"])

UPLOAD_DIR = "uploads/"  # Or use S3 later
os.makedirs(UPLOAD_DIR, exist_ok=True)

@upload_router.post("/upload/profile")
async def upload_profile_photo(
  user = Depends(get_current_user),
  file: UploadFile = File(...),
  db: AsyncSession = Depends(get_async_db)
):
  try:
    filepath = os.path.join(UPLOAD_DIR, file.filename)
    with open(filepath, "wb") as buffer:
      shutil.copyfileobj(file.file, buffer)

    # Collect metadata
    file_url = f"/{UPLOAD_DIR}{file.filename}"  # later -> S3 URL
    file_size = os.path.getsize(filepath)
    mime_type = file.content_type

    # Fetch user (example for EndUser)
    user = await db.get(user, user.id)
    
    if not user:
      raise HTTPException(status_code=404, detail="User not found")

    # Save photo record
    photo = await upload_photo(
      db=db,
      user=user,
      filename=file.filename,
      file_url=file_url,
      file_size=file_size,
      mime_type=mime_type,
      is_profile_photo=True
    )

    return {"photo_id": photo.id, "file_url": photo.file_url} # create response schema for clean response 

  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
