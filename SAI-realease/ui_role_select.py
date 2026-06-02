from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel
from ui_input import InputWindow
from ui_editor import KnowledgeEditorWindow   # главное окно редактора


class RoleSelectWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Выбор режима работы")

        label = QLabel("Выберите режим работы:")
        label.setStyleSheet("font-size: 16px; font-weight: bold;")

        btn_user = QPushButton("Специалист")
        btn_expert = QPushButton("Эксперт")

        btn_user.clicked.connect(self.open_user_mode)
        btn_expert.clicked.connect(self.open_expert_mode)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(btn_user)
        layout.addWidget(btn_expert)
        self.setLayout(layout)

    def open_user_mode(self):
        self.window = InputWindow()
        self.window.show()
        self.close()

    def open_expert_mode(self):
        self.window = KnowledgeEditorWindow()
        self.window.show()
        self.close()
