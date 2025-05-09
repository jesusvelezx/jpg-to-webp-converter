import os
import time
import threading
import concurrent.futures
from tkinter import Tk, Frame, Button, Label, Scale, StringVar, DoubleVar, IntVar, HORIZONTAL, BooleanVar, Canvas
from tkinter import ttk, messagebox, filedialog, PhotoImage, LabelFrame, Listbox, Scrollbar, VERTICAL, SINGLE, END
from PIL import Image, ImageTk
import piexif
from datetime import datetime
import matplotlib.pyplot as plt
from functools import partial


class ImageConverterApp:
	def __init__ (self, root):
		self.root = root
		self.root.title("Convertidor de Imágenes Avanzado")
		self.root.geometry("1050x700")
		
		# Colores y estilo
		self.color_primario = "#3498db"
		self.color_secundario = "#2980b9"
		self.color_fondo = "#f5f5f5"
		self.color_texto = "#333333"
		self.color_resalte = "#e74c3c"
		
		# Variables de Tkinter
		self.carpeta_origen = StringVar()
		self.carpeta_destino = StringVar()
		self.calidad_webp = IntVar(value = 80)
		self.formato_salida = StringVar(value = "webp")
		self.progreso = DoubleVar(value = 0)
		self.estado = StringVar(value = "Listo para comenzar")
		self.conservar_metadatos = IntVar(value = 1)
		self.redimensionar = IntVar(value = 0)
		self.ancho_nuevo = IntVar(value = 1200)
		self.modo_seleccion = StringVar(value = "carpeta")
		
		# Variables de estado y datos
		self.archivos_procesados = 0
		self.total_archivos = 0
		self.tamano_original = 0
		self.tamano_nuevo = 0
		self.tiempo_inicio = 0
		self.vista_previa_imagen = None
		self.archivo_seleccionado = None
		self.archivos_seleccionados = []
		self.miniaturas = []
		self.indice_miniatura_actual = 0
		self.cancelado = False
		
		# Elementos de la interfaz (inicializados como None)
		self.origen_carpeta_frame = None
		self.origen_archivos_frame = None
		self.archivos_label = None
		self.lista_frame = None
		self.lista_archivos = None
		self.scale_calidad = None
		self.label_calidad = None
		self.redim_frame = None
		self.boton_convertir = None
		self.preview_container = None
		self.preview_label = None
		self.nav_frame = None
		self.btn_prev = None
		self.indice_label = None
		self.btn_next = None
		self.barra_progreso = None
		self.info_original = None
		self.info_convertido = None
		self.info_ahorro = None
		self.stats_total = None
		self.stats_tamano = None
		self.stats_tiempo = None
		self.graph_frame = None
		
		# Crear interfaz
		self.crear_interfaz()
	
	def crear_interfaz (self):
		# Configurar estilo
		estilo = ttk.Style()
		estilo.configure("TFrame", background = self.color_fondo)
		estilo.configure("TButton", padding = 5, font = ('Segoe UI', 10))
		estilo.configure("TLabel", font = ('Segoe UI', 10), background = self.color_fondo)
		estilo.configure("TRadiobutton", font = ('Segoe UI', 10), background = self.color_fondo)
		estilo.configure("Header.TLabel", font = ('Segoe UI', 12, 'bold'), background = self.color_fondo)
		estilo.configure("TLabelframe", background = self.color_fondo)
		estilo.configure("TLabelframe.Label", font = ('Segoe UI', 10, 'bold'), background = self.color_fondo)
		
		# Frame principal
		main_frame = ttk.Frame(self.root, padding = "10", style = "TFrame")
		main_frame.pack(fill = "both", expand = True)
		
		# Panel izquierdo - configuración
		config_frame = ttk.LabelFrame(main_frame, text = "Configuración", padding = "10")
		config_frame.pack(side = "left", fill = "both", expand = True, padx = (0, 5))
		
		# Frame para el modo de selección
		modo_frame = ttk.LabelFrame(config_frame, text = "Modo de selección", padding = "5")
		modo_frame.grid(row = 0, column = 0, columnspan = 3, sticky = "ew", pady = 5)
		
		ttk.Radiobutton(modo_frame, text = "Seleccionar carpeta", variable = self.modo_seleccion,
		                value = "carpeta", command = self.cambiar_modo_seleccion).grid(row = 0, column = 0, padx = 5,
		                                                                               sticky = "w")
		ttk.Radiobutton(modo_frame, text = "Seleccionar archivos", variable = self.modo_seleccion,
		                value = "archivos", command = self.cambiar_modo_seleccion).grid(row = 0, column = 1, padx = 5,
		                                                                                sticky = "w")
		
		# Frame para selección de origen
		self.origen_carpeta_frame = ttk.Frame(config_frame)
		self.origen_carpeta_frame.grid(row = 1, column = 0, columnspan = 3, sticky = "ew", pady = 5)
		
		ttk.Label(self.origen_carpeta_frame, text = "Carpeta de origen:").grid(row = 0, column = 0, sticky = "w",
		                                                                       pady = 5)
		ttk.Entry(self.origen_carpeta_frame, textvariable = self.carpeta_origen, width = 40).grid(row = 0, column = 1,
		                                                                                          sticky = "ew",
		                                                                                          pady = 5)
		ttk.Button(self.origen_carpeta_frame, text = "Examinar", command = self.seleccionar_origen).grid(row = 0,
		                                                                                                 column = 2,
		                                                                                                 padx = 5,
		                                                                                                 pady = 5)
		
		# Frame para selección de archivos (inicialmente oculto)
		self.origen_archivos_frame = ttk.Frame(config_frame)
		self.origen_archivos_frame.grid(row = 1, column = 0, columnspan = 3, sticky = "ew", pady = 5)
		
		ttk.Label(self.origen_archivos_frame, text = "Archivos seleccionados:").grid(row = 0, column = 0, sticky = "w",
		                                                                             pady = 5)
		self.archivos_label = ttk.Label(self.origen_archivos_frame, text = "Ningún archivo seleccionado")
		self.archivos_label.grid(row = 0, column = 1, sticky = "ew", pady = 5)
		ttk.Button(self.origen_archivos_frame, text = "Seleccionar", command = self.seleccionar_archivos).grid(row = 0,
		                                                                                                       column = 2,
		                                                                                                       padx = 5,
		                                                                                                       pady = 5)
		
		# Listbox para mostrar archivos seleccionados
		self.lista_frame = ttk.Frame(self.origen_archivos_frame)
		self.lista_frame.grid(row = 1, column = 0, columnspan = 3, sticky = "ew", pady = 5)
		
		self.lista_archivos = Listbox(self.lista_frame, height = 3, width = 55, selectmode = SINGLE)
		scrollbar = Scrollbar(self.lista_frame, orient = VERTICAL, command = self.lista_archivos.yview)
		self.lista_archivos.config(yscrollcommand = scrollbar.set)
		
		self.lista_archivos.pack(side = "left", fill = "both", expand = True)
		scrollbar.pack(side = "right", fill = "y")
		
		self.lista_archivos.bind('<<ListboxSelect>>', self.cambiar_preview_por_seleccion)
		
		# Ocultar el frame de archivos inicialmente
		self.origen_archivos_frame.grid_remove()
		self.lista_frame.grid_remove()
		
		ttk.Label(config_frame, text = "Carpeta de destino:").grid(row = 2, column = 0, sticky = "w", pady = 5)
		ttk.Entry(config_frame, textvariable = self.carpeta_destino, width = 40).grid(row = 2, column = 1,
		                                                                              sticky = "ew", pady = 5)
		ttk.Button(config_frame, text = "Examinar", command = self.seleccionar_destino).grid(row = 2, column = 2,
		                                                                                     padx = 5, pady = 5)
		
		# Formato de salida
		ttk.Label(config_frame, text = "Formato de salida:").grid(row = 3, column = 0, sticky = "w", pady = 5)
		formatos = ttk.Combobox(config_frame, textvariable = self.formato_salida, state = "readonly")
		formatos['values'] = ('webp', 'png', 'jpg', 'avif', 'heif')
		formatos.grid(row = 3, column = 1, sticky = "ew", pady = 5)
		formatos.bind("<<ComboboxSelected>>", self.actualizar_opciones_formato)
		formatos.bind("<<ComboboxSelected>>", lambda e: self.actualizar_vista_previa_si_hay_seleccion(), add = "+")
		
		# Calidad
		ttk.Label(config_frame, text = "Calidad:").grid(row = 4, column = 0, sticky = "w", pady = 5)
		self.scale_calidad = Scale(config_frame, variable = self.calidad_webp, from_ = 0, to = 100,
		                           orient = HORIZONTAL, length = 200, bg = self.color_fondo,
		                           highlightthickness = 0, command = self.actualizar_vista_previa_por_calidad)
		self.scale_calidad.grid(row = 4, column = 1, sticky = "ew", pady = 5)
		self.label_calidad = ttk.Label(config_frame, text = "80%")
		self.label_calidad.grid(row = 4, column = 2, sticky = "w", pady = 5)
		
		# Opciones adicionales en un LabelFrame
		opciones_frame = ttk.LabelFrame(config_frame, text = "Opciones adicionales", padding = "5")
		opciones_frame.grid(row = 5, column = 0, columnspan = 3, sticky = "ew", pady = 10)
		
		ttk.Checkbutton(opciones_frame, text = "Conservar metadatos", variable = self.conservar_metadatos,
		                command = lambda: self.actualizar_vista_previa_si_hay_seleccion()).grid(
				row = 0, column = 0, columnspan = 2, sticky = "w", pady = 5)
		
		ttk.Checkbutton(opciones_frame, text = "Redimensionar imágenes", variable = self.redimensionar,
		                command = self.toggle_redimension).grid(row = 1, column = 0, columnspan = 2, sticky = "w",
		                                                        pady = 5)
		
		# Frame para opciones de redimensionado (inicialmente oculto)
		self.redim_frame = ttk.Frame(opciones_frame)
		self.redim_frame.grid(row = 2, column = 0, columnspan = 2, sticky = "w", pady = 5)
		ttk.Label(self.redim_frame, text = "Ancho máximo:").pack(side = "left")
		ttk.Entry(self.redim_frame, textvariable = self.ancho_nuevo, width = 6).pack(side = "left", padx = 5)
		ttk.Label(self.redim_frame, text = "px (mantiene proporción)").pack(side = "left")
		self.redim_frame.grid_remove()
		
		# Botones de acción
		botones_frame = ttk.Frame(config_frame)
		botones_frame.grid(row = 6, column = 0, columnspan = 3, pady = 15)
		
		self.boton_convertir = ttk.Button(botones_frame, text = "Convertir", command = self.iniciar_conversion)
		self.boton_convertir.pack(side = "left", padx = 5)
		ttk.Button(botones_frame, text = "Cancelar", command = self.cancelar_conversion).pack(side = "left", padx = 5)
		
		# Barra de progreso
		ttk.Label(config_frame, text = "Progreso:").grid(row = 7, column = 0, sticky = "w", pady = 5)
		self.barra_progreso = ttk.Progressbar(config_frame, variable = self.progreso, length = 300)
		self.barra_progreso.grid(row = 7, column = 1, columnspan = 2, sticky = "ew", pady = 5)
		
		# Estado
		ttk.Label(config_frame, textvariable = self.estado).grid(row = 8, column = 0, columnspan = 3, sticky = "w",
		                                                         pady = 5)
		
		# Panel derecho - vista previa y estadísticas
		preview_frame = ttk.LabelFrame(main_frame, text = "Vista previa y estadísticas", padding = "10")
		preview_frame.pack(side = "right", fill = "both", expand = True, padx = (5, 0))
		
		# Vista previa de imagen
		self.preview_container = ttk.Frame(preview_frame)
		self.preview_container.pack(fill = "both", expand = True, pady = 10)
		
		self.preview_label = ttk.Label(self.preview_container, text = "Selecciona un archivo para vista previa")
		self.preview_label.pack(pady = 10)
		
		# Controles de navegación para varias imágenes
		self.nav_frame = ttk.Frame(preview_frame)
		self.nav_frame.pack(fill = "x", pady = 5)
		
		self.btn_prev = ttk.Button(self.nav_frame, text = "< Anterior", command = self.mostrar_imagen_anterior,
		                           state = "disabled")
		self.btn_prev.pack(side = "left", padx = 5)
		
		self.indice_label = ttk.Label(self.nav_frame, text = "")
		self.indice_label.pack(side = "left", padx = 5, expand = True)
		
		self.btn_next = ttk.Button(self.nav_frame, text = "Siguiente >", command = self.mostrar_imagen_siguiente,
		                           state = "disabled")
		self.btn_next.pack(side = "right", padx = 5)
		
		# Ocultar navegación inicialmente
		self.nav_frame.pack_forget()
		
		# Frame para información de la imagen
		info_frame = ttk.LabelFrame(preview_frame, text = "Información")
		info_frame.pack(fill = "x", pady = 10)
		
		self.info_original = ttk.Label(info_frame, text = "Tamaño original: -")
		self.info_original.pack(anchor = "w", pady = 2)
		
		self.info_convertido = ttk.Label(info_frame, text = "Tamaño convertido: -")
		self.info_convertido.pack(anchor = "w", pady = 2)
		
		self.info_ahorro = ttk.Label(info_frame, text = "Ahorro: -")
		self.info_ahorro.pack(anchor = "w", pady = 2)
		
		# Frame para estadísticas totales
		stats_frame = ttk.LabelFrame(preview_frame, text = "Estadísticas de conversión")
		stats_frame.pack(fill = "both", expand = True, pady = 10)
		
		self.stats_total = ttk.Label(stats_frame, text = "Archivos procesados: 0")
		self.stats_total.pack(anchor = "w", pady = 2)
		
		self.stats_tamano = ttk.Label(stats_frame, text = "Reducción total: -")
		self.stats_tamano.pack(anchor = "w", pady = 2)
		
		self.stats_tiempo = ttk.Label(stats_frame, text = "Tiempo: -")
		self.stats_tiempo.pack(anchor = "w", pady = 2)
		
		# Canvas para gráfico de ahorro
		self.graph_frame = ttk.Frame(stats_frame)
		self.graph_frame.pack(fill = "both", expand = True, pady = 5)
	
	def actualizar_vista_previa_por_calidad (self, valor):
		"""Actualiza la vista previa cuando se cambia la calidad"""
		self.label_calidad.config(text = f"{self.calidad_webp.get()}%")
		# Esperar un poco antes de actualizar para evitar múltiples actualizaciones durante el deslizamiento
		self.root.after(200, self.actualizar_vista_previa_si_hay_seleccion)
	
	def actualizar_vista_previa_si_hay_seleccion (self):
		"""Actualiza la vista previa si hay una imagen seleccionada"""
		if self.archivo_seleccionado:
			self.mostrar_vista_previa()
	
	def cambiar_preview_por_seleccion (self, event):
		"""Cambia la vista previa cuando se selecciona una imagen de la lista"""
		if not self.lista_archivos.curselection():
			return
		
		indice = self.lista_archivos.curselection()[0]
		if 0 <= indice < len(self.archivos_seleccionados):
			self.archivo_seleccionado = self.archivos_seleccionados[indice]
			self.indice_miniatura_actual = indice
			self.mostrar_vista_previa()
			self.actualizar_botones_navegacion()
	
	def mostrar_imagen_anterior (self):
		"""Muestra la imagen anterior en la lista de seleccionadas"""
		if self.indice_miniatura_actual > 0:
			self.indice_miniatura_actual -= 1
			self.archivo_seleccionado = self.archivos_seleccionados[self.indice_miniatura_actual]
			self.lista_archivos.selection_clear(0, END)
			self.lista_archivos.selection_set(self.indice_miniatura_actual)
			self.lista_archivos.see(self.indice_miniatura_actual)
			self.mostrar_vista_previa()
			self.actualizar_botones_navegacion()
	
	def mostrar_imagen_siguiente (self):
		"""Muestra la imagen siguiente en la lista de seleccionadas"""
		if self.indice_miniatura_actual < len(self.archivos_seleccionados) - 1:
			self.indice_miniatura_actual += 1
			self.archivo_seleccionado = self.archivos_seleccionados[self.indice_miniatura_actual]
			self.lista_archivos.selection_clear(0, END)
			self.lista_archivos.selection_set(self.indice_miniatura_actual)
			self.lista_archivos.see(self.indice_miniatura_actual)
			self.mostrar_vista_previa()
			self.actualizar_botones_navegacion()
	
	def actualizar_botones_navegacion (self):
		"""Actualiza el estado de los botones de navegación"""
		# Mostrar el índice actual
		if self.archivos_seleccionados:
			self.indice_label.config(
					text = f"Imagen {self.indice_miniatura_actual + 1} de {len(self.archivos_seleccionados)}")
			
			# Actualizar estado de botones
			if self.indice_miniatura_actual <= 0:
				self.btn_prev.config(state = "disabled")
			else:
				self.btn_prev.config(state = "normal")
			
			if self.indice_miniatura_actual >= len(self.archivos_seleccionados) - 1:
				self.btn_next.config(state = "disabled")
			else:
				self.btn_next.config(state = "normal")
			
			# Mostrar la barra de navegación
			self.nav_frame.pack(fill = "x", pady = 5)
		else:
			self.nav_frame.pack_forget()
	
	def cambiar_modo_seleccion (self):
		"""Cambia entre modo de selección de carpeta y archivos"""
		modo = self.modo_seleccion.get()
		
		if modo == "carpeta":
			self.origen_archivos_frame.grid_remove()
			self.lista_frame.grid_remove()
			self.origen_carpeta_frame.grid()
			self.carpeta_origen.set("")
			self.archivos_seleccionados = []
			self.archivo_seleccionado = None
			
			# Resetear vista previa
			self.mostrar_mensaje_vista_previa("Selecciona una carpeta con imágenes")
			self.nav_frame.pack_forget()
		else:  # modo == "archivos"
			self.origen_carpeta_frame.grid_remove()
			self.origen_archivos_frame.grid()
			self.lista_frame.grid()
			self.carpeta_origen.set("")
			self.archivos_seleccionados = []
			self.archivo_seleccionado = None
			
			# Limpiar lista
			self.lista_archivos.delete(0, END)
			self.archivos_label.config(text = "Ningún archivo seleccionado")
			
			# Resetear vista previa
			self.mostrar_mensaje_vista_previa("Selecciona archivos para convertir")
			self.nav_frame.pack_forget()
	
	def toggle_redimension (self):
		"""Muestra u oculta las opciones de redimensión"""
		if self.redimensionar.get():
			self.redim_frame.grid()
		else:
			self.redim_frame.grid_remove()
		
		# Actualizar vista previa si hay una imagen seleccionada
		self.actualizar_vista_previa_si_hay_seleccion()
	
	def actualizar_opciones_formato (self, event):
		"""Actualiza las opciones según el formato seleccionado"""
		formato = self.formato_salida.get()
		if formato in ['jpg', 'webp', 'avif', 'heif']:
			self.scale_calidad.config(state = 'normal')
			self.label_calidad.config(state = 'normal')
		else:
			self.scale_calidad.config(state = 'disabled')
			self.label_calidad.config(state = 'disabled')
	
	def seleccionar_origen (self):
		"""Selecciona una carpeta de origen y muestra una vista previa"""
		carpeta = filedialog.askdirectory(title = "Selecciona la carpeta con imágenes originales")
		if carpeta:
			self.carpeta_origen.set(carpeta)
			
			# Buscar la primera imagen para vista previa
			formatos_soportados = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif']
			for archivo in os.listdir(carpeta):
				if archivo.lower().endswith(tuple(formatos_soportados)):
					self.archivo_seleccionado = os.path.join(carpeta, archivo)
					self.mostrar_vista_previa()
					break
	
	def seleccionar_archivos (self):
		"""Selecciona múltiples archivos y muestra una vista previa del primero"""
		archivos = filedialog.askopenfilenames(
				title = "Selecciona imágenes para convertir",
				filetypes = [("Imágenes", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff;*.gif")]
		)
		
		if archivos:
			self.archivos_seleccionados = list(archivos)
			
			# Actualizar etiqueta y listbox
			if len(self.archivos_seleccionados) > 1:
				self.archivos_label.config(text = f"{len(self.archivos_seleccionados)} archivos seleccionados")
			else:
				self.archivos_label.config(text = os.path.basename(self.archivos_seleccionados[0]))
			
			# Limpiar y llenar la lista
			self.lista_archivos.delete(0, END)
			for archivo in self.archivos_seleccionados:
				self.lista_archivos.insert(END, os.path.basename(archivo))
			
			# Seleccionar el primer archivo
			self.indice_miniatura_actual = 0
			self.archivo_seleccionado = self.archivos_seleccionados[0]
			self.lista_archivos.selection_set(0)
			
			# Mostrar vista previa
			self.mostrar_vista_previa()
			
			# Actualizar navegación
			self.actualizar_botones_navegacion()
	
	def seleccionar_destino (self):
		"""Selecciona una carpeta de destino"""
		carpeta = filedialog.askdirectory(title = "Selecciona la carpeta de destino")
		if carpeta:
			self.carpeta_destino.set(carpeta)
	
	def mostrar_mensaje_vista_previa (self, mensaje):
		"""Muestra un mensaje en lugar de una vista previa"""
		# Limpiar el contenedor de vista previa
		for widget in self.preview_container.winfo_children():
			widget.destroy()
		
		# Mostrar mensaje
		self.preview_label = ttk.Label(
				self.preview_container,
				text = mensaje,
				font = ('Segoe UI', 12)
		)
		self.preview_label.pack(pady = 50)
		
		# Restablecer información
		self.info_original.config(text = "Tamaño original: -")
		self.info_convertido.config(text = "Tamaño convertido: -")
		self.info_ahorro.config(text = "Ahorro: -")
	
	def mostrar_vista_previa (self):
		"""Genera y muestra una vista previa de la imagen seleccionada"""
		if not self.archivo_seleccionado:
			return
		
		try:
			# Mostrar imagen original
			img_original = Image.open(self.archivo_seleccionado)
			
			# Redimensionar para vista previa
			img_preview = self.redimensionar_para_vista_previa(img_original, 350)
			self.vista_previa_imagen = ImageTk.PhotoImage(img_preview)
			
			# Limpiar el contenedor de vista previa
			for widget in self.preview_container.winfo_children():
				widget.destroy()
			
			# Marco para la vista previa con borde
			preview_frame = ttk.Frame(self.preview_container, borderwidth = 2, relief = "solid")
			preview_frame.pack(pady = 10)
			
			# Crear nueva etiqueta con la imagen
			self.preview_label = Label(preview_frame, image = self.vista_previa_imagen, borderwidth = 0)
			self.preview_label.image = self.vista_previa_imagen
			self.preview_label.pack()
			
			# Añadir nombre del archivo
			nombre_archivo = os.path.basename(self.archivo_seleccionado)
			ttk.Label(self.preview_container, text = nombre_archivo,
			          font = ('Segoe UI', 10, 'bold')).pack(pady = 5)
			
			# Añadir dimensiones
			dimensiones = f"Dimensiones: {img_original.width} × {img_original.height} px"
			ttk.Label(self.preview_container, text = dimensiones).pack(pady = 2)
			
			# Crear versión convertida temporal para comparación
			nombre_temp = "temp_preview." + self.formato_salida.get()
			ruta_temp = os.path.join(os.path.dirname(self.archivo_seleccionado), nombre_temp)
			
			# Aplicar configuraciones actuales
			img_convertida = img_original.copy()
			
			# Redimensionar si está activado
			if self.redimensionar.get():
				ancho_orig = img_convertida.width
				alto_orig = img_convertida.height
				if ancho_orig > self.ancho_nuevo.get():
					ratio = self.ancho_nuevo.get() / ancho_orig
					nuevo_alto = int(alto_orig * ratio)
					img_convertida = img_convertida.resize((self.ancho_nuevo.get(), nuevo_alto), Image.LANCZOS)
			
			# Guardar con las opciones configuradas
			if self.formato_salida.get() == 'webp':
				img_convertida.save(ruta_temp, 'WEBP', quality = self.calidad_webp.get())
			elif self.formato_salida.get() == 'jpg':
				img_convertida.save(ruta_temp, 'JPEG', quality = self.calidad_webp.get())
			elif self.formato_salida.get() == 'png':
				img_convertida.save(ruta_temp, 'PNG')
			elif self.formato_salida.get() == 'avif':
				img_convertida.save(ruta_temp, 'AVIF', quality = self.calidad_webp.get())
			elif self.formato_salida.get() == 'heif':
				img_convertida.save(ruta_temp, 'HEIF', quality = self.calidad_webp.get())
			
			# Mostrar información de tamaño
			tamano_orig = os.path.getsize(self.archivo_seleccionado)
			tamano_conv = os.path.getsize(ruta_temp)
			ahorro = 100 - (tamano_conv / tamano_orig * 100)
			
			self.info_original.config(text = f"Tamaño original: {self.formato_tamano(tamano_orig)}")
			self.info_convertido.config(text = f"Tamaño convertido: {self.formato_tamano(tamano_conv)}")
			
			color_ahorro = "#4CAF50" if ahorro > 0 else "#F44336"
			texto_ahorro = f"Ahorro: {ahorro:.1f}% ({self.formato_tamano(tamano_orig - tamano_conv)})"
			self.info_ahorro.config(text = texto_ahorro)
			
			# Eliminar archivo temporal
			os.remove(ruta_temp)
		
		except Exception as e:
			self.mostrar_mensaje_vista_previa(f"Error al generar vista previa: {str(e)}")
	
	def redimensionar_para_vista_previa (self, imagen, tamano_max):
		"""Redimensiona una imagen manteniendo la proporción para la vista previa"""
		ancho, alto = imagen.size
		if ancho > alto:
			nuevo_ancho = tamano_max
			nuevo_alto = int(alto * tamano_max / ancho)
		else:
			nuevo_alto = tamano_max
			nuevo_ancho = int(ancho * tamano_max / alto)
		
		return imagen.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)
	
	def formato_tamano (self, tamano_bytes):
		"""Formatea un tamaño en bytes a formato legible (KB, MB)"""
		if tamano_bytes < 1024:
			return f"{tamano_bytes} bytes"
		elif tamano_bytes < 1024 * 1024:
			return f"{tamano_bytes / 1024:.1f} KB"
		else:
			return f"{tamano_bytes / (1024 * 1024):.2f} MB"
	
	def iniciar_conversion (self):
		"""Inicia el proceso de conversión de imágenes"""
		carpeta_destino = self.carpeta_destino.get()
		
		if not carpeta_destino:
			messagebox.showwarning("Advertencia", "Debes seleccionar una carpeta de destino.")
			return
		
		if not os.path.exists(carpeta_destino):
			try:
				os.makedirs(carpeta_destino)
			except Exception as e:
				messagebox.showerror("Error", f"No se pudo crear la carpeta de destino: {str(e)}")
				return
		
		# Reiniciar variables de control
		self.cancelado = False
		self.tamano_original = 0
		self.tamano_nuevo = 0
		self.archivos_procesados = 0
		
		# Obtener lista de archivos a procesar según el modo
		if self.modo_seleccion.get() == "carpeta":
			carpeta_origen = self.carpeta_origen.get()
			if not carpeta_origen:
				messagebox.showwarning("Advertencia", "Debes seleccionar una carpeta de origen.")
				return
			
			formatos_soportados = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif']
			archivos = [os.path.join(carpeta_origen, f) for f in os.listdir(carpeta_origen)
			            if os.path.isfile(os.path.join(carpeta_origen, f)) and
			            os.path.splitext(f)[1].lower() in formatos_soportados]
		else:  # modo archivos
			if not self.archivos_seleccionados:
				messagebox.showwarning("Advertencia", "Debes seleccionar al menos un archivo.")
				return
			
			archivos = self.archivos_seleccionados
		
		self.total_archivos = len(archivos)
		
		if self.total_archivos == 0:
			messagebox.showinfo("Información", "No se encontraron imágenes para procesar.")
			return
		
		# Iniciar tiempo
		self.tiempo_inicio = time.time()
		
		# Deshabilitar botones durante la conversión
		self.boton_convertir.config(state = "disabled")
		
		# Iniciar conversión en hilo separado
		threading.Thread(target = self.procesar_lote, args = (carpeta_destino, archivos)).start()
	
	def procesar_lote (self, carpeta_destino, archivos):
		"""Procesa un lote de imágenes en paralelo"""
		# Actualizar interfaz
		self.estado.set(f"Procesando {len(archivos)} archivos...")
		self.progreso.set(0)
		
		# Usar ThreadPoolExecutor para procesamiento paralelo
		with concurrent.futures.ThreadPoolExecutor(max_workers = os.cpu_count()) as executor:
			futures = []
			for archivo in archivos:
				if self.cancelado:
					break
				
				nombre_base = os.path.splitext(os.path.basename(archivo))[0]
				extension = "." + self.formato_salida.get()
				ruta_destino = os.path.join(carpeta_destino, nombre_base + extension)
				
				future = executor.submit(
						self.convertir_imagen,
						archivo,
						ruta_destino
				)
				futures.append(future)
			
			# Procesar resultados a medida que terminan
			for i, future in enumerate(concurrent.futures.as_completed(futures)):
				if self.cancelado:
					executor.shutdown(wait = False)
					break
				
				tamano_orig, tamano_nuevo = future.result()
				self.tamano_original += tamano_orig
				self.tamano_nuevo += tamano_nuevo
				self.archivos_procesados += 1
				
				# Actualizar progreso
				porcentaje = (self.archivos_procesados / self.total_archivos) * 100
				self.root.after(10, lambda p = porcentaje: self.progreso.set(p))
				
				# Actualizar estadísticas cada 3 archivos o al final
				if self.archivos_procesados % 3 == 0 or self.archivos_procesados == self.total_archivos:
					self.root.after(10, self.actualizar_estadisticas)
		
		# Finalizar
		tiempo_total = time.time() - self.tiempo_inicio
		
		# Habilitar botones nuevamente
		self.root.after(0, lambda: self.boton_convertir.config(state = "normal"))
		
		if self.cancelado:
			self.root.after(0, lambda: self.estado.set("Conversión cancelada."))
		else:
			self.root.after(0, lambda: self.estado.set(
					f"Conversión completada. {self.archivos_procesados} archivos procesados en {tiempo_total:.1f} segundos."
			))
			
			# Generar gráfico de ahorro
			self.generar_grafico_ahorro()
			
			# Mostrar mensaje de finalización con estilo mejorado
			self.root.after(100, self.mostrar_resumen_conversion)
	
	def mostrar_resumen_conversion (self):
		"""Muestra un resumen de la conversión con un diseño mejorado"""
		tiempo_total = time.time() - self.tiempo_inicio
		ahorro = self.calcular_porcentaje_ahorro()
		
		# Crear ventana de resumen
		ventana_resumen = Tk()
		ventana_resumen.title("Conversión Completada")
		ventana_resumen.geometry("400x350")
		ventana_resumen.resizable(False, False)
		
		# Frame principal
		frame_principal = Frame(ventana_resumen, bg = "#f5f5f5", padx = 20, pady = 20)
		frame_principal.pack(fill = "both", expand = True)
		
		# Título
		Label(frame_principal, text = "¡Conversión completada con éxito!",
		      font = ("Segoe UI", 14, "bold"), bg = "#f5f5f5", fg = "#4CAF50").pack(pady = (0, 15))
		
		# Estadísticas
		frame_stats = Frame(frame_principal, bg = "#f5f5f5", relief = "groove", bd = 1)
		frame_stats.pack(fill = "x", pady = 10)
		
		Label(frame_stats, text = f"Archivos procesados: {self.archivos_procesados}",
		      font = ("Segoe UI", 10), bg = "#f5f5f5", anchor = "w").pack(fill = "x", padx = 15, pady = 5)
		
		Label(frame_stats, text = f"Tamaño original: {self.formato_tamano(self.tamano_original)}",
		      font = ("Segoe UI", 10), bg = "#f5f5f5", anchor = "w").pack(fill = "x", padx = 15, pady = 5)
		
		Label(frame_stats, text = f"Tamaño nuevo: {self.formato_tamano(self.tamano_nuevo)}",
		      font = ("Segoe UI", 10), bg = "#f5f5f5", anchor = "w").pack(fill = "x", padx = 15, pady = 5)
		
		Label(frame_stats,
		      text = f"Ahorro: {ahorro:.1f}% ({self.formato_tamano(self.tamano_original - self.tamano_nuevo)})",
		      font = ("Segoe UI", 10, "bold"), bg = "#f5f5f5", fg = "#E91E63", anchor = "w").pack(fill = "x", padx = 15,
		                                                                                          pady = 5)
		
		Label(frame_stats, text = f"Tiempo: {tiempo_total:.1f} segundos",
		      font = ("Segoe UI", 10), bg = "#f5f5f5", anchor = "w").pack(fill = "x", padx = 15, pady = 5)
		
		# Ubicación
		Label(frame_principal, text = f"Las imágenes convertidas se guardaron en:",
		      font = ("Segoe UI", 9), bg = "#f5f5f5").pack(anchor = "w", pady = (15, 5))
		
		# Frame para la ruta
		frame_ruta = Frame(frame_principal, bg = "#EEF2F5", relief = "groove", bd = 1)
		frame_ruta.pack(fill = "x", pady = 5)
		
		Label(frame_ruta, text = self.carpeta_destino.get(),
		      font = ("Segoe UI", 9), bg = "#EEF2F5", wraplength = 350, justify = "left").pack(fill = "x", padx = 10,
		                                                                                       pady = 8)
		
		# Botón cerrar
		Button(frame_principal, text = "Cerrar", command = ventana_resumen.destroy,
		       font = ("Segoe UI", 10), padx = 20, bg = "#4CAF50", fg = "white").pack(pady = 15)
		
		# Centrar ventana
		ventana_resumen.update_idletasks()
		ancho = ventana_resumen.winfo_width()
		alto = ventana_resumen.winfo_height()
		x = (ventana_resumen.winfo_screenwidth() // 2) - (ancho // 2)
		y = (ventana_resumen.winfo_screenheight() // 2) - (alto // 2)
		ventana_resumen.geometry('{}x{}+{}+{}'.format(ancho, alto, x, y))
		
		ventana_resumen.mainloop()
	
	def convertir_imagen (self, ruta_origen, ruta_destino):
		"""Convierte una imagen y devuelve el tamaño original y nuevo"""
		try:
			# Obtener tamaño original
			tamano_orig = os.path.getsize(ruta_origen)
			
			# Abrir imagen
			imagen = Image.open(ruta_origen)
			
			# Obtener metadatos si es necesario
			metadatos = None
			if self.conservar_metadatos.get() and ruta_origen.lower().endswith(('.jpg', '.jpeg', '.tiff')):
				try:
					metadatos = piexif.load(ruta_origen)
				except Exception:
					pass
			
			# Redimensionar si está activado
			if self.redimensionar.get():
				ancho_orig = imagen.width
				alto_orig = imagen.height
				if ancho_orig > self.ancho_nuevo.get():
					ratio = self.ancho_nuevo.get() / ancho_orig
					nuevo_alto = int(alto_orig * ratio)
					imagen = imagen.resize((self.ancho_nuevo.get(), nuevo_alto), Image.LANCZOS)
			
			# Guardar con el formato elegido
			formato = self.formato_salida.get()
			if formato == 'webp':
				imagen.save(ruta_destino, "WEBP", quality = self.calidad_webp.get())
			elif formato == 'jpg':
				if metadatos:
					exif_bytes = piexif.dump(metadatos)
					imagen.save(ruta_destino, "JPEG", quality = self.calidad_webp.get(), exif = exif_bytes)
				else:
					imagen.save(ruta_destino, "JPEG", quality = self.calidad_webp.get())
			elif formato == 'png':
				imagen.save(ruta_destino, "PNG")
			elif formato == 'avif':
				imagen.save(ruta_destino, "AVIF", quality = self.calidad_webp.get())
			elif formato == 'heif':
				imagen.save(ruta_destino, "HEIF", quality = self.calidad_webp.get())
			
			# Obtener tamaño nuevo
			tamano_nuevo = os.path.getsize(ruta_destino)
			
			return tamano_orig, tamano_nuevo
		
		except Exception as e:
			print(f"Error al convertir {os.path.basename(ruta_origen)}: {e}")
			return 0, 0
	
	def cancelar_conversion (self):
		"""Cancela la conversión en curso"""
		self.cancelado = True
		self.estado.set("Cancelando...")
	
	def actualizar_estadisticas (self):
		"""Actualiza los widgets de estadísticas"""
		if self.archivos_procesados > 0:
			# Actualizar etiquetas de estadísticas
			self.stats_total.config(text = f"Archivos procesados: {self.archivos_procesados} de {self.total_archivos}")
			
			if self.tamano_original > 0:
				ahorro = self.calcular_porcentaje_ahorro()
				ahorro_abs = self.tamano_original - self.tamano_nuevo
				
				self.stats_tamano.config(
						text = f"Reducción: {ahorro:.1f}% ({self.formato_tamano(ahorro_abs)})"
				)
			
			tiempo_actual = time.time() - self.tiempo_inicio
			self.stats_tiempo.config(text = f"Tiempo: {tiempo_actual:.1f} segundos")
	
	def calcular_porcentaje_ahorro (self):
		"""Calcula el porcentaje de ahorro"""
		if self.tamano_original > 0:
			return 100 - (self.tamano_nuevo / self.tamano_original * 100)
		return 0
	
	def generar_grafico_ahorro (self):
		"""Genera un gráfico de comparación de tamaños"""
		try:
			# Crear figura y ejes con estilo mejorado
			plt.style.use('ggplot')
			fig, ax = plt.subplots(figsize = (5, 4), dpi = 80)
			
			# Datos
			formatos = ['Original', self.formato_salida.get().upper()]
			tamanos = [self.tamano_original / (1024 * 1024), self.tamano_nuevo / (1024 * 1024)]
			
			# Crear gráfico de barras con colores más atractivos
			barras = ax.bar(formatos, tamanos, color = ['#FF7043', '#42A5F5'], width = 0.5)
			
			# Estilizar gráfico
			ax.set_ylabel('Tamaño (MB)')
			ax.set_title('Comparación de Tamaños', fontweight = 'bold')
			ax.spines['top'].set_visible(False)
			ax.spines['right'].set_visible(False)
			ax.grid(axis = 'y', linestyle = '--', alpha = 0.7)
			
			# Añadir texto con el valor
			for i, barra in enumerate(barras):
				altura = barra.get_height()
				ax.text(barra.get_x() + barra.get_width() / 2., altura + 0.05,
				        f'{altura:.2f} MB', ha = 'center', va = 'bottom', fontweight = 'bold')
			
			# Añadir texto con el porcentaje de ahorro
			ahorro = self.calcular_porcentaje_ahorro()
			ax.text(0.5, 0.9, f'Ahorro: {ahorro:.1f}%',
			        transform = ax.transAxes, ha = 'center',
			        bbox = dict(facecolor = 'white', alpha = 0.8, boxstyle = 'round,pad=0.5'),
			        fontsize = 11, fontweight = 'bold', color = '#E91E63')
			
			# Ajustar márgenes
			plt.tight_layout()
			
			# Guardar gráfico en un archivo
			ruta_grafico = os.path.join(os.path.dirname(self.carpeta_destino.get()),
			                            f"estadisticas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
			fig.savefig(ruta_grafico)
			
			# Mostrar mensaje con la ubicación del gráfico
			messagebox.showinfo("Estadísticas guardadas",
			                    f"Se ha guardado un gráfico con las estadísticas en:\n{ruta_grafico}")
		
		except Exception:
			print(f"Error al generar gráfico")


# Comprobar si se tienen las bibliotecas necesarias
def verificar_dependencias ():
	"""Verifica e instala las dependencias necesarias"""
	dependencias = {
		"piexif": "piexif",
		"matplotlib": "matplotlib"
	}
	
	for modulo, paquete in dependencias.items():
		try:
			__import__(modulo)
		except ImportError:
			print(f"La biblioteca {modulo} no está instalada. Instalando...")
			import subprocess
			try:
				subprocess.check_call(["pip", "install", paquete])
				print(f"{paquete} instalado correctamente.")
			except Exception as e:
				print(f"Error al instalar {paquete}: {e}")
				messagebox.showerror("Error de dependencia",
				                     f"No se pudo instalar {paquete}. Por favor, instálalo manualmente con 'pip install {paquete}'")
				return False
	return True


# Función principal
def main ():
	"""Función principal del programa"""
	if verificar_dependencias():
		root = Tk()
		app = ImageConverterApp(root)
		root.mainloop()


if __name__ == "__main__":
	main()