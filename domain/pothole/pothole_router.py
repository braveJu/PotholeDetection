from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from starlette import status

from database import SessionLocal, get_db
from domain.pothole import pothole_shema

from ultralytics import YOLO
from PIL import Image
import io
import torch
from torchvision import transforms


def load_yolo_model():
    model = YOLO('best.pt')
    return model

def byte_to_pil(image_bytes: bytes) -> Image.Image:
    image = Image.open(io.BytesIO(image_bytes))
    return image


def pil_to_tensor(image: Image.Image) -> torch.Tensor:
    transform = transforms.Compose([transforms.ToTensor(), transforms.Resize((640,640))])  # ToTensor 변환을 사용
    tensor = transform(image)
    return tensor


DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
Model = load_yolo_model().to(DEVICE)

router = APIRouter(
    prefix="/api/pothole",
)


@router.post('/road_image', status_code=status.HTTP_201_CREATED)
async def check_pothole(file:UploadFile = File(...), db:Session=Depends(get_db)):
    try:
        cnt = 0
        bbox_list = []
        content = await file.read()
        img_tensor = pil_to_tensor(byte_to_pil(content)).to(DEVICE)

        results = Model(img_tensor)
        for result in results:
            boxes = result.boxes
            bbox_list.append(boxes.xyxy)
            print(bbox_list)
            
        return {'result': len(bbox_list)}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="파일이 잘못되었습니다.")
    