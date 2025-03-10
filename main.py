from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QSlider, QListWidget, QFileDialog, QProgressBar
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import subprocess
import sys
import os

file_list = []
temp_file_list = []

def update_slider_lable(value):
    slider_label.setText("Качество: " + str(value))

def update_level_slider_lable(value):
    if value == 0:
        level_slider_label.setText("Нагрузка: Низкая")
    elif value == 1:
        level_slider_label.setText("Нагрузка: Средняя")
    elif value == 2:
        level_slider_label.setText("Нагрузка: Высокая")
    elif value == 3:
        level_slider_label.setText("Нагрузка: Максимальная")

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
        convert_temp(file_list)
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
    convert(file_list)
    complete()
    

def convert_temp(images_path):
    quality = slider.value()
    perfomance = level_slider.value()
    folder_path = "./tmp"
    program = "./converter.exe"
    args = [
        program,
        f"-q={quality}",
        f"-tmp={True}",
        f"-p={perfomance}"
    ] + images_path
    result = subprocess.Popen(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )



    if result.returncode == 0:
        print("Временная конвертация успешна:")
        print(result.stdout)
        items = os.listdir(folder_path)
        for item in items:
            temp_file_list.append("./tmp/" + item)
    else:
        print("Произошла ошибка:")
        print(result.stderr)


def convert(images_path):
    progress_bar.setVisible(True)
    quality = slider.value()
    perfomance = level_slider.value()
    folder_path = "./output"
    program = "./converter.exe"
    args = [
        program,
        f"-q={quality}",
        f"-tmp={False}",
        f"-p={perfomance}"
    ] + images_path
    result = subprocess.Popen(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    total_files = len(images_path)
    print("Всего файлов:" + str(total_files))
    progress_bar.setMaximum(total_files)

    for line in result.stdout:
        line = line.strip()
        if line.startswith("PROGRESS:"):
            current_progress = int(line.split(":")[1])
            progress_bar.setValue(current_progress)
        elif line == "DONE":
            progress_bar.setVisible(False)
            complete_label.setVisible(True)
            print("Конвертация завершена")
            break

    if result.returncode == 0:
        print("Конвертация успешна:")
        print(result.stdout)
    else:
        print("Произошла ошибка:")
        print(result.stderr)
    

app = QApplication(sys.argv)
app.setStyle('Fusion')
app.setWindowIcon(QIcon('icon.ico'))

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

level_slider = QSlider(Qt.Orientation.Horizontal)
level_slider.setMinimum(0)
level_slider.setMaximum(3)
level_slider.setValue(3)
main_layout.addWidget(level_slider)

level_slider_label = QLabel("Нагрузка: Максимальная")
main_layout.addWidget(level_slider_label)
level_slider.valueChanged.connect(update_level_slider_lable)

fileDialog = QListWidget()
main_layout.addWidget(fileDialog)

input_size_label = QLabel("Исходный размер: 0 МB")
main_layout.addWidget(input_size_label)

output_size_label = QLabel("Итоговый размер: 0 МB")
main_layout.addWidget(output_size_label)

progress_bar = QProgressBar()
main_layout.addWidget(progress_bar)
progress_bar.setVisible(False)

complete_label = QLabel("Конвертация успешна!")
complete_label.setVisible(False)

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