from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
    QPushButton, QLabel, QMessageBox
)
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

    # -----------------------------
    # Загрузка возможных значений выбранного признака
    # -----------------------------
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
            item.setSelected(val in selected)
            self.values_list.addItem(item)

    # -----------------------------
    # Сохранение значений признака для диагноза
    # -----------------------------
    def save_values(self):
        diag_item = self.diag_list.currentItem()
        feat_item = self.feat_list.currentItem()

        if not diag_item or not feat_item:
            QMessageBox.warning(self, "Ошибка", "Выберите диагноз и признак.")
            return

        diag = diag_item.text()
        feat = feat_item.text()

        selected_values = [i.text() for i in self.values_list.selectedItems()]

        # integer → преобразуем в числа
        if self.kb.get_feature_type(feat) == "integer":
            selected_values = list(map(int, selected_values))

        self.kb.set_diag_value(diag, feat, selected_values)

        QMessageBox.information(self, "Готово", "Значения признака сохранены.")
