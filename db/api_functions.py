import base64
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from .models import *
from datetime import datetime
from sqlalchemy import func, text
from loguru import logger
import json
from sqlalchemy import desc
import boto3, botocore
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import os
import tempfile

aws_access_key_id = os.getenv('AWS_ACCESS_KEY')
aws_secret_access_key = os.getenv('AWS_SECRET_KEY')
s3 = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

load_dotenv()
def allowed_file(filename: str):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif','mp4'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




def slider_insertion(db: Session,slide_name,slide_type,expiry_date,file_content):
    new_Slider = Slider(
        slide_name=slide_name,
        slide_type=slide_type,
        expiry_date=expiry_date,
        content=file_content  # Insert the binary content into the 'content' field
    )
    
    db.add(new_Slider)
    db.commit()
    db.refresh(new_Slider)
    return new_Slider

def get_all_sliders(db: Session):
    all_sliders = db.query(Slider).order_by(Slider.id).all()
    slider_Array=[]
    for slider in all_sliders:
        encoded_content=base64.b64encode(slider.content).decode("utf-8")
        image_content = f"data:image/jpeg;base64,{encoded_content}"
        slider_data={
            "id":slider.id,
            "slide_name":slider.slide_name,
            "slide_type":slider.slide_type,
            "expiry_date":slider.expiry_date,
            "content":image_content
        }
        slider_Array.append(slider_data)
    return slider_Array 
