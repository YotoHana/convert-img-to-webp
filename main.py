from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QSlider, QListWidget, QFileDialog
from concurrent.futures import ThreadPoolExecutor
from PyQt5.QtCore import Qt
from PIL import Image
import sys
import os

file_list = []
temp_file_list = []

def update_slider_lable(value):
    slider_label.setText("Качество: " + str(value))

def open_file_dialog():
    files, _ = QFileDialog.getOpenFileNames(None, 'Choose files', '', "Image files (*.jpg *.jpeg *.png *.heif *.heic *.jfif *.bmp *.tiff *.tif *.pjpeg *.pjp)")
    if files:
        fileDialog.clear()
        file_list.clear()
        temp_file_list.clear()
        total_size = 0
        for file in files:
            fileDialog.addItem(file)
            file_list.append(file)
            total_size += os.path.getsize(file)
        input_size_label.setText(f'Исходный размер: {total_size / (1024 * 1024):.2f} МB')
        total_size = 0
        with ThreadPoolExecutor() as executor:
            executor.map(convert_temp, file_list)
        for file in temp_file_list:
            total_size += os.path.getsize(file)
        output_size_label.setText(f'Итоговый размер: {total_size / (1024 * 1024):.2f} МB')

def clear_tmp():
    for filename in os.listdir("./tmp/"):
        file_path = os.path.join("./tmp/", filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f'Ошибка при удалении файла {file_path}: {e}')

def complete():
    file_list.clear()
    temp_file_list.clear()
    fileDialog.clear()
    input_size_label.setText("Исходный размер: 0 МB")
    output_size_label.setText("Итоговый размер: 0 МB")
    clear_tmp()

def convert_files():
    with ThreadPoolExecutor() as executor:
        executor.map(convert, file_list)
    complete()
    

def convert_temp(input_path):
    quality = slider.value()
    img = Image.open(input_path)
    output_path = './tmp/' + os.path.splitext(os.path.basename(input_path))[0] + '.webp'
    img.save(output_path, 'WEBP', quality=quality)
    temp_file_list.append(output_path)


def convert(input_path):
    quality = slider.value()
    img = Image.open(input_path)
    output_path = './Output/' + os.path.splitext(os.path.basename(input_path))[0] + '.webp'
    img.save(output_path, 'WEBP', quality=quality)

app = QApplication(sys.argv)
app.setStyle('Fusion')

window = QWidget()
window.setWindowTitle("Конвертер WEBP")
window.setMinimumSize(400, 400)

main_layout = QVBoxLayout()

slider = QSlider(Qt.Orientation.Horizontal)
slider.setMinimum(1)
slider.setMaximum(100)
slider.setValue(80)
main_layout.addWidget(slider)

slider_label = QLabel("Качество: 80")
main_layout.addWidget(slider_label)
slider.valueChanged.connect(update_slider_lable)

fileDialog = QListWidget()
main_layout.addWidget(fileDialog)

input_size_label = QLabel("Исходный размер: 0 МB")
main_layout.addWidget(input_size_label)

output_size_label = QLabel("Итоговый размер: 0 МB")
main_layout.addWidget(output_size_label)

file_button = QPushButton("Выбрать файлы...")
file_button.clicked.connect(open_file_dialog)
main_layout.addWidget(file_button)

convert_button = QPushButton("Конвертировать")
convert_button.clicked.connect(convert_files)
main_layout.addWidget(convert_button)

window.setLayout(main_layout)

window.show()
app.exec_()
clear_tmp()