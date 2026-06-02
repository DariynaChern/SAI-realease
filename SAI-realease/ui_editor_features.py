from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton,
    QLineEdit, QLabel, QComboBox, QTextEdit, QMessageBox
)
from knowledge_base import KnowledgeBase


class FeaturesTab(QWidget):
    def __init__(self, kb: KnowledgeBase):
        super().__init__()
        self.kb = kb

        # --- UI элементы ---
        self.list = QListWidget()
        self.refresh_list()

        self.input_name = QLineEdit()
        self.btn_add = QPushButton("Добавить признак")
        self.btn_delete = QPushButton("Удалить признак")

        # Редактирование выбранного признака
        self.type_box = QComboBox()
        self.type_box.addItems(["binary", "integer", "categorical"])

        self.possible_edit = QTextEdit()
        self.normal_edit = QTextEdit()

        self.btn_save = QPushButton("Сохранить изменения")

        # --- Layout ---
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Список признаков:"))
        layout.addWidget(self.list)

        hl = QHBoxLayout()
        hl.addWidget(self.input_name)
        hl.addWidget(self.btn_add)
        layout.addLayout(hl)

        layout.addWidget(self.btn_delete)

        layout.addWidget(QLabel("Тип признака:"))
        layout.addWidget(self.type_box)

        layout.addWidget(QLabel("Возможные значения (через запятую):"))
        layout.addWidget(self.possible_edit)

        layout.addWidget(QLabel("Нормальные значения (через запятую):"))
        layout.addWidget(self.normal_edit)

        layout.addWidget(self.btn_save)

        self.setLayout(layout)

        # --- События ---
        self.list.currentItemChanged.connect(self.load_feature)
        self.btn_add.clicked.connect(self.add_feature)
        self.btn_delete.clicked.connect(self.delete_feature)
        self.btn_save.clicked.connect(self.save_feature)

    # -----------------------------
    # Обновление списка признаков
    # -----------------------------
    def refresh_list(self):
        self.list.clear()
        for feat in self.kb.get_features():
            self.list.addItem(feat)

    # -----------------------------
    # Загрузка выбранного признака
    # -----------------------------
    def load_feature(self):
        item = self.list.currentItem()
        if not item:
            return

        name = item.text()
        info = self.kb.features[name]

        self.type_box.setCurrentText(info["type"])
        self.possible_edit.setText(", ".join(map(str, info["possible"])))
        self.normal_edit.setText(", ".join(map(str, info["normal"])))

    # -----------------------------
    # Добавление признака
    # -----------------------------
    def add_feature(self):
        name = self.input_name.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название признака.")
            return

        if name in self.kb.get_features():
            QMessageBox.warning(self, "Ошибка", "Такой признак уже существует.")
            return

        # создаём пустой признак
        self.kb.add_feature(name, "binary", ["отсутствует", "присутствует"], ["отсутствует"])
        self.refresh_list()
        self.input_name.clear()

    # -----------------------------
    # Удаление признака
    # -----------------------------
    def delete_feature(self):
        item = self.list.currentItem()
        if not item:
            QMessageBox.warning(self, "Ошибка", "Выберите признак.")
            return

        name = item.text()
        self.kb.remove_feature(name)
        self.refresh_list()

    # -----------------------------
    # Сохранение изменений признака
    # -----------------------------
    def save_feature(self):
        item = self.list.currentItem()
        if not item:
            QMessageBox.warning(self, "Ошибка", "Выберите признак.")
            return

        name = item.text()
        ftype = self.type_box.currentText()

        possible = [v.strip() for v in self.possible_edit.toPlainText().split(",") if v.strip()]
        normal = [v.strip() for v in self.normal_edit.toPlainText().split(",") if v.strip()]

        # integer → преобразуем в числа
        if ftype == "integer":
            try:
                possible = list(map(int, possible))
                normal = list(map(int, normal))
            except ValueError:
                QMessageBox.warning(self, "Ошибка", "Для integer значения должны быть числами.")
                return

        self.kb.update_feature(name, ftype=ftype, possible=possible, normal=normal)
        QMessageBox.information(self, "Готово", "Изменения сохранены.")
