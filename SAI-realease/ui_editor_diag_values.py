from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
    QPushButton, QLabel
)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, QTimer
from knowledge_base import KnowledgeBase


class DiagnosisValuesTab(QWidget):
    def __init__(self, kb: KnowledgeBase):
        super().__init__()
        self.kb = kb

        # --- UI элементы ---
        self.diag_list = QListWidget()
        self.feat_list = QListWidget()
        self.values_list = QListWidget()
        self.values_list.setSelectionMode(QListWidget.MultiSelection)

        self.btn_save = QPushButton("Сохранить значения")

        # --- метка для уведомлений ---
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: green; font-weight: bold;")
        self.status_label.hide()

        # --- наполняем список диагнозов ---
        self.refresh_diagnoses()

        # --- layout ---
        layout = QHBoxLayout()
        layout.addWidget(self.diag_list)
        layout.addWidget(self.feat_list)
        layout.addWidget(self.values_list)

        main = QVBoxLayout()
        main.addWidget(QLabel("Выберите диагноз → признак → значения"))
        main.addLayout(layout)
        main.addWidget(self.btn_save)
        main.addWidget(self.status_label)

        self.setLayout(main)

        # --- события ---
        self.diag_list.currentItemChanged.connect(self.load_features)
        self.feat_list.currentItemChanged.connect(self.load_values)
        self.btn_save.clicked.connect(self.save_values)

    # -----------------------------
    # Обновление списка диагнозов
    # -----------------------------
    def refresh_diagnoses(self):
        self.diag_list.clear()
        for diag in self.kb.get_diagnoses():
            self.diag_list.addItem(diag)

    # -----------------------------
    # Загрузка признаков выбранного диагноза
    # -----------------------------
    def load_features(self):
        item = self.diag_list.currentItem()
        if not item:
            return

        diag = item.text()
        features = self.kb.get_diag_features(diag)

        self.feat_list.clear()
        for feat in features:
            self.feat_list.addItem(feat)

        self.values_list.clear()

    def load_values(self):
        diag_item = self.diag_list.currentItem()
        feat_item = self.feat_list.currentItem()

        if not diag_item or not feat_item:
            return

        diag = diag_item.text()
        feat = feat_item.text()

        possible = self.kb.get_possible_values(feat)
        selected = set(self.kb.get_diag_values(diag, feat))

        self.values_list.clear()
        for val in possible:
            item = QListWidgetItem(str(val))
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)

            # ВАЖНО: правильная установка чекбокса
            if val in selected:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)

            self.values_list.addItem(item)

    # -----------------------------
    # Сохранение значений
    # -----------------------------
    def save_values(self):
        try:
            diag_item = self.diag_list.currentItem()
            feat_item = self.feat_list.currentItem()

            if not diag_item or not feat_item:
                return

            diag = diag_item.text()
            feat = feat_item.text()

            selected = []
            for i in range(self.values_list.count()):
                item = self.values_list.item(i)
                if item and item.checkState() == Qt.Checked:
                    selected.append(item.text())

            # создаём values, если его нет
            if feat not in self.kb.diagnoses[diag]["values"]:
                self.kb.diagnoses[diag]["values"][feat] = []

            self.kb.diagnoses[diag]["values"][feat] = selected
            self.kb.save()

            # --- показываем уведомление ---
            self.status_label.setText("Сохранено")
            self.status_label.show()

            QTimer.singleShot(5000, self.status_label.hide)

        except RuntimeError:
            pass

    # -----------------------------
    # Подсветка ошибок
    # -----------------------------
    def highlight_diagnosis(self, diag_name):
        try:
            for i in range(self.diag_list.count()):
                item = self.diag_list.item(i)
                if item and item.text() == diag_name:
                    item.setBackground(QColor("red"))
                    item.setForeground(QColor("white"))
        except RuntimeError:
            pass

    def highlight_feature(self, feat_name):
        try:
            for i in range(self.feat_list.count()):
                item = self.feat_list.item(i)
                if item and item.text() == feat_name:
                    item.setBackground(QColor("red"))
                    item.setForeground(QColor("white"))
        except RuntimeError:
            pass

    def highlight_value(self, value_text):
        try:
            for i in range(self.values_list.count()):
                item = self.values_list.item(i)
                if item and item.text() == value_text:
                    item.setBackground(QColor("red"))
                    item.setForeground(QColor("white"))
        except RuntimeError:
            pass

    def clear_highlight(self):
        try:
            for lst in (self.diag_list, self.feat_list, self.values_list):
                for i in range(lst.count()):
                    item = lst.item(i)
                    if item:
                        item.setBackground(QColor("white"))
                        item.setForeground(QColor("black"))
        except RuntimeError:
            pass
