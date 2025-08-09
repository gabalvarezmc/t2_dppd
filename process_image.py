import joblib
import matplotlib.pyplot as plt
import cv2
import time
import numpy as np
from ultralytics import YOLO
from PIL import Image
from sudoku_solver.main import SudokuBoard, suggest_technique
import uuid
import os


def save_figure(fig):
    filename = f"{uuid.uuid4().hex}.png"
    path = os.path.join("static/uploads", filename)
    fig.savefig(path)
    plt.close(fig)
    return f"/static/uploads/{filename}"


# Se utiliza para dibujar el tablero Sudoku digitalizado
def dibujar_sudoku(sudoku):
    fig, ax = plt.subplots(figsize=(6, 6))
    # Se establece el fondo blanco
    ax.set_facecolor('white')
    # Se dibujan las líneas del tablero. Cada 3 líneas se dibuja una línea más gruesa.
    for i in range(10):
        grosor_linea = 0.5
        if i % 3 == 0:
            grosor_linea = 2
        ax.axhline(i, color='black', lw=grosor_linea)
        ax.axvline(i, color='black', lw=grosor_linea)

    # Se dibujan los números del tablero
    for i in range(9):
        for j in range(9):
            num = sudoku[i][j]
            if num == 0:
                continue
            ax.text(j + 0.5, 8.5 - i, str(num), va='center', ha='center', fontsize=16)

    # Se establecen los límites del gráfico y se eliminan los ticks
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 9)
    ax.set_xticks([])
    ax.set_yticks([])
    plt.tight_layout()
    plt.show()

def process_image_v2(path_image, model_cnn, model_yolo, bool_is_sudoku, show_graphs=False):
    # Se mide el tiempo de inicio de ejecución
    timestart = time.time()

    # Se lee la imagen y se redimensiona a 450x450 píxeles
    img_tablero_base = cv2.imread(f"{path_image}.jpg")
    img_tablero_base = cv2.resize(img_tablero_base, (450, 450))
    
    # Se aplica BGR to RGB para que el modelo YOLO pueda procesar la imagen correctamente y se convierte a un objeto PIL
    image_rgb = cv2.cvtColor(img_tablero_base, cv2.COLOR_BGR2RGB)
    image_array = Image.fromarray(image_rgb)
    
    # Se utiliza el modelo YOLOv8 para detectar el tablero de Sudoku en la imagen
    results_yolo = model_yolo.predict(source=image_array, conf=0.25, save=False, save_txt=False, save_conf=False, verbose=False)
    # Se obtiene la lista de probabilidades de detección
    results_probababilities = results_yolo[0].boxes.conf.cpu().numpy()
    # Si no se detecta ningún tablero de Sudoku o si la probabilidad es menor a 0.7, se retorna 0.0
    probability_list = []
    for probability in results_probababilities:
        if probability >= 0.7:
            probability_list.append(probability)
    if not probability_list:
        timeend = time.time()
        seconds_execution = timeend - timestart
        return 0.0, seconds_execution, bool_is_sudoku==False
    # Si la imágen ingresada no debería ser un Sudoku, se retorna 0.0
    if not bool_is_sudoku:
        timeend = time.time()
        seconds_execution = timeend - timestart
        return 0.0, seconds_execution, False

    # Se convierte la imagen a escala de grises
    img_gray = cv2.cvtColor(img_tablero_base, cv2.COLOR_BGR2GRAY) 
    # Se aplica un filtro de desenfoque gaussiano para reducir el ruido
    img_blur = cv2.GaussianBlur(img_gray, (3, 3), 6) 
    # Se aplica umbral adaptativo para mejorar la detección de bordes
    img_tablero_mod = cv2.adaptiveThreshold(img_blur, 255, 1, 1, 11, 2)

    # Se encuentran los contornos en la imagen
    tablero_contours, hierarchy = cv2.findContours(img_tablero_mod, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Se ordenan de mayor a menor los contornos según su área para elegir el más grande 
    sorted_contours = sorted(tablero_contours, key=cv2.contourArea, reverse=True)
    for contour in sorted_contours:
        # Encuentra el perímetro del contorno y lo aproxima a un polígono
        perimetro = cv2.arcLength(contour, True)
        # Se aproxima el contorno a un polígono con 4 puntos
        biggest_contour = cv2.approxPolyDP(contour, 0.02 * perimetro, True)
        # Si el contorno tiene 4 puntos, se considera el contorno del tablero
        if len(biggest_contour) == 4:
            break
    if len(biggest_contour) != 4:
        print("No se encontró un contorno con 4 puntos")
        return

    # Se reorganizan los puntos del contorno para calzar con el orden esperado
    biggest_contour = biggest_contour.reshape(-1, 2)
    puntos_ordenados_y = biggest_contour[np.argsort(biggest_contour[:, 1])]
    top = puntos_ordenados_y[:2]
    bottom = puntos_ordenados_y[2:]
    top = top[np.argsort(top[:, 0])]
    bottom = bottom[np.argsort(bottom[:, 0])]

    # Se define el tamaño de la imagen de salida
    image_size_np = np.float32([[0,0], [0, 450], [450, 450], [450, 0]])
    biggest_contour_np = np.float32([top[0], bottom[0], bottom[1], top[1]])

    # Se obtiene la matriz de transformación de perspectiva utilziando los puntos del contorno más grande y el tamaño de la imagen
    perspective_trans_matrix = cv2.getPerspectiveTransform(biggest_contour_np, image_size_np)
    # Se transforma la perspectiva del mayor contorno encontrado a una imagen de 450x450 píxeles
    image_warped = cv2.warpPerspective(img_tablero_base, perspective_trans_matrix, (450, 450))
    # Se convierte la imagen a escala de grises
    image_warped = cv2.cvtColor(image_warped, cv2.COLOR_BGR2GRAY)
    # Se aplica ecualizador de histograma para que calce con las imágenes de números entrenadas
    image_warped = cv2.equalizeHist(image_warped)

    # Se divide la imagen en 9 filas y 9 columnas
    image_divided_h = np.vsplit(image_warped, 9)
    celdas_sudoku = []
    for fila in image_divided_h:
        image_divided_v = np.hsplit(fila, 9)
        for celda in image_divided_v:
            celdas_sudoku.append(celda)
    
    prediccion_list = []
    for celda in celdas_sudoku:
        # Se redimensionan las celdas a 32x32 píxeles y se normalizan para que tengan las mismas dimensiones que las imágenes de entrenamiento
        img = cv2.resize(celda, (32, 32))
        img = img / 255
        img = img.reshape(1, 32, 32, 1)
        
        # Se predice la clase de la celda utilizando el modelo entrenado
        prediccion = model_cnn.predict(img, verbose=0)
        # Se obtiene la clase con mayor probabilidad
        clase_idx = np.argmax(prediccion, axis=1)
        valor_probabilidad = np.amax(prediccion)
        # Si la probabilidad de que el número pertenezca a la clase es mayor a 0.4, se considera el valor predicho
        prediccion_tmp = 0
        if valor_probabilidad > 0.4:
            prediccion_tmp = clase_idx[0]
        prediccion_list.append(prediccion_tmp)

    # Se redimensiona la lista de predicciones a una matriz de 9x9
    grid = np.asarray(prediccion_list)
    grid = np.reshape(grid, (9, 9))

    # Se obtiene el archivo de solución correspondiente a la imagen para validar la predicción
    path_solution = f"{path_image}.dat"
    list_solution = []
    # Se lee el archivo de solución y se formatea en una lista
    with open(path_solution, "r") as f:
        lines = f.readlines()
        for line in lines[2:]:
            list_line = line.replace(" \n", "").split(" ")
            list_line = [int(i) for i in list_line if i != ""]
            list_solution.append(list_line)
    
    # Se calcula el porcentaje de coincidencias entre la solución y la predicción
    array_solution = np.array(list_solution)
    count_coincidencias = 0
    for i in range(9):
        for j in range(9):
            if grid[i][j] == array_solution[i][j]:
                count_coincidencias += 1
    porcentaje_aciertos = count_coincidencias/81*100
    
    # Clase que inicializa el tablero de Sudoku para poder sugerir una técnica avanzada
    board_formatted = SudokuBoard(grid)
    # Se sugiere una técnica avanzada para resolver el Sudoku
    suggestion = suggest_technique(board_formatted)

    # Se calcula el tiempo de ejecución total
    timeend = time.time()
    seconds_execution = timeend - timestart

    # Si show_graphs es verdadero, se grafican las imágenes y resultados
    if show_graphs:
        print(f"Total de coincidencias: {count_coincidencias} de 81, {count_coincidencias/81*100}%")

        # Se grafica la imagen orinigal
        plt.figure(figsize=(5, 5))
        plt.title("Imagen original")
        plt.imshow(img_tablero_base, cmap = plt.get_cmap('gray'))
        plt.axis('off')
        plt.show()

        # Display the results
        plt.imshow(results_yolo[0].plot())
        plt.axis('off')
        plt.show()
        
        # Se grafican los contornos encontrados en la imagen
        cv2.drawContours(img_tablero_base, tablero_contours, -1, (0, 255, 0), 3)
        plt.figure(figsize=(5, 5))
        plt.title("Contornos en la imagen")
        plt.axis('off')
        plt.imshow(img_tablero_base)
        plt.show()

        # Se grafica la imagen con perspectiva transformada
        plt.figure(figsize=(5, 5))
        plt.title("Imagen con perspectiva transformada")
        plt.axis('off')
        plt.imshow(image_warped, cmap = plt.get_cmap('gray'))
        plt.show()

        # Se grafica el tablero de Sudoku digitalizado
        dibujar_sudoku(grid)
        # Se imprime la sugerencia de técnica avanzada
        print(f"Recomendación: {suggestion}")
        # Se entrega el tiempo de ejecución
        print(f"Tiempo de ejecución: {seconds_execution:.2f} segundos")
    return porcentaje_aciertos, seconds_execution, True

model_yolo = YOLO("models/yolo_best.pt")
model_cnn = joblib.load("models/cnn_model.h5")
# Ejecución de ejemplo
path_image = "data/sudoku_complete/data/image98"
porcentaje_aciertos, seconds_execution, bool_is_sudoku_is_correct = process_image_v2(path_image, model_cnn, model_yolo, True, True)
