from PyQt5.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QPushButton
from ml_module import MLModule
from knowledge_base import KnowledgeBase
from ui_ml_output import MLOutputWindow


class OutputWindow(QWidget):
    def __init__(self, suitable, explanations, instance):
        super().__init__()
        self.setWindowTitle("Результат диагностики")

        self.suitable = suitable
        self.explanations = explanations
        self.instance = instance  # сохраняем входные данные для ML

        # Основное текстовое поле
        self.box = QTextEdit()
        self.box.setReadOnly(True)
        self.box.setText(self.build_text())

        # Кнопка ML-модуля
        self.btn_ml = QPushButton("Уточнить диагноз с помощью ИИ")
        self.btn_ml.clicked.connect(self.use_ml)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.box)
        layout.addWidget(self.btn_ml)
        self.setLayout(layout)

    # ---------------------------------------------------------
    # Формирование текста экспертной системы
    # ---------------------------------------------------------
    def build_text(self):
        lines = []

        if self.suitable:
            lines.append(f"Подходящий диагноз: «{self.suitable[0]}».\n\n")
        else:
            lines.append("Диагноз не определён.\n\n")

        for diag, reasons in self.explanations.items():
            for r in reasons:
                lines.append(f"Диагноз «{diag}» исключён, так как {r}.\n\n")

        return "".join(lines)

    # ---------------------------------------------------------
    # ML-модуль: уточнение диагноза
    # ---------------------------------------------------------

    def use_ml(self):
        kb = KnowledgeBase("knowledge_base.json")
        ml = MLModule(kb)
        ml.load()

        preds = ml.predict(self.instance)

        self.ml_window = MLOutputWindow(preds)
        self.ml_window.show()

