import os

from typing import List
from typing import Optional

from sqlalchemy.orm import Session

from fastapi import Depends
from fastapi import Query
from fastapi import Body
from fastapi import HTTPException
from fastapi import UploadFile
from fastapi import File
from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.models.Videos import Videos

from app.db.database import get_db

from app.schemas import schemas

from fastapi.logger import logger

#  Initialize router
router = APIRouter()



################################################ START OF VIDEO APIs ######################################################

# API for starting segmentation on a video
@router.post("/start-segmentation", response_model=schemas.VideoRead, status_code=201)
def start_segmentation(VideoCreate: schemas.VideosCreate = Body(...), db: Session = Depends(get_db)):
    db_return = Videos.create_entry(db, Videos.video_id)
    if db_return:
        raise HTTPException(status_code=400, detail="Video with same ID is already present")
    return Videos.create_entry(db=db, code=VideoCreate)


# API for getting all video ids (limit 100)
@router.get("/get-all-video-details", response_model=List[schemas.VideoRead])
def read_all_videos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_return = Videos.get_videos(db, skip=skip, limit=limit)
    return db_return


# API for getting a video detail by id
@router.get("/get-details-by-id/{vid}")
def read_video_details_by_id(vid: str, db: Session = Depends(get_db)):
    db_return = Videos.get_video_by_id(db, code=vid)
    logger.debug(f"User with first name received - {vid}")
    if db_return is None:
        raise HTTPException(status_code=404, detail="Video details not found")
    return db_return


# API for getting a video status by id
@router.get("/get-status-by-id/{vid}")
def read_video_status_by_id(vid: str, db: Session = Depends(get_db)):
    return {
        "msg" : "Video analysis ongoing",
        "status" : "Analysing Segments",
        "completion" : "50%"
    }


# API for getting a video status by id
@router.get("/get-analysis-results/{vid}")
def get_video_analysis_results(vid: str, db: Session = Depends(get_db)):
    return {
   "videoUrl": "https://cloudfront.mp4",
   "assetType": "poster | frame | 3dcan",
   "assetFileUrl": "https://cloudfront/boldr.png",
   "assetPosition": ["x", "y", "z"],
   "postEffects": [
     {
       "lighting": {
         "type": "point | directional | spotlight",
         "color": ["r", "g", "b", "a"],
         "intensity": "Light_intensity_value",
         "position": ["x", "y", "z"],
         "rotation": ["x", "y", "z"],
         "range": "range_value",
         "shadow": {
           "type": "hard | soft | none",
           "strength": "shadow_strength_value"
         }
       }
     }
   ],
   "globalVolume": {
     "colorAdjustments": {
       "hueShift": "hue_shift_value",
       "saturation": "saturation_value",
       "contrast": "contrast_value"
     }
   }
 }


# API to stop a video analysis by code value
@router.post("/stop-segmentation/{vid}")
def stop_video_analysis(vid: str, db:Session = Depends(get_db)):
    return {"msg" : "Video analysis stopped"}

     
################################################# END OF CODE APIs #######################################################