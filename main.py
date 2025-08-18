from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import shutil
import os
import joblib
from fastapi.responses import JSONResponse
from ultralytics import YOLO
from src.process_image import process_image_v2

app = FastAPI()
if os.path.exists("static") is False:
    os.makedirs("static")
    os.makedirs("static/uploads")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "image_url": None, "processed_url": None})


@app.post("/upload", response_class=HTMLResponse)
async def upload_image(request: Request, file: UploadFile = File(...)):
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        os.remove(file_path)
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
    image_paths, suggestion, status, sudoku_digitalized = process_image_v2(input_path, model_cnn, model_yolo)
    print(status)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "image_url": f"/static/uploads/{image_name}",
        "processed_url": None,
        "graph_paths": image_paths,
        "suggestion": suggestion
    })

@app.post("/api/suggestion")
async def api_suggestion(file: UploadFile = File(...)):
    # Guardar imagen temporalmente
    file_ext = file.filename.split(".")[-1].lower()
    if file_ext not in ["jpg", "jpeg", "png"]:
        return JSONResponse(content={"error": "Formato no soportado"}, status_code=400)

    temp_filename = f"temp_{file.filename}"
    image_path = os.path.join(UPLOAD_FOLDER, temp_filename)

    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Ejecutar el procesamiento de imagen
        image_paths, suggestion, status, sudoku_digitalized = process_image_v2(image_path, model_cnn, model_yolo)

        # Eliminar imagen y gráficos generados si se desea
        for filename in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            os.remove(file_path)

        return JSONResponse(content={
            "suggestion": suggestion,
            "status": status,
            "sudoku_digitalized": sudoku_digitalized,
        })
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
