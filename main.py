from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QMessageBox
import os
from docxtpl import DocxTemplate
from main_ui import Ui_MainWindow
from lib import context
class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Загрузка файла интерфейса
        self.win = Ui_MainWindow()
        self.win.setupUi(self)
        # Подключаем обработчик события к кнопке
        self.win.toolButton.clicked.connect(self.showFileDialog)
        self.win.toolButton.setToolTip("Откройте файл шаблона .docx")
        self.win.pushButton.clicked.connect(self.generateDoc)
        self.win.pushButton.setToolTip("Нажмите кнопку для генерации выходного файла")
        self.win.pushButton_3.clicked.connect(self.closeWindows)
        self.win.lineEdit.setToolTip("Введите название шаблона с расширением, либо введите его при помощи кнопки")
        self.win.lineEdit_2.setToolTip("Введите название выходного файла БЕЗ расширения")
        self.win.checkBox.setToolTip("Если чек бокс активирован, после генерации файла, он будет открыт")
        self.win.pushButton_2.clicked.connect(self.deleteFiles)
        self.win.pushButton_2.setToolTip("Выберите файлы для удаления")
    def showFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        # Открываем диалог выбора файла
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", "All Files (*);;Word Files (*.docx)", options=options)

        if file_name:
            # Вписываем название файла в lineEdit
            only_name = os.path.basename(file_name)
            self.win.lineEdit.setText(only_name)
            self.template_path = only_name

    def generateDoc(self):
        nameFrom = self.win.lineEdit_2.text()

        # Check if the file name has the correct extension
        if not nameFrom.endswith(".docx"):
            # Display error message for incorrect extension
            print("Error: File extension must be .docx")
            return

        doc = DocxTemplate(self.template_path)
        doc.render(context)
        doc.save(nameFrom)

        is_check = self.win.checkBox.isChecked()
        if is_check:
            if hasattr(self, 'template_path') and os.path.exists(self.template_path):
                os.system(f"start {nameFrom}")
            else:
                # Display error message for invalid template path
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error: Template path is invalid.")
                msg.setWindowTitle("Error")
                msg.exec_()
    def deleteFiles(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        files_to_delete, _ = QFileDialog.getOpenFileNames(self, "Выберите файлы для удаления", "",
                                                          "Word Files (*.docx)", options=options)
        if files_to_delete:
            try:
                for file_path in files_to_delete:
                    if not self.isForbiddenFile(file_path):
                        os.remove(file_path)
                        QMessageBox.information(self, "Успех", f"Файлы: {files_to_delete} успешно удалены.")
                    else:
                        QMessageBox.warning(self, "Предупреждение", f"Удаление файла {file_path} запрещено")
            except Exception as e:
                # В случае ошибки выводим сообщение об ошибке
                self.showErrorMessage(f"Ошибка удаления файлов: {str(e)}")
    def isForbiddenFile(self, file_path):
        forbidden_file = ["шаблон.docx", "main.py", "lib.py", "main.ui", "main_ui.py", "run.py"]
        return os.path.basename(file_path) in forbidden_file
    def closeWindows(self):
        self.close()

if __name__ == "__main__":
    app = QApplication([])
    window = MyMainWindow()
    window.show()
    app.exec_()
