import os
import time
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, Menu, Label, Scale, HORIZONTAL, Frame, END
from PIL import Image, ImageTk
import concurrent.futures
from datetime import datetime


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
		self.carpeta_origen = tk.StringVar()
		self.carpeta_destino = tk.StringVar()
		self.calidad_webp = tk.IntVar(value = 80)
		self.formato_salida = tk.StringVar(value = "webp")
		self.progreso = tk.DoubleVar(value = 0)
		self.porcentaje_progreso = tk.StringVar(value = "0%")
		self.estado = tk.StringVar(value = "Listo para comenzar")
		self.conservar_metadatos = tk.IntVar(value = 1)
		self.redimensionar = tk.IntVar(value = 0)
		self.ancho_nuevo = tk.IntVar(value = 1200)
		self.modo_seleccion = tk.StringVar(value = "carpeta")
		self.modo_vista_previa = tk.StringVar(value = "simple")
		
		# Variables de estado y datos
		self.archivos_procesados = 0
		self.total_archivos = 0
		self.tamano_original = 0
		self.tamano_nuevo = 0
		self.tiempo_inicio = 0
		self.vista_previa_imagen = None
		self.vista_previa_convertida = None
		self.archivo_seleccionado = None
		self.archivos_seleccionados = []
		self.miniaturas = []
		self.indice_miniatura_actual = 0
		self.cancelado = False
		self.historial_conversiones = []
		
		# Inicializar interfaz
		try:
			# Crear menú superior
			self.crear_menu()
			
			# Crear interfaz principal
			self.crear_interfaz()
			
			print("Interfaz creada correctamente")
		except Exception as e:
			messagebox.showerror("Error de inicialización", f"Error al crear la interfaz: {str(e)}")
			print(f"ERROR: {str(e)}")
			import traceback
			traceback.print_exc()
	
	def crear_menu (self):
		"""Crea el menú superior de la aplicación"""
		menu_bar = Menu(self.root)
		self.root.config(menu = menu_bar)
		
		# Menú Archivo
		archivo_menu = Menu(menu_bar, tearoff = 0)
		menu_bar.add_cascade(label = "Archivo", menu = archivo_menu)
		archivo_menu.add_command(label = "Seleccionar carpeta de origen", command = self.seleccionar_origen)
		archivo_menu.add_command(label = "Seleccionar archivos", command = self.seleccionar_archivos)
		archivo_menu.add_command(label = "Seleccionar carpeta de destino", command = self.seleccionar_destino)
		archivo_menu.add_separator()
		archivo_menu.add_command(label = "Salir", command = self.root.quit)
		
		# Menú Convertir
		convertir_menu = Menu(menu_bar, tearoff = 0)
		menu_bar.add_cascade(label = "Convertir", menu = convertir_menu)
		convertir_menu.add_command(label = "Iniciar conversión", command = self.iniciar_conversion)
		convertir_menu.add_command(label = "Cancelar conversión", command = self.cancelar_conversion)
		convertir_menu.add_separator()
		
		# Submenú para formato de salida
		formato_menu = Menu(convertir_menu, tearoff = 0)
		convertir_menu.add_cascade(label = "Formato de salida", menu = formato_menu)
		formatos = ['webp', 'png', 'jpg']
		for fmt in formatos:
			formato_menu.add_radiobutton(label = fmt.upper(), variable = self.formato_salida, value = fmt,
			                             command = self.actualizar_opciones_formato)
		
		# Menú Ver
		ver_menu = Menu(menu_bar, tearoff = 0)
		menu_bar.add_cascade(label = "Ver", menu = ver_menu)
		ver_menu.add_radiobutton(label = "Vista previa simple", variable = self.modo_vista_previa, value = "simple",
		                         command = self.cambiar_modo_vista_previa)
		ver_menu.add_radiobutton(label = "Vista previa comparativa", variable = self.modo_vista_previa,
		                         value = "comparativa",
		                         command = self.cambiar_modo_vista_previa)
		
		# Menú Ayuda
		ayuda_menu = Menu(menu_bar, tearoff = 0)
		menu_bar.add_cascade(label = "Ayuda", menu = ayuda_menu)
		ayuda_menu.add_command(label = "Acerca de formatos de imagen", command = self.mostrar_info_formatos)
		ayuda_menu.add_separator()
		ayuda_menu.add_command(label = "Acerca de", command = self.mostrar_acerca_de)
	
	def crear_interfaz (self):
		"""Crea la interfaz principal de la aplicación"""
		# Frame principal
		main_frame = ttk.Frame(self.root, padding = "10")
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
		
		# Frame para selección de carpeta origen
		self.origen_carpeta_frame = ttk.Frame(config_frame)
		self.origen_carpeta_frame.grid(row = 1, column = 0, columnspan = 3, sticky = "ew", pady = 5)
		
		ttk.Label(self.origen_carpeta_frame, text = "Carpeta de origen:").grid(row = 0, column = 0, sticky = "w",
		                                                                       pady = 5)
		ttk.Entry(self.origen_carpeta_frame, textvariable = self.carpeta_origen, width = 40).grid(
				row = 0, column = 1, sticky = "ew", pady = 5)
		ttk.Button(self.origen_carpeta_frame, text = "Examinar", command = self.seleccionar_origen).grid(
				row = 0, column = 2, padx = 5, pady = 5)
		
		# Frame para selección de archivos
		self.origen_archivos_frame = ttk.Frame(config_frame)
		self.origen_archivos_frame.grid(row = 1, column = 0, columnspan = 3, sticky = "ew", pady = 5)
		
		ttk.Label(self.origen_archivos_frame, text = "Archivos seleccionados:").grid(row = 0, column = 0, sticky = "w",
		                                                                             pady = 5)
		self.archivos_label = ttk.Label(self.origen_archivos_frame, text = "Ningún archivo seleccionado")
		self.archivos_label.grid(row = 0, column = 1, sticky = "ew", pady = 5)
		ttk.Button(self.origen_archivos_frame, text = "Seleccionar", command = self.seleccionar_archivos).grid(
				row = 0, column = 2, padx = 5, pady = 5)
		
		# Listbox para mostrar archivos seleccionados
		self.lista_frame = ttk.Frame(self.origen_archivos_frame)
		self.lista_frame.grid(row = 1, column = 0, columnspan = 3, sticky = "ew", pady = 5)
		
		self.lista_archivos = tk.Listbox(self.lista_frame, height = 5, width = 55, selectmode = tk.SINGLE)
		scrollbar = ttk.Scrollbar(self.lista_frame, orient = tk.VERTICAL, command = self.lista_archivos.yview)
		self.lista_archivos.config(yscrollcommand = scrollbar.set)
		
		self.lista_archivos.pack(side = "left", fill = "both", expand = True)
		scrollbar.pack(side = "right", fill = "y")
		
		self.lista_archivos.bind('<<ListboxSelect>>', self.cambiar_preview_por_seleccion)
		
		# Ocultar el frame de archivos inicialmente
		self.origen_archivos_frame.grid_remove()
		self.lista_frame.grid_remove()
		
		# Carpeta destino
		ttk.Label(config_frame, text = "Carpeta de destino:").grid(row = 2, column = 0, sticky = "w", pady = 5)
		ttk.Entry(config_frame, textvariable = self.carpeta_destino, width = 40).grid(
				row = 2, column = 1, sticky = "ew", pady = 5)
		ttk.Button(config_frame, text = "Examinar", command = self.seleccionar_destino).grid(
				row = 2, column = 2, padx = 5, pady = 5)
		
		# Formato de salida con mejor visualización
		formato_frame = ttk.LabelFrame(config_frame, text = "Formato y calidad", padding = "5")
		formato_frame.grid(row = 3, column = 0, columnspan = 3, sticky = "ew", pady = 10)
		
		ttk.Label(formato_frame, text = "Formato de salida:").grid(row = 0, column = 0, sticky = "w", pady = 5)
		formatos = ttk.Combobox(formato_frame, textvariable = self.formato_salida, state = "readonly")
		formatos['values'] = ('webp', 'png', 'jpg')
		formatos.grid(row = 0, column = 1, sticky = "ew", pady = 5, padx = 5)
		formatos.bind("<<ComboboxSelected>>", self.actualizar_opciones_formato)
		
		# Calidad con mejor diseño
		ttk.Label(formato_frame, text = "Calidad:").grid(row = 1, column = 0, sticky = "w", pady = 5)
		calidad_frame = ttk.Frame(formato_frame)
		calidad_frame.grid(row = 1, column = 1, sticky = "ew", pady = 5, padx = 5)
		
		self.scale_calidad = Scale(calidad_frame, variable = self.calidad_webp, from_ = 0, to = 100,
		                           orient = HORIZONTAL, length = 250, bg = self.color_fondo,
		                           highlightthickness = 0, command = self.actualizar_calidad)
		self.scale_calidad.pack(side = "left", fill = "x", expand = True)
		
		self.label_calidad = ttk.Label(calidad_frame, text = "80%", width = 5)
		self.label_calidad.pack(side = "right", padx = 5)
		
		# Opciones adicionales
		opciones_frame = ttk.LabelFrame(config_frame, text = "Opciones adicionales", padding = "10")
		opciones_frame.grid(row = 4, column = 0, columnspan = 3, sticky = "ew", pady = 10)
		
		ttk.Checkbutton(opciones_frame, text = "Conservar metadatos", variable = self.conservar_metadatos,
		                command = self.actualizar_vista_previa_si_hay_seleccion).grid(
				row = 0, column = 0, columnspan = 2, sticky = "w", pady = 5)
		
		ttk.Checkbutton(opciones_frame, text = "Redimensionar imágenes", variable = self.redimensionar,
		                command = self.toggle_redimension).grid(row = 1, column = 0, columnspan = 2, sticky = "w",
		                                                        pady = 5)
		
		# Frame para opciones de redimensionado
		self.redim_frame = ttk.Frame(opciones_frame)
		self.redim_frame.grid(row = 2, column = 0, columnspan = 2, sticky = "w", pady = 5)
		ttk.Label(self.redim_frame, text = "Ancho máximo:").pack(side = "left")
		ttk.Entry(self.redim_frame, textvariable = self.ancho_nuevo, width = 6).pack(side = "left", padx = 5)
		ttk.Label(self.redim_frame, text = "px (mantiene proporción)").pack(side = "left")
		self.redim_frame.grid_remove()
		
		# Botones de acción
		botones_frame = ttk.Frame(config_frame)
		botones_frame.grid(row = 5, column = 0, columnspan = 3, pady = 15)
		
		self.boton_convertir = ttk.Button(botones_frame, text = "Convertir", command = self.iniciar_conversion)
		self.boton_convertir.pack(side = "left", padx = 5)
		ttk.Button(botones_frame, text = "Cancelar", command = self.cancelar_conversion).pack(side = "left", padx = 5)
		
		# Barra de progreso mejorada con porcentaje
		progreso_frame = ttk.Frame(config_frame)
		progreso_frame.grid(row = 6, column = 0, columnspan = 3, sticky = "ew", pady = 5)
		
		ttk.Label(progreso_frame, text = "Progreso:").pack(side = "left", padx = 5)
		self.barra_progreso = ttk.Progressbar(progreso_frame, variable = self.progreso, length = 300)
		self.barra_progreso.pack(side = "left", fill = "x", expand = True, padx = 5)
		self.porcentaje_label = ttk.Label(progreso_frame, textvariable = self.porcentaje_progreso, width = 6)
		self.porcentaje_label.pack(side = "right", padx = 5)
		
		# Estado
		ttk.Label(config_frame, textvariable = self.estado, font = ('Segoe UI', 10, 'italic')).grid(
				row = 7, column = 0, columnspan = 3, sticky = "w", pady = 5)
		
		# Panel derecho - vista previa y estadísticas
		preview_frame = ttk.LabelFrame(main_frame, text = "Vista previa y estadísticas", padding = "10")
		preview_frame.pack(side = "right", fill = "both", expand = True, padx = (5, 0))
		
		# Notebook para organizar vistas
		self.notebook = ttk.Notebook(preview_frame)
		self.notebook.pack(fill = "both", expand = True, pady = 5)
		
		# Pestaña 1: Vista previa simple
		tab_preview = ttk.Frame(self.notebook)
		self.notebook.add(tab_preview, text = "Vista Previa")
		
		# Vista previa de imagen
		self.preview_container = ttk.Frame(tab_preview)
		self.preview_container.pack(fill = "both", expand = True, pady = 10)
		
		self.preview_label = ttk.Label(self.preview_container, text = "Selecciona un archivo para vista previa")
		self.preview_label.pack(pady = 10)
		
		# Controles de navegación para varias imágenes
		self.nav_frame = ttk.Frame(tab_preview)
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
		
		# Pestaña 2: Vista comparativa
		tab_comparativa = ttk.Frame(self.notebook)
		self.notebook.add(tab_comparativa, text = "Comparativa")
		
		# Contenedor para vista comparativa
		comp_container = ttk.Frame(tab_comparativa)
		comp_container.pack(fill = "both", expand = True, pady = 10)
		
		# Frame para vista original
		orig_frame = ttk.LabelFrame(comp_container, text = "Original")
		orig_frame.pack(side = "left", fill = "both", expand = True, padx = 5)
		
		self.preview_original_label = ttk.Label(orig_frame, text = "Sin imagen")
		self.preview_original_label.pack(pady = 10, expand = True)
		
		# Frame para vista convertida
		conv_frame = ttk.LabelFrame(comp_container, text = "Convertida")
		conv_frame.pack(side = "right", fill = "both", expand = True, padx = 5)
		
		self.preview_converted_label = ttk.Label(conv_frame, text = "Sin imagen")
		self.preview_converted_label.pack(pady = 10, expand = True)
		
		# Pestaña 3: Información
		tab_info = ttk.Frame(self.notebook)
		self.notebook.add(tab_info, text = "Información")
		
		# Información de la imagen
		info_frame = ttk.LabelFrame(tab_info, text = "Información de la imagen", padding = 10)
		info_frame.pack(fill = "x", pady = 10)
		
		self.info_original = ttk.Label(info_frame, text = "Tamaño original: -")
		self.info_original.pack(anchor = "w", pady = 2)
		
		self.info_convertido = ttk.Label(info_frame, text = "Tamaño convertido: -")
		self.info_convertido.pack(anchor = "w", pady = 2)
		
		self.info_ahorro = ttk.Label(info_frame, text = "Ahorro: -")
		self.info_ahorro.pack(anchor = "w", pady = 2)
		
		# Estadísticas de conversión
		stats_frame = ttk.LabelFrame(tab_info, text = "Estadísticas de conversión")
		stats_frame.pack(fill = "both", expand = True, pady = 10)
		
		self.stats_total = ttk.Label(stats_frame, text = "Archivos procesados: 0")
		self.stats_total.pack(anchor = "w", pady = 2)
		
		self.stats_tamano = ttk.Label(stats_frame, text = "Reducción total: -")
		self.stats_tamano.pack(anchor = "w", pady = 2)
		
		self.stats_tiempo = ttk.Label(stats_frame, text = "Tiempo: -")
		self.stats_tiempo.pack(anchor = "w", pady = 2)
	
	def cambiar_modo_vista_previa (self):
		"""Cambia entre los modos de vista previa simple y comparativa"""
		if self.archivo_seleccionado:
			self.mostrar_vista_previa()
	
	def actualizar_calidad (self, valor):
		"""Actualiza la etiqueta de calidad y la vista previa"""
		self.label_calidad.config(text = f"{self.calidad_webp.get()}%")
		self.actualizar_vista_previa_si_hay_seleccion()
	
	def actualizar_vista_previa_si_hay_seleccion (self):
		"""Actualiza la vista previa si hay una imagen seleccionada"""
		if self.archivo_seleccionado:
			self.mostrar_vista_previa()
	
	def actualizar_opciones_formato (self, event = None):
		"""Actualiza las opciones según el formato seleccionado"""
		formato = self.formato_salida.get()
		if formato in ['jpg', 'webp']:
			self.scale_calidad.config(state = 'normal')
			self.label_calidad.config(state = 'normal')
		else:
			self.scale_calidad.config(state = 'disabled')
			self.label_calidad.config(state = 'disabled')
		
		# Actualizar vista previa si hay selección
		if self.archivo_seleccionado:
			self.mostrar_vista_previa()
	
	def mostrar_info_formatos (self):
		"""Muestra información sobre los formatos de imagen soportados"""
		info = (
			"Formatos de imagen soportados:\n\n"
			"WebP: Formato moderno de Google con buena compresión y soporte para transparencia.\n"
			"JPG: Ideal para fotografías, no soporta transparencia, excelente compresión.\n"
			"PNG: Soporta transparencia, bueno para gráficos e imágenes con texto, compresión sin pérdida.\n\n"
			"Recomendaciones:\n"
			"• Para fotografías web: WebP\n"
			"• Para fotografías con máxima calidad: PNG\n"
			"• Para compatibilidad: JPG\n"
			"• Para imágenes con transparencia: WebP o PNG"
		)
		
		# Usar messagebox para mostrar información
		messagebox.showinfo("Información de Formatos", info)
	
	def mostrar_acerca_de (self):
		"""Muestra información acerca de la aplicación"""
		mensaje = (
			"Convertidor de Imágenes Avanzado\n"
			"Versión 2.0\n\n"
			"Una aplicación para convertir imágenes entre diferentes formatos\n"
			"con opciones avanzadas de optimización.\n\n"
			"© 2025 Todos los derechos reservados"
		)
		messagebox.showinfo("Acerca de", mensaje)
	
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
		if self.archivo_seleccionado:
			self.mostrar_vista_previa()
	
	def seleccionar_origen (self):
		"""Selecciona una carpeta de origen y muestra una vista previa"""
		carpeta = filedialog.askdirectory(title = "Selecciona la carpeta con imágenes originales")
		if carpeta:
			self.carpeta_origen.set(carpeta)
			
			# Buscar la primera imagen para vista previa
			formatos_soportados = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif']
			archivos_encontrados = False
			for archivo in os.listdir(carpeta):
				if archivo.lower().endswith(tuple(formatos_soportados)):
					self.archivo_seleccionado = os.path.join(carpeta, archivo)
					self.mostrar_vista_previa()
					archivos_encontrados = True
					break
			
			if not archivos_encontrados:
				messagebox.showinfo("Información", "No se encontraron imágenes en la carpeta seleccionada.")
	
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
			
			if self.modo_vista_previa.get() == "simple":
				# Limpiar el contenedor de vista previa
				for widget in self.preview_container.winfo_children():
					widget.destroy()
				
				# Marco para la vista previa con borde
				preview_frame = Frame(self.preview_container, borderwidth = 2, relief = "solid")
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
			else:
				# Modo comparativo - actualizar primera imagen
				if isinstance(self.preview_original_label, ttk.Label):
					# Crear una nueva etiqueta para la imagen
					parent = self.preview_original_label.master
					self.preview_original_label = Label(parent, image = self.vista_previa_imagen)
					self.preview_original_label.image = self.vista_previa_imagen
					self.preview_original_label.pack(pady = 10, expand = True)
			
			# Crear versión convertida temporal para comparación
			try:
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
				
				# Si estamos en modo comparativo, mostrar la imagen convertida
				if self.modo_vista_previa.get() == "comparativa":
					img_conv = Image.open(ruta_temp)
					img_conv_preview = self.redimensionar_para_vista_previa(img_conv, 350)
					self.vista_previa_convertida = ImageTk.PhotoImage(img_conv_preview)
					
					if isinstance(self.preview_converted_label, ttk.Label):
						# Crear nueva etiqueta para la imagen convertida
						parent = self.preview_converted_label.master
						self.preview_converted_label.destroy()
						self.preview_converted_label = Label(parent, image = self.vista_previa_convertida)
						self.preview_converted_label.image = self.vista_previa_convertida
						self.preview_converted_label.pack(pady = 10, expand = True)
				
				# Mostrar información de tamaño
				tamano_orig = os.path.getsize(self.archivo_seleccionado)
				tamano_conv = os.path.getsize(ruta_temp)
				ahorro = 100 - (tamano_conv / tamano_orig * 100) if tamano_orig > 0 else 0
				
				self.info_original.config(text = f"Tamaño original: {self.formato_tamano(tamano_orig)}")
				self.info_convertido.config(text = f"Tamaño convertido: {self.formato_tamano(tamano_conv)}")
				self.info_ahorro.config(
						text = f"Ahorro: {ahorro:.1f}% ({self.formato_tamano(tamano_orig - tamano_conv)})")
				
				# Eliminar archivo temporal
				os.remove(ruta_temp)
			except Exception as e:
				print(f"Error en vista previa convertida: {str(e)}")
				if self.modo_vista_previa.get() == "comparativa":
					# Mostrar mensaje de error
					if isinstance(self.preview_converted_label, ttk.Label):
						self.preview_converted_label.config(text = f"Error: {str(e)}")
		
		except Exception as e:
			self.mostrar_mensaje_vista_previa(f"Error al generar vista previa: {str(e)}")
			print(f"Error en mostrar_vista_previa: {str(e)}")
	
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
	
	def redimensionar_para_vista_previa(self, imagen, tamano_max):
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
		self.porcentaje_progreso.set("0%")
		
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
		
		# Confirmación con detalles de la operación
		mensaje = (
			f"Se convertirán {self.total_archivos} imágenes\n"
			f"Formato: {self.formato_salida.get().upper()}\n"
			f"Calidad: {self.calidad_webp.get()}%\n"
			f"Destino: {carpeta_destino}\n\n"
			"¿Desea continuar con la conversión?"
		)
		
		if not messagebox.askyesno("Confirmar conversión", mensaje):
			return
		
		# Iniciar tiempo
		self.tiempo_inicio = time.time()
		
		# Deshabilitar botones durante la conversión
		self.boton_convertir.config(state = "disabled")
		
		# Añadir animación a la barra de progreso
		self.barra_progreso.config(mode = "indeterminate")
		self.barra_progreso.start(10)
		
		# Actualizar estado
		self.estado.set(f"Iniciando conversión de {self.total_archivos} archivos...")
		
		# Iniciar conversión en hilo separado
		threading.Thread(target = self.procesar_lote, args = (carpeta_destino, archivos)).start()
	
	def procesar_lote (self, carpeta_destino, archivos):
		"""Procesa un lote de imágenes en paralelo"""
		try:
			# Actualizar interfaz
			self.estado.set(f"Procesando {len(archivos)} archivos...")
			self.progreso.set(0)
			
			# Cambiar la barra a modo determinado después de iniciar
			self.root.after(1000, lambda: self.barra_progreso.config(mode = "determinate"))
			self.root.after(1000, lambda: self.barra_progreso.stop())
			
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
					
					try:
						tamano_orig, tamano_nuevo = future.result()
						self.tamano_original += tamano_orig
						self.tamano_nuevo += tamano_nuevo
						self.archivos_procesados += 1
						
						# Actualizar progreso
						porcentaje = (self.archivos_procesados / self.total_archivos) * 100
						self.root.after(10, lambda p = porcentaje: self.actualizar_progreso(p))
						
						# Actualizar estadísticas cada 3 archivos o al final
						if self.archivos_procesados % 3 == 0 or self.archivos_procesados == self.total_archivos:
							self.root.after(10, self.actualizar_estadisticas)
					except Exception as e:
						print(f"Error procesando archivo: {str(e)}")
			
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
				
				# Añadir a historial
				self.historial_conversiones.append({
					"fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
					"archivos": self.archivos_procesados,
					"formato": self.formato_salida.get(),
					"ahorro": self.calcular_porcentaje_ahorro()
				})
				
				# Mostrar mensaje de finalización con estilo mejorado
				self.root.after(100, self.mostrar_resumen_conversion)
		
		except Exception as e:
			print(f"Error en procesar_lote: {str(e)}")
			import traceback
			traceback.print_exc()
			self.root.after(0, lambda: messagebox.showerror("Error en procesamiento",
			                                                f"Ocurrió un error durante la conversión: {str(e)}"))
			self.root.after(0, lambda: self.boton_convertir.config(state = "normal"))
	
	def actualizar_progreso (self, porcentaje):
		"""Actualiza la barra de progreso y el porcentaje"""
		self.progreso.set(porcentaje)
		self.porcentaje_progreso.set(f"{porcentaje:.1f}%")
	
	def actualizar_estadisticas(self):
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
	
	def convertir_imagen (self, ruta_origen, ruta_destino):
		"""Convierte una imagen y devuelve el tamaño original y nuevo"""
		try:
			# Obtener tamaño original
			tamano_orig = os.path.getsize(ruta_origen)
			
			# Abrir imagen
			imagen = Image.open(ruta_origen)
			
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
				imagen.save(ruta_destino, "JPEG", quality = self.calidad_webp.get())
			elif formato == 'png':
				imagen.save(ruta_destino, "PNG")
			
			# Obtener tamaño nuevo
			tamano_nuevo = os.path.getsize(ruta_destino)
			
			# Actualizar estado con información del archivo actual
			nombre_archivo = os.path.basename(ruta_origen)
			ahorro_ind = 100 - (tamano_nuevo / tamano_orig * 100) if tamano_orig > 0 else 0
			self.root.after(0, lambda: self.estado.set(
					f"Procesando: {nombre_archivo} → {ahorro_ind:.1f}% reducción"
			))
			
			return tamano_orig, tamano_nuevo
		
		except Exception as e:
			print(f"Error al convertir {os.path.basename(ruta_origen)}: {str(e)}")
			# No mostrar messagebox desde un hilo secundario, podría causar problemas
			# Solo propagar la excepción
			raise
	
	def cancelar_conversion (self):
		"""Cancela la conversión en curso"""
		self.cancelado = True
		self.estado.set("Cancelando...")
		messagebox.showinfo("Cancelando", "La conversión se cancelará en breve...")
	
	def mostrar_resumen_conversion (self):
		"""Muestra un resumen de la conversión con un diseño mejorado"""
		try:
			tiempo_total = time.time() - self.tiempo_inicio
			ahorro = self.calcular_porcentaje_ahorro()
			
			# Crear ventana de resumen
			ventana_resumen = tk.Toplevel(self.root)
			ventana_resumen.title("Conversión Completada")
			ventana_resumen.geometry("550x400")
			ventana_resumen.transient(self.root)  # Hacer que sea modal
			ventana_resumen.grab_set()  # Forzar foco en esta ventana
			
			# Frame principal
			frame_principal = Frame(ventana_resumen, bg = "#f5f5f5", padx = 20, pady = 20)
			frame_principal.pack(fill = "both", expand = True)
			
			# Título con ícono de éxito
			Label(frame_principal, text = "✓", font = ("Segoe UI", 24, "bold"),
			      bg = "#f5f5f5", fg = "#4CAF50").pack(side = "left", padx = (0, 10))
			
			Label(frame_principal, text = "¡Conversión completada con éxito!",
			      font = ("Segoe UI", 16, "bold"), bg = "#f5f5f5").pack(side = "left")
			
			# Separador
			Frame(frame_principal, height = 2, bg = "#e0e0e0").pack(fill = "x", pady = 15, expand = True)
			
			# Resumen en tabla
			tabla_frame = Frame(frame_principal, bg = "#f5f5f5")
			tabla_frame.pack(fill = "both", expand = True, pady = 10)
			
			# Filas de la tabla
			columna1_ancho = 20
			columna2_ancho = 25
			
			Label(tabla_frame, text = "Archivos procesados:", font = ("Segoe UI", 10, "bold"),
			      bg = "#f5f5f5", anchor = "w", width = columna1_ancho).grid(row = 0, column = 0, sticky = "w",
			                                                                 pady = 5)
			Label(tabla_frame, text = f"{self.archivos_procesados}",
			      bg = "#f5f5f5", anchor = "w", width = columna2_ancho).grid(row = 0, column = 1, sticky = "w",
			                                                                 pady = 5)
			
			Label(tabla_frame, text = "Formato de salida:", font = ("Segoe UI", 10, "bold"),
			      bg = "#f5f5f5", anchor = "w", width = columna1_ancho).grid(row = 1, column = 0, sticky = "w",
			                                                                 pady = 5)
			Label(tabla_frame, text = self.formato_salida.get().upper(),
			      bg = "#f5f5f5", anchor = "w", width = columna2_ancho).grid(row = 1, column = 1, sticky = "w",
			                                                                 pady = 5)
			
			Label(tabla_frame, text = "Tamaño original:", font = ("Segoe UI", 10, "bold"),
			      bg = "#f5f5f5", anchor = "w", width = columna1_ancho).grid(row = 2, column = 0, sticky = "w",
			                                                                 pady = 5)
			Label(tabla_frame, text = self.formato_tamano(self.tamano_original),
			      bg = "#f5f5f5", anchor = "w", width = columna2_ancho).grid(row = 2, column = 1, sticky = "w",
			                                                                 pady = 5)
			
			Label(tabla_frame, text = "Tamaño nuevo:", font = ("Segoe UI", 10, "bold"),
			      bg = "#f5f5f5", anchor = "w", width = columna1_ancho).grid(row = 3, column = 0, sticky = "w",
			                                                                 pady = 5)
			Label(tabla_frame, text = self.formato_tamano(self.tamano_nuevo),
			      bg = "#f5f5f5", anchor = "w", width = columna2_ancho).grid(row = 3, column = 1, sticky = "w",
			                                                                 pady = 5)
			
			Label(tabla_frame, text = "Ahorro:", font = ("Segoe UI", 10, "bold"),
			      bg = "#f5f5f5", anchor = "w", width = columna1_ancho).grid(row = 4, column = 0, sticky = "w",
			                                                                 pady = 5)
			Label(tabla_frame,
			      text = f"{ahorro:.1f}% ({self.formato_tamano(self.tamano_original - self.tamano_nuevo)})",
			      fg = "#4CAF50", bg = "#f5f5f5", anchor = "w", width = columna2_ancho).grid(row = 4, column = 1,
			                                                                                 sticky = "w", pady = 5)
			
			Label(tabla_frame, text = "Tiempo:", font = ("Segoe UI", 10, "bold"),
			      bg = "#f5f5f5", anchor = "w", width = columna1_ancho).grid(row = 5, column = 0, sticky = "w",
			                                                                 pady = 5)
			Label(tabla_frame, text = f"{tiempo_total:.1f} segundos",
			      bg = "#f5f5f5", anchor = "w", width = columna2_ancho).grid(row = 5, column = 1, sticky = "w",
			                                                                 pady = 5)
			
			# Frame para botones
			botones_frame = Frame(frame_principal, bg = "#f5f5f5")
			botones_frame.pack(fill = "x", pady = 15)
			
			ttk.Button(botones_frame, text = "Abrir carpeta de destino",
			           command = lambda: os.startfile(self.carpeta_destino.get())).pack(side = "left", padx = 5)
			
			ttk.Button(botones_frame, text = "Cerrar",
			           command = ventana_resumen.destroy).pack(side = "right", padx = 5)
		
		except Exception as e:
			print(f"Error en mostrar_resumen_conversion: {str(e)}")
			import traceback
			traceback.print_exc()


def main ():
	try:
		print("Iniciando aplicación...")
		root = tk.Tk()
		app = ImageConverterApp(root)
		print("Interfaz creada, iniciando mainloop()...")
		root.mainloop()
		print("Aplicación cerrada normalmente")
	except Exception as e:
		print(f"ERROR: {str(e)}")
		import traceback
		traceback.print_exc()
		messagebox.showerror("Error crítico", f"Se produjo un error crítico: {str(e)}")
		input("Presiona Enter para salir...")


if __name__ == "__main__":
	main().destroy()
	self.preview_original_label