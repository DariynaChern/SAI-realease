from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
    QPushButton, QLabel, QMessageBox
)
from PyQt5.QtGui import QColor
from knowledge_base import KnowledgeBase


class DiagnosisFeaturesTab(QWidget):
    def __init__(self, kb: KnowledgeBase):
        super().__init__()
        self.kb = kb

        # --- UI элементы ---
        self.diag_list = QListWidget()
        self.feat_list = QListWidget()
        self.feat_list.setSelectionMode(QListWidget.MultiSelection)

        self.btn_save = QPushButton("Сохранить изменения")

        # --- наполняем список диагнозов ---
        self.refresh_diagnoses()

        # --- layout ---
        layout = QHBoxLayout()
        layout.addWidget(self.diag_list)
        layout.addWidget(self.feat_list)

        main = QVBoxLayout()
        main.addWidget(QLabel("Выберите диагноз и отметьте признаки"))
        main.addLayout(layout)
        main.addWidget(self.btn_save)

        self.setLayout(main)

        # --- события ---
        self.diag_list.currentItemChanged.connect(self.load_diag_features)
        self.btn_save.clicked.connect(self.save_changes)

    # -----------------------------
    # Обновление списка диагнозов
    # -----------------------------
    def refresh_diagnoses(self):
        self.diag_list.clear()
        for diag in self.kb.get_diagnoses():
            self.diag_list.addItem(diag)

    # -----------------------------
    # Загрузка признаков диагноза
    # -----------------------------
    def load_diag_features(self):
        item = self.diag_list.currentItem()
        if not item:
            return

        diag = item.text()

        # список всех признаков
        self.feat_list.clear()
        all_features = self.kb.get_features()
        diag_features = set(self.kb.get_diag_features(diag))

        for feat in all_features:
            lw_item = QListWidgetItem(feat)
            lw_item.setSelected(feat in diag_features)
            self.feat_list.addItem(lw_item)

    # -----------------------------
    # Сохранение изменений
    # -----------------------------
    def save_changes(self):
        item = self.diag_list.currentItem()
        if not item:
            QMessageBox.warning(self, "Ошибка", "Выберите диагноз.")
            return

        diag = item.text()

        selected = [i.text() for i in self.feat_list.selectedItems()]

        self.kb.set_diag_features(diag, selected)

        QMessageBox.information(self, "Готово", "Описание признаков диагноза сохранено.")

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

    def clear_highlight(self):
        try:
            for lst in (self.diag_list, self.feat_list):
                for i in range(lst.count()):
                    item = lst.item(i)
                    if item:
                        item.setBackground(QColor("white"))
                        item.setForeground(QColor("black"))
        except RuntimeError:
            pass
