from PyQt5.QtWidgets import QWidget, QTextEdit, QVBoxLayout


class MLOutputWindow(QWidget):
    def __init__(self, preds):
        super().__init__()
        self.setWindowTitle("Результаты ML-модуля")

        self.box = QTextEdit()
        self.box.setReadOnly(True)

        # сортируем по вероятности
        preds_sorted = sorted(preds, key=lambda x: x[1], reverse=True)

        best_diag, best_prob = preds_sorted[0]

        text = ""
        text += f"Наиболее вероятный диагноз: «{best_diag}» ({best_prob:.3f})\n\n"
        text += "Вероятности по всем диагнозам:\n\n"

        for diag, prob in preds_sorted:
            text += f"{diag}: {prob:.3f}\n"

        self.box.setText(text)

        layout = QVBoxLayout()
        layout.addWidget(self.box)
        self.setLayout(layout)
