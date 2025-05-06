# 🖼️ JPG to WebP Converter

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Pillow Version](https://img.shields.io/badge/Pillow-8.0+-green.svg)](https://python-pillow.org/)
[![piexif](https://img.shields.io/badge/piexif-1.1.3+-orange.svg)](https://pypi.org/project/piexif/)
[![matplotlib](https://img.shields.io/badge/matplotlib-3.5.0+-red.svg)](https://matplotlib.org/)

Una herramienta sencilla, pero potente para convertir imágenes JPG a formato WebP, reduciendo el tamaño de archivo mientras mantiene una excelente calidad visual.

![Vista Previa de la Aplicación](https://raw.githubusercontent.com/username/image-converter/main/preview.png)

## ✨ Características

- **Conversión entre múltiples formatos**: WebP, PNG, JPG, AVIF y HEIF
- **Interfaz gráfica completa**: Fácil de usar con paneles organizados para configuración y vista previa
- **Control de calidad ajustable**: Optimiza el equilibrio entre calidad y tamaño de archivo
- **Vista previa en tiempo real**: Visualiza los resultados antes de procesar todo el lote
- **Procesamiento multi-núcleo**: Aprovecha todos los núcleos de la CPU para conversiones rápidas
- **Estadísticas detalladas**: Información sobre ahorro de espacio y tiempo de procesamiento
- **Redimensionado inteligente**: Opción para redimensionar imágenes manteniendo la proporción
- **Preservación de metadatos**: Mantiene la información EXIF de las imágenes originales
- **Reporte gráfico**: Genera automáticamente un gráfico comparativo del ahorro de espacio

## 🛠️ Requisitos

- Python 3.6 o superior
- Bibliotecas requeridas (se instalan automáticamente si es necesario):
  - Pillow 8.0+ (PIL)
  - piexif 1.1.3+
  - matplotlib 3.5.0+

## 📥 Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/username/jpg-to-webp-converter.git
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
   python image_converter.py
   ```

2. Selecciona la carpeta de origen con tus imágenes

3. Elige la carpeta de destino para las imágenes convertidas

4. Configura las opciones de conversión:
   - Formato de salida (WebP, PNG, JPG, AVIF, HEIF)
   - Calidad de compresión (0-100%)
   - Preservación de metadatos
   - Redimensionado (opcional)

5. Utiliza la función "Vista previa" para verificar los resultados en una imagen

6. Haz clic en "Convertir" para procesar todas las imágenes

## 📖 Guía Detallada

### Configuración Inicial

- **Carpeta de origen**: Contiene las imágenes a convertir (JPG, JPEG, PNG, BMP, TIFF, GIF)
- **Carpeta de destino**: Donde se guardarán las imágenes convertidas
- **Formato de salida**: Selecciona entre WebP, PNG, JPG, AVIF o HEIF
- **Calidad**: Ajusta la calidad de compresión para formatos con pérdida (WebP, JPG, AVIF, HEIF)

### Opciones Avanzadas

- **Conservar metadatos**: Mantiene información EXIF como fecha de captura, datos de la cámara, etc.
- **Redimensionar imágenes**: Reduce el tamaño de las imágenes manteniendo la proporción
- **Ancho máximo**: Define el ancho máximo para el redimensionado

### Vista Previa

Antes de procesar todo el lote, puedes ver cómo quedaría una imagen después de la conversión:

1. Selecciona una imagen para vista previa
2. Verifica la calidad visual resultante
3. Compara el tamaño original vs. el tamaño convertido
4. Observa el porcentaje de ahorro de espacio

### Estadísticas y Reportes

Al finalizar la conversión, la aplicación muestra:

- Total de archivos procesados
- Tamaño original acumulado
- Tamaño nuevo acumulado
- Porcentaje de ahorro total
- Tiempo de procesamiento
- Gráfico comparativo (se guarda automáticamente)

## 🎯 Por Qué Usar Este Convertidor

- **Ahorro de espacio**: Reduce significativamente el tamaño de tus imágenes sin pérdida notable de calidad
- **Formatos modernos**: Soporte para formatos de imagen de última generación
- **Eficiencia**: Procesamiento en paralelo para conversiones rápidas
- **Facilidad de uso**: Interfaz intuitiva sin necesidad de conocimientos técnicos
- **Control total**: Ajusta la calidad y tamaño según tus necesidades específicas

## 👥 Contribuciones

¡Las contribuciones son bienvenidas! Si tienes alguna idea para mejorar esta aplicación:

1. Haz un fork del repositorio
2. Crea una rama para tu característica (`git checkout -b feature/nueva-caracteristica`)
3. Haz commit de tus cambios (`git commit -am 'Añadir nueva característica'`)
4. Haz push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

## 📱 Capturas de Pantalla

![Interfaz principal](https://raw.githubusercontent.com/username/jpg-to-webp-converter/main/screenshots/main-ui.png)
![Vista previa de conversión](https://raw.githubusercontent.com/username/jpg-to-webp-converter/main/screenshots/preview.png)
![Estadísticas](https://raw.githubusercontent.com/username/jpg-to-webp-converter/main/screenshots/stats.png)

## 📝 Licencia

Este proyecto está licenciado bajo [MIT License](LICENSE).

## 📊 Estadísticas de Uso

![GitHub stars](https://img.shields.io/github/stars/username/jpg-to-webp-converter?style=social)
![GitHub forks](https://img.shields.io/github/forks/username/jpg-to-webp-converter?style=social)
![GitHub issues](https://img.shields.io/github/issues/username/jpg-to-webp-converter)
![GitHub pull requests](https://img.shields.io/github/issues-pr/username/jpg-to-webp-converter)