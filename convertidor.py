import os
from tkinter import Tk, filedialog
from PIL import Image


def seleccionar_carpeta(titulo = "Selecciona una carpeta"):
	root = Tk()
	root.withdraw()
	carpeta = filedialog.askdirectory(title = titulo)
	return carpeta


def convertir_jpg_a_webp(carpeta_origen, carpeta_destino):
	if not carpeta_origen or not carpeta_destino:
		print("No se seleccionaron rutas válidas.")
		return
	
	for archivo in os.listdir(carpeta_origen):
		if archivo.lower().endswith(".jpg") or archivo.lower().endswith(".jpeg"):
			ruta_origen = os.path.join(carpeta_origen, archivo)
			nombre_base = os.path.splitext(archivo)[0]
			ruta_destino = os.path.join(carpeta_destino, nombre_base + ".webp")
			
			try:
				imagen = Image.open(ruta_origen)
				imagen.save(ruta_destino, "WEBP")
				print(f"Convertido: {archivo} -> {nombre_base}.webp")
			except Exception as e:
				print(f"Error al convertir {archivo}: {e}")


# Paso 1: Seleccionar carpeta de imágenes JPG
carpeta_jpg = seleccionar_carpeta("Selecciona la carpeta con imágenes JPG")

# Paso 2: Seleccionar carpeta de destino para imágenes WEBP
carpeta_webp = seleccionar_carpeta("Selecciona la carpeta donde guardar las imágenes WEBP")

# Paso 3: Convertir las imágenes
convertir_jpg_a_webp(carpeta_jpg, carpeta_webp)

print("Conversión completada.")