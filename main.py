from fastapi import Depends, FastAPI, File, Query, Request, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from fastapi import File, UploadFile, Form
from db.database import get_db
from db import api_functions
from flask import request, redirect, url_for
from db.api_functions import *
# FastAPI Framework Instance
app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.put("/slider")
async def insert_slider(slide_name: str = Form(None),slide_type: str = Form(None),expiry_date: str = Form(None),file = Form(...), db: Session = Depends(get_db)):
    try:
        # Read the file content in binary mode
        file_content = await file.read()

        # Pass the file content along with other details to the slider_insertion function
        new_slider = api_functions.slider_insertion(db, slide_name, slide_type, expiry_date, file_content)
        return JSONResponse(content={"message": "Slider inserted successfully", "id": new_slider.id})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/slider")
async def get_slider(db: Session = Depends(get_db)):
    try:
        result=api_functions.get_all_sliders(db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
# Uvicorn server instance to run the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)