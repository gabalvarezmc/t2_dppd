from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PIL import Image
import shutil
import os
import joblib
from ultralytics import YOLO
from src.process_image import process_image_v2

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "image_url": None, "processed_url": None})


@app.post("/upload", response_class=HTMLResponse)
async def upload_image(request: Request, file: UploadFile = File(...)):
    image_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "image_url": f"/static/uploads/{file.filename}",
        "processed_url": None
    })

model_yolo = YOLO("models/yolo_best.pt")
model_cnn = joblib.load("models/model_cnn_numbers.joblib")

@app.post("/process", response_class=HTMLResponse)
async def process(request: Request, image_name: str = Form(...)):
    input_path = os.path.join(UPLOAD_FOLDER, image_name)
    image_paths, suggestion, status = process_image_v2(input_path, model_cnn, model_yolo)
    print(status)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "image_url": f"/static/uploads/{image_name}",
        "processed_url": None,
        "graph_paths": image_paths,
        "suggestion": suggestion
    })

# @app.post("/process", response_class=HTMLResponse)
# async def process_image(request: Request, image_name: str = Form(...)):
#     input_path = os.path.join(UPLOAD_FOLDER, image_name)
#     output_path = os.path.join(UPLOAD_FOLDER, f"processed_{image_name}")

#     # Procesamiento: convertir a escala de grises
#     img = Image.open(input_path).convert("L")
#     img.save(output_path)

#     return templates.TemplateResponse("index.html", {
#         "request": request,
#         "image_url": f"/static/uploads/{image_name}",
#         "processed_url": f"/static/uploads/processed_{image_name}"
#     })
