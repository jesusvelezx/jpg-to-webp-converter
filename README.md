# 🖼️ JPG to WebP Converter

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Pillow Version](https://img.shields.io/badge/Pillow-8.0+-green.svg)](https://python-pillow.org/)

Una herramienta sencilla, pero potente para convertir imágenes JPG a formato WebP, reduciendo el tamaño de archivo mientras mantiene una excelente calidad visual.

## ✨ Características

- **Conversión eficiente**: Transforma imágenes JPG al formato WebP, logrando hasta un 34% de reducción de tamaño
- **Preserva la calidad**: Mantiene la calidad visual mientras optimiza el peso de los archivos
- **Procesamiento por lotes**: Convierte múltiples imágenes con un solo comando
- **Fácil de usar**: Interfaz simple a través de línea de comandos
- **Personalizable**: Ajusta el nivel de compresión según tus necesidades

## 🚀 Instalación

1. Clona este repositorio:
```bash
git clone https://github.com/tu-usuario/jpg-to-webp-converter.git
cd jpg-to-webp-converter
```
2. Instala las dependencias:
```bash
pip install pillow
```

## 💻 Uso

Ejecuta el script principal con Python:

```bash
python convertidor.py
```

### Argumentos opcionales

- `--input`: Carpeta de origen con las imágenes JPG (por defecto:“./input”)
- `--output`: Carpeta de destino para las imágenes WebP (por defecto:“./output”)
- `--quality`: Nivel de calidad WebP (0-100, por defecto: 80)

Ejemplo:
```bash
python convertidor.py --input ./mis_fotos --output ./fotos_optimizadas --quality 75
```

## 📊 Comparación de formatos

| Formato | Tamaño promedio | Soporte en navegadores | Transparencia | Animación |
|---------|-----------------|------------------------|---------------|-----------|
| JPG     | Medio           | Todos                  | No            | No        |
| WebP    | Bajo            | Modernos               | Sí            | Sí        |
| PNG     | Alto            | Todos                  | Sí            | No        |

## 🔧 Requisitos

- Python 3.6 o superior
- Pillow (PIL Fork) 8.0 o superior

## 👥 Contribuciones

Las contribuciones son bienvenidas. Por favor, siente libre de:

1. Hacer un fork del proyecto
2. Crear una rama para tu funcionalidad (`git checkout -b feature/amazing-feature`)
3. Commit de tus cambios (`git commit -m 'Add some amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abrir un Pull Request


_________

⭐️ **¡No olvides darle una estrella al proyecto si te fue útil!** ⭐️