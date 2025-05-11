# 🖼️ Convertidor de Imágenes Avanzado

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Pillow Version](https://img.shields.io/badge/Pillow-9.0+-green.svg)](https://python-pillow.org/)

Una herramienta sencilla pero potente para convertir imágenes entre diferentes formatos, reduciendo el tamaño de archivo mientras mantiene una excelente calidad visual.

![Vista Previa de la Aplicación](https://github.com/jesusvelezx/jpg-to-webp-converter/blob/main/screenshots/main-ui.png)

## ✨ Características

- **Conversión entre múltiples formatos**: WebP, PNG, JPG
- **Interfaz gráfica moderna**: Fácil de usar con diseño intuitivo y elementos visuales mejorados
- **Menú superior organizado**: Opciones agrupadas por categorías (Archivo, Convertir, Ver, Ayuda)
- **Control de calidad ajustable**: Optimiza el equilibrio entre calidad y tamaño de archivo
- **Vista previa mejorada**: Dos modos de visualización (simple y comparativa lado a lado)
- **Previsualización automática**: Visualiza los cambios automáticamente al modificar cualquier configuración
- **Selección flexible**: Elige entre procesar carpetas completas o archivos individuales específicos
- **Navegación de imágenes**: Sistema integrado para navegar entre múltiples imágenes seleccionadas
- **Procesamiento multi-núcleo**: Aprovecha todos los núcleos de la CPU para conversiones rápidas
- **Estadísticas detalladas**: Información estructurada sobre ahorro de espacio y tiempo de procesamiento
- **Barra de progreso mejorada**: Visualización del progreso con porcentaje numérico
- **Redimensionado inteligente**: Opción para redimensionar imágenes manteniendo la proporción
- **Resumen mejorado de conversión**: Ventana de resumen detallada con toda la información relevante

## 🛠️ Requisitos

- Python 3.6 o superior
- Bibliotecas requeridas (se instalan automáticamente si es necesario):
  - Pillow 9.0+

## 📥 Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/jesusvelezx/jpg-to-webp-converter
   ```

2. Navega al directorio del proyecto:
   ```bash
   cd jpg-to-webp-converter
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Uso

1. Ejecuta la aplicación:
   ```bash
   python convertidor_mejorado.py
   ```

2. Desde el menú superior accede a todas las funcionalidades organizadas por categorías:
   - **Archivo**: Selección de origen/destino y salir
   - **Convertir**: Iniciar/cancelar conversión y selección de formato
   - **Ver**: Cambiar entre modos de vista previa (simple o comparativa)
   - **Ayuda**: Información sobre formatos y acerca del programa

3. Elige el modo de selección:
   - **Modo carpeta**: Selecciona una carpeta completa con imágenes
   - **Modo archivos**: Selecciona imágenes individuales específicas

4. Selecciona la carpeta de destino para las imágenes convertidas

5. Configura las opciones de conversión:
   - Formato de salida (WebP, PNG, JPG)
   - Calidad de compresión (0-100%)
   - Redimensionado (opcional)

6. La vista previa se actualiza automáticamente al cambiar cualquier configuración

7. Haz clic en "Convertir" para procesar todas las imágenes

## 📖 Guía Detallada

### Menú Superior

- **Archivo**: Opciones para gestionar archivos y carpetas
  - Seleccionar carpeta de origen
  - Seleccionar archivos
  - Seleccionar carpeta de destino
  - Salir

- **Convertir**: Opciones relacionadas con la conversión
  - Iniciar conversión
  - Cancelar conversión
  - Formato de salida (submenú para seleccionar formato)

- **Ver**: Opciones de visualización
  - Vista previa simple (imagen única)
  - Vista previa comparativa (original vs convertida)

- **Ayuda**: Información y ayuda
  - Acerca de formatos de imagen
  - Acerca de la aplicación

### Configuración Inicial

- **Modo de selección**: Elige entre procesar una carpeta o archivos específicos
- **Origen**: Carpeta o archivos individuales para convertir (JPG, JPEG, PNG, BMP, TIFF, GIF)
- **Destino**: Donde se guardarán las imágenes convertidas
- **Formato de salida**: Selecciona entre WebP, PNG, JPG
- **Calidad**: Ajusta la calidad de compresión para formatos con pérdida (WebP, JPG)

### Opciones Avanzadas

- **Redimensionar imágenes**: Reduce el tamaño de las imágenes manteniendo la proporción
- **Ancho máximo**: Define el ancho máximo para el redimensionado

### Visualización Mejorada

La aplicación ofrece múltiples vistas para analizar tus imágenes:

1. **Vista Previa**: Visualización simple de la imagen seleccionada
2. **Comparativa**: Vista lado a lado de la imagen original y la versión convertida
3. **Información**: Datos detallados sobre tamaños y ahorro

### Navegación Intuitiva

Con múltiples imágenes seleccionadas:
- Navega entre ellas con botones "Anterior/Siguiente"
- Listado visual de todos los archivos seleccionados
- Selección directa desde la lista para previsualizar

### Estadísticas y Resumen

Al finalizar la conversión, la aplicación muestra:

- Total de archivos procesados
- Tamaño original acumulado
- Tamaño nuevo acumulado
- Porcentaje de ahorro total
- Tiempo de procesamiento
- Ventana de resumen detallado con diseño atractivo
- Botón para abrir directamente la carpeta de destino

## 🎯 Por Qué Usar Este Convertidor

- **Interfaz mejorada**: Menú superior organizado y elementos visuales optimizados
- **Ahorro de espacio**: Reduce significativamente el tamaño de tus imágenes sin pérdida notable de calidad
- **Vista previa dual**: Compara lado a lado la imagen original y convertida
- **Experiencia mejorada**: Previsualización automática y navegación intuitiva
- **Selección flexible**: Procesa carpetas completas o solo los archivos que necesitas
- **Eficiencia**: Procesamiento en paralelo para conversiones rápidas
- **Facilidad de uso**: Interfaz moderna e intuitiva sin necesidad de conocimientos técnicos
- **Control total**: Ajusta la calidad y tamaño según tus necesidades específicas

## 👥 Contribuciones

¡Las contribuciones son bienvenidas! Si tienes alguna idea para mejorar esta aplicación:

1. Haz un fork del repositorio
2. Crea una rama para tu característica (`git checkout -b feature/nueva-caracteristica`)
3. Haz commit de tus cambios (`git commit -am 'Añadir nueva característica'`)
4. Haz push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

## 📱 Capturas de Pantalla

![Interfaz principal](https://raw.githubusercontent.com/jesusvelezx/jpg-to-webp-converter/main/screenshots/main-ui.png)
![Vista previa de conversión](https://raw.githubusercontent.com/jesusvelezx/jpg-to-webp-converter/main/screenshots/preview.png)
![Estadísticas](https://raw.githubusercontent.com/jesusvelezx/jpg-to-webp-converter/main/screenshots/stats.png)

## 📋 Actualizaciones Recientes

### Versión 3.0.0
- **Menú superior organizativo**: Ahora con opciones agrupadas por categorías (Archivo, Convertir, Ver, Ayuda)
- **Vista previa comparativa**: Nueva vista lado a lado de la imagen original y convertida
- **Interfaz con pestañas**: Organización mejorada de vista previa, comparativa e información
- **Previsualización automática**: Actualización instantánea al cambiar cualquier configuración
- **Barra de progreso mejorada**: Visualización con porcentaje numérico e indicación de archivo en proceso
- **Ventana de resumen mejorada**: Información estructurada en formato de tabla para mejor legibilidad
- **Información detallada**: Datos de tamaño, ahorro y tiempo organizados por categorías
- **Botón para abrir carpeta**: Acceso directo a la carpeta de destino tras finalizar la conversión
- **Optimizado para estabilidad**: Mejor manejo de errores y compatibilidad mejorada
- **Dependencias reducidas**: Simplificación de requisitos para mejor compatibilidad

### Versión 2.0.0
- **Nueva interfaz moderna**: Diseño más limpio y elementos visuales mejorados
- **Previsualización automática**: Las imágenes se previsualizan instantáneamente al seleccionarlas
- **Selección de archivos individuales**: Ahora puedes elegir archivos específicos en lugar de carpetas completas
- **Sistema de navegación**: Botones Anterior/Siguiente para navegar entre múltiples imágenes
- **Lista visual de archivos**: Vista de lista para seleccionar rápidamente entre las imágenes cargadas
- **Indicador de progreso mejorado**: Mejor visualización del progreso durante la conversión
- **Resumen de conversión mejorado**: Ventana de resumen más atractiva y detallada
- **Correcciones de errores**: Solucionados problemas de sintaxis y mejorado el manejo de excepciones

## 📝 Licencia

Este proyecto está licenciado bajo [MIT License](LICENSE).

## 📊 Estadísticas de Uso

![GitHub stars](https://img.shields.io/github/stars/jesusvelezx/jpg-to-webp-converter?style=social)
![GitHub forks](https://img.shields.io/github/forks/jesusvelezx/jpg-to-webp-converter?style=social)
![GitHub issues](https://img.shields.io/github/issues/jesusvelezx/jpg-to-webp-converter)
![GitHub pull requests](https://img.shields.io/github/issues-pr/jesusvelezx/jpg-to-webp-converter)