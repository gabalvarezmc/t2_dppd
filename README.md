# 🧠 Sugeridor de técnicas de resolución de Sudoku

Este proyecto implementa una aplicación basada en **FastAPI** que permite subir imágenes de tableros de Sudoku, detectarlos mediante **YOLOv8**, reconocer los dígitos con una red **CNN**, y entregar una sugerencia sobre la técnica avanzada que podría aplicarse para continuar resolviendo el Sudoku.

---

## 📖 Descripción

El sistema permite a los usuarios cargar una imagen de un tablero de Sudoku (tomada desde papel, pantalla u otro medio) y realiza el siguiente procesamiento:

1. **Detección del tablero** usando un modelo **YOLOv8 personalizado**.
2. **Transformación de perspectiva** y preprocesamiento de la imagen para segmentar cada celda del tablero.
3. **Clasificación de los números** usando un modelo **CNN entrenado** para reconocer dígitos escritos.
4. **Construcción de la grilla digitalizada** del Sudoku.
5. **Sugerencia de técnica avanzada de resolución** (como XY-Wing, Intersección línea-región, etc.).

Además, se generan visualizaciones intermedias del proceso (detección, contornos, transformación y tablero digitalizado) que se muestran en la aplicación web.

También se expone una API para recibir imágenes y retornar los resultados en formato JSON, útil para integraciones externas.

---

## 🛠 Tecnologías

- Python 3.12.7
- fastapi==0.116.1
- uvicorn==0.35.0
- pydantic==2.11.7
- pillow==11.3.0
- Jinja2==3.1.6
- python-multipart==0.0.20
- numpy==2.1.3
- opencv-python==4.12.0.88
- ultralytics==8.3.173
- matplotlib==3.10.5
- joblib==1.5.1
- scikit-learn==1.7.1
- keras==3.11.1
- tensorflow==2.19.0

---

## 📦 Instalación

1. Clona el repositorio:
   bash
   git clone https://github.com/gabalvarezmc/t2_dppd
   cd sudoku-solver-web

2. Crea y activa un entorno virtual
    python -m venv .venv
    .venv\Scripts\activate

3. Instala las dependencias:
    pip install -r requirements.txt

4. Asegúrate de que existan los siguientes archivos en la carpeta models/:
    yolo_best.pt: modelo entrenado para detección de tableros.
    model_cnn_numbers.joblib: modelo CNN para reconocimiento de dígitos.

## ▶️ Uso
### 🌐 Interfaz web

1. Inicia el servidor:
    uvicorn main:app --reload

2. Abre tu navegador en:
    http://localhost:8000

3. Sube una imagen de un Sudoku y presiona "Procesar" para ver los gráficos intermedios y la sugerencia de técnica.

### 🧪 API REST para Postman u otras apps
Endpoint:
    POST /api/suggestion
Parámetros:

file: imagen del Sudoku (form-data)

Ejemplo en Postman:

Método: POST

URL: http://localhost:8000/api/suggestion

Body: form-data

Key: file (tipo: File)

Value: selecciona una imagen .jpg o .png

{
  "suggestion": "XY-Wing",
  "status": "ok",
  "sudoku_digitalized": "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
}


## 💡 Estructura del proyecto
sudoku-solver-web/
├── main.py
├── requirements.txt
├── static/
│   └── uploads/
├── templates/
│   └── index.html
├── models/
│   ├── yolo_best.pt
│   └── model_cnn_numbers.joblib
├── src/
│   ├── process_image.py
│   └── sudoku_solver/
│       └── main.py
