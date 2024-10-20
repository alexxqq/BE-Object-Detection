from ultralytics.yolo.utils.plotting import Annotator, colors
from task.models import TaskResult, Task
from sqlalchemy.orm import Session
from ultralytics import YOLO
from loguru import logger
from PIL import Image
import pandas as pd
import numpy as np
import io


model_sample_model = YOLO("./models/yolov8n.pt")


def get_image_from_bytes(binary_image: bytes) -> Image:

    input_image = Image.open(io.BytesIO(binary_image)).convert("RGB")
    return input_image


def get_bytes_from_image(image: Image) -> bytes:

    return_image = io.BytesIO()
    image.save(return_image, format='JPEG', quality=85)
    return_image.seek(0)
    return return_image

def transform_predict_to_df(results: list, labeles_dict: dict) -> pd.DataFrame:

    predict_bbox = pd.DataFrame(results[0].to("cpu").numpy().boxes.xyxy, columns=['xmin', 'ymin', 'xmax','ymax'])

    predict_bbox['confidence'] = results[0].to("cpu").numpy().boxes.conf

    predict_bbox['class'] = (results[0].to("cpu").numpy().boxes.cls).astype(int)

    predict_bbox['name'] = predict_bbox["class"].replace(labeles_dict)
    return predict_bbox

def get_model_predict(model: YOLO, input_image: Image, save: bool = False, image_size: int = 1248, conf: float = 0.5, augment: bool = False) -> pd.DataFrame:

    predictions = model.predict(
                        imgsz=image_size, 
                        source=input_image, 
                        conf=conf,
                        save=save, 
                        augment=augment,
                        flipud= 0.0,
                        fliplr= 0.0,
                        mosaic = 0.0,
                        )
    
    predictions = transform_predict_to_df(predictions, model.model.names)
    return predictions


def add_bboxs_on_img(image: Image, predict: pd.DataFrame()) -> Image:

    annotator = Annotator(np.array(image))

    predict = predict.sort_values(by=['xmin'], ascending=True)


    for i, row in predict.iterrows():

        text = f"{row['name']}: {int(row['confidence']*100)}%"

        bbox = [row['xmin'], row['ymin'], row['xmax'], row['ymax']]

        annotator.box_label(bbox, text, color=colors(row['class'], True))

    return Image.fromarray(annotator.result())


def detect_sample_model(input_image: Image) -> pd.DataFrame:

    predict = get_model_predict(
        model=model_sample_model,
        input_image=input_image,
        save=False,
        image_size=640,
        augment=False,
        conf=0.5,
    )
    return predict
def log_task_history(user_id: int, task_data: dict, db: Session):

    detected_objects = task_data.get("detect_objects", [])
    
    new_task = Task(
        task_id=task_data.get("task_id"),
        status=task_data.get("status"),
        user_id=user_id,
    )
    
    db.add(new_task)
    db.commit()

    for obj in detected_objects:
        name = obj.get('name', 'Unknown')
        confidence = obj.get('confidence', 0)

        new_result = TaskResult(
            task_id=new_task.id,
            name=name,
            confidence=round(confidence,4)
        )
        
        db.add(new_result)

    db.commit()


def crop_image_by_predict(image: Image, predict: pd.DataFrame(), crop_class_name: str) -> Image:

    crop_predicts = predict[(predict['name'] == crop_class_name)]

    if crop_predicts.empty:
        raise HTTPException(status_code=400, detail=f"{crop_class_name} not found in photo")

    if len(crop_predicts) > 1:
        crop_predicts = crop_predicts.sort_values(by=['confidence'], ascending=False)

    crop_bbox = crop_predicts[['xmin', 'ymin', 'xmax','ymax']].iloc[0].values
    img_crop = image.crop(crop_bbox)
    return img_crop
