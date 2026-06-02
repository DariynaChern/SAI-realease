from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QPushButton, QLineEdit, QMessageBox
)
from knowledge_base import KnowledgeBase


class DiagnosesTab(QWidget):
    def __init__(self, kb: KnowledgeBase):
        super().__init__()
        self.kb = kb

        # --- UI элементы ---
        self.list = QListWidget()
        self.input = QLineEdit()
        self.btn_add = QPushButton("Добавить диагноз")
        self.btn_delete = QPushButton("Удалить выбранный диагноз")

        # --- наполняем список ---
        self.refresh_list()

        # --- layout ---
        layout = QVBoxLayout()
        layout.addWidget(self.list)

        hl = QHBoxLayout()
        hl.addWidget(self.input)
        hl.addWidget(self.btn_add)
        layout.addLayout(hl)

        layout.addWidget(self.btn_delete)

        self.setLayout(layout)

        # --- события ---
        self.btn_add.clicked.connect(self.add_diag)
        self.btn_delete.clicked.connect(self.delete_diag)

    # -----------------------------
    # Обновление списка диагнозов
    # -----------------------------
    def refresh_list(self):
        self.list.clear()
        for diag in self.kb.get_diagnoses():
            self.list.addItem(diag)

    # -----------------------------
    # Добавление диагноза
    # -----------------------------
    def add_diag(self):
        name = self.input.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название диагноза.")
            return

        if name in self.kb.get_diagnoses():
            QMessageBox.warning(self, "Ошибка", "Такой диагноз уже существует.")
            return

        self.kb.add_diagnosis(name)
        self.refresh_list()
        self.input.clear()

    # -----------------------------
    # Удаление диагноза
    # -----------------------------
    def delete_diag(self):
        item = self.list.currentItem()
        if not item:
            QMessageBox.warning(self, "Ошибка", "Выберите диагноз.")
            return

        name = item.text()

        if name == self.kb.healthy:
            QMessageBox.warning(self, "Ошибка", "Нельзя удалить диагноз «Исправен».")
            return

        self.kb.remove_diagnosis(name)
        self.refresh_list()
