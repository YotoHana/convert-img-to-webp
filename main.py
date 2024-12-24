import argparse
from PIL import Image
import os

parser = argparse.ArgumentParser(description="Конвертация изображения в Webp")

parser.add_argument('-q', '--quality', type=int, default=80, help='Качество изображения (1-100)')

parser.add_argument('path', type=str, help='Путь к входному файлу со списком путей к изображениям')

args = parser.parse_args()

def convert(input_path):
    img = Image.open(input_path)
    output_path = './Output/' + os.path.splitext(os.path.basename(input_path))[0] + '.webp'
    img.save(output_path, format='WEBP', quality=args.quality)

with open(args.path, "r") as file:
    content = file.read()
    paths = content.split("\n")

    os.makedirs('./Output', exist_ok=True)
    
    for i in paths:
        convert(i)