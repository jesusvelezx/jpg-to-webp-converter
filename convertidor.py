import os
import time
import threading
import concurrent.futures
from tkinter import Tk, Frame, Button, Label, Scale, StringVar, DoubleVar, IntVar, HORIZONTAL, BooleanVar
from tkinter import ttk, messagebox, filedialog, PhotoImage, LabelFrame
from PIL import Image, ImageTk
import piexif
from datetime import datetime
import matplotlib.pyplot as plt


class ImageConverterApp:
	def __init__ (self, root):
		self.root = root
		self.root.title("Convertidor de Imágenes Avanzado")
		self.root.geometry("950x650")
		
		# Variables
		self.carpeta_origen = StringVar( )
		self.carpeta_destino = StringVar( )
		self.calidad_webp = IntVar(value = 80)
		self.formato_salida = StringVar(value = "webp")
		self.progreso = DoubleVar(value = 0)
		self.estado = StringVar(value = "Listo para comenzar")
		self.conservar_metadatos = IntVar(value = 1)
		self.redimensionar = IntVar(value = 0)
		self.ancho_nuevo = IntVar(value = 1200)
		self.modo_seleccion = StringVar(value = "carpeta")  # Nueva variable para el modo de selección
		self.archivos_procesados = 0
		self.total_archivos = 0
		self.tamano_original = 0
		self.tamano_nuevo = 0
		self.tiempo_inicio = 0
		self.vista_previa_imagen = None
		self.archivo_seleccionado = None
		self.archivos_seleccionados = []  # Lista para almacenar múltiples archivos seleccionados
		
		# Crear interfaz
		self.crear_interfaz( )
	
	def crear_interfaz (self):
		# Frame principal
		main_frame = ttk.Frame(self.root, padding = "10")
		main_frame.pack(fill = "both", expand = True)
		
		# Estilo
		estilo = ttk.Style( )
		estilo.configure("TButton", padding = 5, font = ('Arial', 10))
		estilo.configure("TLabel", font = ('Arial', 10))
		estilo.configure("TRadiobutton", font = ('Arial', 10))
		
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
		
		# Ocultar el frame de archivos inicialmente
		self.origen_archivos_frame.grid_remove( )
		
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
		
		# Calidad
		ttk.Label(config_frame, text = "Calidad:").grid(row = 4, column = 0, sticky = "w", pady = 5)
		self.scale_calidad = Scale(config_frame, variable = self.calidad_webp, from_ = 0, to = 100,
		                           orient = HORIZONTAL, length = 200)
		self.scale_calidad.grid(row = 4, column = 1, sticky = "ew", pady = 5)
		self.label_calidad = ttk.Label(config_frame, text = "80%")
		self.label_calidad.grid(row = 4, column = 2, sticky = "w", pady = 5)
		self.calidad_webp.trace_add("write", self.actualizar_label_calidad)
		
		# Opciones adicionales en un LabelFrame
		opciones_frame = ttk.LabelFrame(config_frame, text = "Opciones adicionales", padding = "5")
		opciones_frame.grid(row = 5, column = 0, columnspan = 3, sticky = "ew", pady = 10)
		
		ttk.Checkbutton(opciones_frame, text = "Conservar metadatos", variable = self.conservar_metadatos).grid(
				row = 0, column = 0, columnspan = 2, sticky = "w", pady = 5)
		
		ttk.Checkbutton(opciones_frame, text = "Redimensionar imágenes", variable = self.redimensionar,
		                command = self.toggle_redimension).grid(row = 1, column = 0, columnspan = 2, sticky = "w",
		                                                        pady = 5)
		
		# Frame para opciones de redimensionado (inicialmente oculto)
		self.redim_frame = ttk.Frame(opciones_frame)
		self.redim_frame.grid(row = 2, column = 0, columnspan = 2, sticky = "w", pady = 5)
		ttk.Label(self.redim_frame, text = "Ancho máximo:").pack(side = "left")
		ttk.Entry(self.redim_frame, textvariable = self.ancho_nuevo, width = 6).pack(side = "left", padx = 5)
		ttk.Label(self.redim_frame, text = "px (se mantiene la proporción)").pack(side = "left")
		self.redim_frame.grid_remove( )
		
		# Botones de acción
		botones_frame = ttk.Frame(config_frame)
		botones_frame.grid(row = 6, column = 0, columnspan = 3, pady = 15)
		
		self.boton_convertir = ttk.Button(botones_frame, text = "Convertir", command = self.iniciar_conversion)
		self.boton_convertir.pack(side = "left", padx = 5)
		self.boton_vista_previa = ttk.Button(botones_frame, text = "Vista previa", command = self.mostrar_vista_previa)
		self.boton_vista_previa.pack(side = "left", padx = 5)
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
		
		ttk.Button(preview_frame, text = "Seleccionar imagen para vista previa",
		           command = self.seleccionar_imagen_preview).pack(pady = 5)
		
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
		
		# Inicialización
		self.cancelado = False
	
	def cambiar_modo_seleccion (self):
		"""Cambia entre modo de selección de carpeta y archivos"""
		modo = self.modo_seleccion.get( )
		
		if modo == "carpeta":
			self.origen_archivos_frame.grid_remove( )
			self.origen_carpeta_frame.grid( )
			self.carpeta_origen.set("")
			self.archivos_seleccionados = []
		else:  # modo == "archivos"
			self.origen_carpeta_frame.grid_remove( )
			self.origen_archivos_frame.grid( )
			self.carpeta_origen.set("")
			self.archivos_seleccionados = []
			self.archivos_label.config(text = "Ningún archivo seleccionado")
	
	def toggle_redimension (self):
		if self.redimensionar.get( ):
			self.redim_frame.grid( )
		else:
			self.redim_frame.grid_remove( )
	
	def actualizar_label_calidad (self, *args):
		self.label_calidad.config(text = f"{self.calidad_webp.get( )}%")
	
	def actualizar_opciones_formato (self, event):
		formato = self.formato_salida.get( )
		if formato in ['jpg', 'webp', 'avif', 'heif']:
			self.scale_calidad.config(state = 'normal')
			self.label_calidad.config(state = 'normal')
		else:
			self.scale_calidad.config(state = 'disabled')
			self.label_calidad.config(state = 'disabled')
	
	def seleccionar_origen (self):
		carpeta = filedialog.askdirectory(title = "Selecciona la carpeta con imágenes originales")
		if carpeta:
			self.carpeta_origen.set(carpeta)
	
	def seleccionar_archivos (self):
		archivos = filedialog.askopenfilenames(
				title = "Selecciona imágenes para convertir",
				filetypes = [("Imágenes", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff;*.gif")]
		)
		
		if archivos:
			self.archivos_seleccionados = list(archivos)
			if len(self.archivos_seleccionados) > 1:
				self.archivos_label.config(text = f"{len(self.archivos_seleccionados)} archivos seleccionados")
			else:
				self.archivos_label.config(text = os.path.basename(self.archivos_seleccionados[0]))
			
			# Establecer el archivo seleccionado para vista previa
			self.archivo_seleccionado = self.archivos_seleccionados[0]
	
	def seleccionar_destino (self):
		carpeta = filedialog.askdirectory(title = "Selecciona la carpeta de destino")
		if carpeta:
			self.carpeta_destino.set(carpeta)
	
	def seleccionar_imagen_preview (self):
		if self.modo_seleccion.get( ) == "carpeta":
			carpeta = self.carpeta_origen.get( )
			if not carpeta:
				messagebox.showwarning("Advertencia", "Primero selecciona una carpeta de origen.")
				return
			
			archivo = filedialog.askopenfilename(
					title = "Selecciona una imagen para vista previa",
					initialdir = carpeta,
					filetypes = [("Imágenes", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff;*.gif")]
			)
		else:  # modo archivos
			if not self.archivos_seleccionados:
				messagebox.showwarning("Advertencia", "Primero selecciona al menos un archivo.")
				return
			
			archivo = filedialog.askopenfilename(
					title = "Selecciona una imagen para vista previa",
					filetypes = [("Imágenes", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff;*.gif")]
			)
		
		if archivo:
			self.archivo_seleccionado = archivo
			self.mostrar_vista_previa( )
	
	def mostrar_vista_previa (self):
		if not self.archivo_seleccionado:
			if self.modo_seleccion.get( ) == "carpeta":
				if not self.carpeta_origen.get( ):
					messagebox.showwarning("Advertencia", "Primero selecciona una carpeta de origen.")
					return
				
				# Buscar la primera imagen en la carpeta
				for archivo in os.listdir(self.carpeta_origen.get( )):
					if archivo.lower( ).endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif')):
						self.archivo_seleccionado = os.path.join(self.carpeta_origen.get( ), archivo)
						break
				
				if not self.archivo_seleccionado:
					messagebox.showinfo("Información", "No se encontraron imágenes en la carpeta de origen.")
					return
			else:  # modo archivos
				if not self.archivos_seleccionados:
					messagebox.showwarning("Advertencia", "Primero selecciona al menos un archivo.")
					return
				self.archivo_seleccionado = self.archivos_seleccionados[0]
		
		try:
			# Mostrar imagen original
			img_original = Image.open(self.archivo_seleccionado)
			
			# Redimensionar para vista previa
			img_preview = self.redimensionar_para_vista_previa(img_original, 300)
			self.vista_previa_imagen = ImageTk.PhotoImage(img_preview)
			
			# Limpiar el contenedor de vista previa
			for widget in self.preview_container.winfo_children( ):
				widget.destroy( )
			
			# Crear nueva etiqueta con la imagen
			self.preview_label = Label(self.preview_container, image = self.vista_previa_imagen)
			self.preview_label.image = self.vista_previa_imagen
			self.preview_label.pack(pady = 10)
			
			# Añadir nombre del archivo
			ttk.Label(self.preview_container, text = os.path.basename(self.archivo_seleccionado)).pack(pady = 5)
			
			# Crear versión convertida temporal para comparación
			nombre_temp = "temp_preview." + self.formato_salida.get( )
			ruta_temp = os.path.join(os.path.dirname(self.archivo_seleccionado), nombre_temp)
			
			# Aplicar configuraciones actuales
			img_convertida = img_original.copy( )
			
			# Redimensionar si está activado
			if self.redimensionar.get( ):
				ancho_orig = img_convertida.width
				alto_orig = img_convertida.height
				if ancho_orig > self.ancho_nuevo.get( ):
					ratio = self.ancho_nuevo.get( ) / ancho_orig
					nuevo_alto = int(alto_orig * ratio)
					img_convertida = img_convertida.resize((self.ancho_nuevo.get( ), nuevo_alto), Image.LANCZOS)
			
			# Guardar con las opciones configuradas
			if self.formato_salida.get( ) == 'webp':
				img_convertida.save(ruta_temp, 'WEBP', quality = self.calidad_webp.get( ))
			elif self.formato_salida.get( ) == 'jpg':
				img_convertida.save(ruta_temp, 'JPEG', quality = self.calidad_webp.get( ))
			elif self.formato_salida.get( ) == 'png':
				img_convertida.save(ruta_temp, 'PNG')
			elif self.formato_salida.get( ) == 'avif':
				img_convertida.save(ruta_temp, 'AVIF', quality = self.calidad_webp.get( ))
			elif self.formato_salida.get( ) == 'heif':
				img_convertida.save(ruta_temp, 'HEIF', quality = self.calidad_webp.get( ))
			
			# Mostrar información de tamaño
			tamano_orig = os.path.getsize(self.archivo_seleccionado)
			tamano_conv = os.path.getsize(ruta_temp)
			ahorro = 100 - (tamano_conv / tamano_orig * 100)
			
			self.info_original.config(text = f"Tamaño original: {self.formato_tamano(tamano_orig)}")
			self.info_convertido.config(text = f"Tamaño convertido: {self.formato_tamano(tamano_conv)}")
			self.info_ahorro.config(text = f"Ahorro: {ahorro:.1f}% ({self.formato_tamano(tamano_orig - tamano_conv)})")
			
			# Eliminar archivo temporal
			os.remove(ruta_temp)
		
		except Exception as e:
			messagebox.showerror("Error", f"Error al generar vista previa: {str(e)}")
	
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
		carpeta_destino = self.carpeta_destino.get( )
		
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
		if self.modo_seleccion.get( ) == "carpeta":
			carpeta_origen = self.carpeta_origen.get( )
			if not carpeta_origen:
				messagebox.showwarning("Advertencia", "Debes seleccionar una carpeta de origen.")
				return
			
			formatos_soportados = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif']
			archivos = [os.path.join(carpeta_origen, f) for f in os.listdir(carpeta_origen)
			            if os.path.isfile(os.path.join(carpeta_origen, f)) and
			            os.path.splitext(f)[1].lower( ) in formatos_soportados]
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
		self.tiempo_inicio = time.time( )
		
		# Deshabilitar botones durante la conversión
		self.boton_convertir.config(state = "disabled")
		self.boton_vista_previa.config(state = "disabled")
		
		# Iniciar conversión en hilo separado
		threading.Thread(target = self.procesar_lote, args = (carpeta_destino, archivos)).start( )
	
	def procesar_lote (self, carpeta_destino, archivos):
		# Actualizar interfaz
		self.estado.set(f"Procesando {len(archivos)} archivos...")
		self.progreso.set(0)
		
		# Usar ThreadPoolExecutor para procesamiento paralelo
		with concurrent.futures.ThreadPoolExecutor(max_workers = os.cpu_count( )) as executor:
			futures = []
			for archivo in archivos:
				if self.cancelado:
					break
				
				nombre_base = os.path.splitext(os.path.basename(archivo))[0]
				extension = "." + self.formato_salida.get( )
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
				
				tamano_orig, tamano_nuevo = future.result( )
				self.tamano_original += tamano_orig
				self.tamano_nuevo += tamano_nuevo
				self.archivos_procesados += 1
				
				# Actualizar progreso
				porcentaje = (self.archivos_procesados / self.total_archivos) * 100
				self.root.after(10, lambda p = porcentaje: self.progreso.set(p))
				
				# Actualizar estadísticas cada 5 archivos o al final
				if self.archivos_procesados % 5 == 0 or self.archivos_procesados == self.total_archivos:
					self.root.after(10, self.actualizar_estadisticas)
		
		# Finalizar
		tiempo_total = time.time( ) - self.tiempo_inicio
		
		# Habilitar botones nuevamente
		self.root.after(0, lambda: self.boton_convertir.config(state = "normal"))
		self.root.after(0, lambda: self.boton_vista_previa.config(state = "normal"))
		
		if self.cancelado:
			self.root.after(0, lambda: self.estado.set("Conversión cancelada."))
		else:
			self.root.after(0, lambda: self.estado.set(
					f"Conversión completada. {self.archivos_procesados} archivos procesados en {tiempo_total:.1f} segundos."
			))
			
			# Generar gráfico de ahorro
			self.generar_grafico_ahorro( )
			
			# Mostrar mensaje de finalización
			self.root.after(100, lambda: messagebox.showinfo("Completado",
			                                                 f"Conversión finalizada con éxito.\n\n"
			                                                 f"- Archivos procesados: {self.archivos_procesados}\n"
			                                                 f"- Tamaño original: {self.formato_tamano(self.tamano_original)}\n"
			                                                 f"- Tamaño nuevo: {self.formato_tamano(self.tamano_nuevo)}\n"
			                                                 f"- Ahorro: {self.calcular_porcentaje_ahorro( ):.1f}%\n"
			                                                 f"- Tiempo: {tiempo_total:.1f} segundos"
			                                                 ))
	
	def convertir_imagen (self, ruta_origen, ruta_destino):
		"""Convierte una imagen y devuelve el tamaño original y nuevo"""
		try:
			# Obtener tamaño original
			tamano_orig = os.path.getsize(ruta_origen)
			
			# Abrir imagen
			imagen = Image.open(ruta_origen)
			
			# Obtener metadatos si es necesario
			metadatos = None
			if self.conservar_metadatos.get( ) and ruta_origen.lower( ).endswith(('.jpg', '.jpeg', '.tiff')):
				try:
					metadatos = piexif.load(ruta_origen)
				except Exception:
					pass
			
			# Redimensionar si está activado
			if self.redimensionar.get( ):
				ancho_orig = imagen.width
				alto_orig = imagen.height
				if ancho_orig > self.ancho_nuevo.get( ):
					ratio = self.ancho_nuevo.get( ) / ancho_orig
					nuevo_alto = int(alto_orig * ratio)
					imagen = imagen.resize((self.ancho_nuevo.get( ), nuevo_alto), Image.LANCZOS)
			
			# Guardar con el formato elegido
			formato = self.formato_salida.get( )
			if formato == 'webp':
				imagen.save(ruta_destino, "WEBP", quality = self.calidad_webp.get( ))
			elif formato == 'jpg':
				if metadatos:
					exif_bytes = piexif.dump(metadatos)
					imagen.save(ruta_destino, "JPEG", quality = self.calidad_webp.get( ), exif = exif_bytes)
				else:
					imagen.save(ruta_destino, "JPEG", quality = self.calidad_webp.get( ))
			elif formato == 'png':
				imagen.save(ruta_destino, "PNG")
			elif formato == 'avif':
				imagen.save(ruta_destino, "AVIF", quality = self.calidad_webp.get( ))
			elif formato == 'heif':
				imagen.save(ruta_destino, "HEIF", quality = self.calidad_webp.get( ))
			
			# Obtener tamaño nuevo
			tamano_nuevo = os.path.getsize(ruta_destino)
			
			return tamano_orig, tamano_nuevo
		
		except Exception as e:
			print(f"Error al convertir {os.path.basename(ruta_origen)}: {e}")
			return 0, 0
	
	def cancelar_conversion (self):
		self.cancelado = True
		self.estado.set("Cancelando...")
	
	def actualizar_estadisticas (self):
		"""Actualiza los widgets de estadísticas"""
		if self.archivos_procesados > 0:
			# Actualizar etiquetas de estadísticas
			self.stats_total.config(text = f"Archivos procesados: {self.archivos_procesados} de {self.total_archivos}")
			
			if self.tamano_original > 0:
				ahorro = self.calcular_porcentaje_ahorro( )
				ahorro_abs = self.tamano_original - self.tamano_nuevo
				
				self.stats_tamano.config(
						text = f"Reducción: {ahorro:.1f}% ({self.formato_tamano(ahorro_abs)})"
				)
			
			tiempo_actual = time.time( ) - self.tiempo_inicio
			self.stats_tiempo.config(text = f"Tiempo: {tiempo_actual:.1f} segundos")
	
	def calcular_porcentaje_ahorro (self):
		"""Calcula el porcentaje de ahorro"""
		if self.tamano_original > 0:
			return 100 - (self.tamano_nuevo / self.tamano_original * 100)
		return 0
	
	def generar_grafico_ahorro (self):
		"""Genera un gráfico de comparación de tamaños"""
		try:
			# Crear figura y ejes
			fig, ax = plt.subplots(figsize = (4, 3), dpi = 80)
			
			# Datos
			formatos = ['Original', self.formato_salida.get( ).upper( )]
			tamanos = [self.tamano_original / (1024 * 1024), self.tamano_nuevo / (1024 * 1024)]
			
			# Crear gráfico de barras
			barras = ax.bar(formatos, tamanos, color = ['#ff9999', '#66b3ff'])
			
			# Añadir etiquetas
			ax.set_ylabel('Tamaño (MB)')
			ax.set_title('Comparación de tamaños')
			
			# Añadir texto con el valor
			for i, barra in enumerate(barras):
				altura = barra.get_height( )
				ax.text(barra.get_x( ) + barra.get_width( ) / 2., altura + 0.05,
				        f'{altura:.2f} MB', ha = 'center', va = 'bottom')
			
			# Añadir texto con el porcentaje de ahorro
			ahorro = self.calcular_porcentaje_ahorro( )
			ax.text(0.5, 0.9, f'Ahorro: {ahorro:.1f}%',
			        transform = ax.transAxes, ha = 'center',
			        bbox = dict(facecolor = 'white', alpha = 0.8))
			
			# Guardar gráfico en un archivo temporal
			ruta_grafico = os.path.join(os.path.dirname(self.carpeta_destino.get( )),
			                            f"estadisticas_{datetime.now( ).strftime('%Y%m%d_%H%M%S')}.png")
			fig.savefig(ruta_grafico)
			
			# Mostrar mensaje con la ubicación del gráfico
			messagebox.showinfo("Estadísticas guardadas",
			                    f"Se ha guardado un gráfico con las estadísticas en:\n{ruta_grafico}")
		
		except Exception as e:
			print(f"Error al generar gráfico: {e}")


# Comprobar si se tienen las bibliotecas necesarias
def verificar_dependencias ( ):
	dependencias = {
		"piexif": "piexif",
		"matplotlib": "matplotlib"
	}
	
	for modulo, paquete in dependencias.items( ):
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
def main ( ):
	if verificar_dependencias( ):
		root = Tk( )
		app = ImageConverterApp(root)
		root.mainloop( )


if __name__ == "__main__":
	main()