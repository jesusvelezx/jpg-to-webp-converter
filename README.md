# 🖼️ JPG to WebP Converter

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Pillow Version](https://img.shields.io/badge/Pillow-8.0+-green.svg)](https://python-pillow.org/)
[![piexif](https://img.shields.io/badge/piexif-1.1.3+-orange.svg)](https://pypi.org/project/piexif/)
[![matplotlib](https://img.shields.io/badge/matplotlib-3.5.0+-red.svg)](https://matplotlib.org/)

Una herramienta sencilla, pero potente para convertir imágenes JPG a formato WebP, reduciendo el tamaño de archivo mientras mantiene una excelente calidad visual.

![Vista Previa de la Aplicación](https://github.com/jesusvelezx/jpg-to-webp-converter/blob/main/screenshots/main-ui.png)

## ✨ Características

- **Conversión entre múltiples formatos**: WebP, PNG, JPG, AVIF y HEIF
- **Interfaz gráfica moderna**: Fácil de usar con diseño intuitivo y elementos visuales mejorados
- **Control de calidad ajustable**: Optimiza el equilibrio entre calidad y tamaño de archivo
- **Vista previa en tiempo real**: Visualiza los cambios automáticamente sin necesidad de clics adicionales
- **Selección flexible**: Elige entre procesar carpetas completas o archivos individuales específicos
- **Navegación de imágenes**: Sistema integrado para navegar entre múltiples imágenes seleccionadas
- **Procesamiento multi-núcleo**: Aprovecha todos los núcleos de la CPU para conversiones rápidas
- **Estadísticas detalladas**: Información sobre ahorro de espacio y tiempo de procesamiento
- **Redimensionado inteligente**: Opción para redimensionar imágenes manteniendo la proporción
- **Preservación de metadatos**: Mantiene la información EXIF de las imágenes originales
- **Reporte gráfico mejorado**: Genera automáticamente un gráfico comparativo del ahorro de espacio con diseño visualmente atractivo

## 🛠️ Requisitos

- Python 3.6 o superior
- Bibliotecas requeridas (se instalan automáticamente si es necesario):
  - Pillow 8.0+ (PIL)
  - piexif 1.1.3+
  - matplotlib 3.5.0+

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
   python convertidor.py
   ```

2. Elige el modo de selección:
   - **Modo carpeta**: Selecciona una carpeta completa con imágenes
   - **Modo archivos**: Selecciona imágenes individuales específicas

3. Selecciona la carpeta de destino para las imágenes convertidas

4. Configura las opciones de conversión:
   - Formato de salida (WebP, PNG, JPG, AVIF, HEIF)
   - Calidad de compresión (0-100%)
   - Preservación de metadatos
   - Redimensionado (opcional)

5. La vista previa se actualiza automáticamente al cambiar cualquier configuración

6. Haz clic en "Convertir" para procesar todas las imágenes

## 📖 Guía Detallada

### Configuración Inicial

- **Modo de selección**: Elige entre procesar una carpeta o archivos específicos
- **Origen**: Carpeta o archivos individuales para convertir (JPG, JPEG, PNG, BMP, TIFF, GIF)
- **Destino**: Donde se guardarán las imágenes convertidas
- **Formato de salida**: Selecciona entre WebP, PNG, JPG, AVIF o HEIF
- **Calidad**: Ajusta la calidad de compresión para formatos con pérdida (WebP, JPG, AVIF, HEIF)

### Opciones Avanzadas

- **Conservar metadatos**: Mantiene información EXIF como fecha de captura, datos de la cámara, etc.
- **Redimensionar imágenes**: Reduce el tamaño de las imágenes manteniendo la proporción
- **Ancho máximo**: Define el ancho máximo para el redimensionado

### Vista Previa Automática

La aplicación ahora muestra automáticamente una vista previa:

1. Al seleccionar un archivo o carpeta, se muestra una vista previa instantánea
2. Al cambiar cualquier configuración (formato, calidad, redimensionado), la vista previa se actualiza
3. Visualiza el nombre del archivo, dimensiones originales y comparativa de tamaños
4. Con múltiples imágenes, navega entre ellas con botones "Anterior/Siguiente"

### Estadísticas y Reportes Mejorados

Al finalizar la conversión, la aplicación muestra:

- Total de archivos procesados
- Tamaño original acumulado
- Tamaño nuevo acumulado
- Porcentaje de ahorro total
- Tiempo de procesamiento
- Ventana de resumen detallado con diseño atractivo
- Gráfico comparativo mejorado (se guarda automáticamente)

## 🎯 Por Qué Usar Este Convertidor

- **Ahorro de espacio**: Reduce significativamente el tamaño de tus imágenes sin pérdida notable de calidad
- **Formatos modernos**: Soporte para formatos de imagen de última generación
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

### Versión 2.0.0
- **Nueva interfaz moderna**: Diseño más limpio y elementos visuales mejorados
- **Previsualización automática**: Las imágenes se previsualizan instantáneamente al seleccionarlas
- **Selección de archivos individuales**: Ahora puedes elegir archivos específicos en lugar de carpetas completas
- **Sistema de navegación**: Botones Anterior/Siguiente para navegar entre múltiples imágenes
- **Lista visual de archivos**: Vista de lista para seleccionar rápidamente entre las imágenes cargadas
- **Indicador de progreso mejorado**: Mejor visualización del progreso durante la conversión
- **Resumen de conversión mejorado**: Ventana de resumen más atractiva y detallada
- **Gráficos estadísticos mejorados**: Diseño visual más atractivo para los gráficos de ahorro
- **Correcciones de errores**: Solucionados problemas de sintaxis y mejorado el manejo de excepciones

## 📝 Licencia

Este proyecto está licenciado bajo [MIT License](LICENSE).

## 📊 Estadísticas de Uso

![GitHub stars](https://img.shields.io/github/stars/jesusvelezx/jpg-to-webp-converter?style=social)
![GitHub forks](https://img.shields.io/github/forks/jesusvelezx/jpg-to-webp-converter?style=social)
![GitHub issues](https://img.shields.io/github/issues/jesusvelezx/jpg-to-webp-converter)
![GitHub pull requests](https://img.shields.io/github/issues-pr/jesusvelezx/jpg-to-webp-converter)
