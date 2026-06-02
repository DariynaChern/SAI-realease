from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel
from ui_input import InputWindow
from ui_editor import KnowledgeEditorWindow


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Система диагностики электрических чайников")

        # Заголовок
        self.title = QLabel("Система диагностики электрических чайников")
        self.title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 15px;")

        # Кнопки
        self.btn_input = QPushButton("Диагностика")
        self.btn_editor = QPushButton("Редактор знаний")
        self.btn_exit = QPushButton("Выход")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.btn_input)
        layout.addWidget(self.btn_editor)
        layout.addWidget(self.btn_exit)

        layout.addStretch()
        self.setLayout(layout)

        # События
        self.btn_input.clicked.connect(self.open_input)
        self.btn_editor.clicked.connect(self.open_editor)
        self.btn_exit.clicked.connect(self.close)

    def open_input(self):
        self.input_window = InputWindow()
        self.input_window.show()

    def open_editor(self):
        self.editor_window = KnowledgeEditorWindow()
        self.editor_window.show()
