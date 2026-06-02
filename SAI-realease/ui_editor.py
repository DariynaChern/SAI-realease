from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QPushButton
from knowledge_base import KnowledgeBase
from ui_editor_diagnoses import DiagnosesTab
from ui_editor_features import FeaturesTab
from ui_editor_diag_features import DiagnosisFeaturesTab
from ui_editor_diag_values import DiagnosisValuesTab
from ui_kb_check import KBCheckWindow


class KnowledgeEditorWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Редактор знаний")

        self.kb = KnowledgeBase("knowledge_base.json")

        # --- вкладки ---
        self.tabs = QTabWidget()
        self.tabs.addTab(DiagnosesTab(self.kb), "Диагнозы")
        self.tabs.addTab(FeaturesTab(self.kb), "Признаки")
        self.tabs.addTab(DiagnosisFeaturesTab(self.kb), "Описание признаков диагноза")
        self.tabs.addTab(DiagnosisValuesTab(self.kb), "Значения признаков диагноза")

        # --- кнопка проверки ---
        self.btn_check = QPushButton("Проверить полноту базы знаний")
        self.btn_check.clicked.connect(self.open_kb_check)

        # --- layout ---
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        layout.addWidget(self.btn_check)
        self.setLayout(layout)

    def open_kb_check(self):
        self.check_window = KBCheckWindow()
        self.check_window.show()
