from .utils import get_image_from_bytes, detect_sample_model, add_bboxs_on_img, get_bytes_from_image
from fastapi import APIRouter, File, Depends, Header
from fastapi.responses import StreamingResponse
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from auth.auth import get_current_user
from .utils import log_task_history
from sqlalchemy.orm import Session
from auth.models import User
from database import get_db
from typing import Optional
from loguru import logger

router = APIRouter(
    prefix="/image",
    tags=["Image"]
)


@router.post("/img_object_detection_to_json")
def img_object_detection_to_json(
    file: bytes = File(...),
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None)
):
    result = {'detect_objects': None}

    input_image = get_image_from_bytes(file)

    predict = detect_sample_model(input_image)

    detect_res = predict[['name', 'confidence']]
    objects = detect_res['name'].values

    result['detect_objects_names'] = ', '.join(objects)
    result['detect_objects'] = detect_res.to_dict(orient='records')

    if authorization:
        try:
            token = authorization.split(" ")[1] if " " in authorization else authorization
            user = get_current_user(token,db)
            if user:

                log_task_history(user.id, dict(result), db)
            else:
                raise HTTPException(status_code=401, detail="Invalid authentication token")
        except Exception as e:
            logger.error(f"Token processing failed: {e}")
            raise HTTPException(status_code=401, detail="Invalid authentication token")
    
    logger.info("results: {}", result)
    return JSONResponse(content=result)


@router.post("/img_object_detection_to_img")
def img_object_detection_to_img(file: bytes = File(...)):

    input_image = get_image_from_bytes(file)

    predict = detect_sample_model(input_image)

    final_image = add_bboxs_on_img(image=input_image, predict=predict)

    return StreamingResponse(content=get_bytes_from_image(final_image), media_type="image/jpeg")