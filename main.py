from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow
import os
from docxtpl import DocxTemplate
from main_ui import Ui_MainWindow

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Загрузка файла интерфейса
        self.win = Ui_MainWindow()
        self.win.setupUi(self)
        # Подключаем обработчик события к кнопке
        self.win.toolButton.clicked.connect(self.showFileDialog)
        self.win.pushButton.clicked.connect(self.generateDoc)
        self.win.pushButton_3.clicked.connect(self.closeWindows)

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
        nameFrom = nameFrom + ".docx"
        doc = DocxTemplate(self.template_path)
        context = {}
        context['first'] = 'Первый.'
        context['first2'] = 'Второй.'
        context['first3'] = 'Третий.'
        context['primer'] = 'Шаблон.'
        context['name'] = 'Аяз.'
        doc.render(context)
        doc.save(nameFrom)
        is_check = self.win.checkBox.isChecked()
        if is_check:
            if hasattr(self, 'template_path') and os.path.exists(self.template_path):
                os.system(f"start {nameFrom}")
    def closeWindows(self):
        self.win.close()

if __name__ == "__main__":
    app = QApplication([])
    window = MyMainWindow()
    window.show()
    app.exec_()
