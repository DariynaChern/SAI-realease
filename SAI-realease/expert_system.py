from typing import Dict, List, Tuple, Any
from knowledge_base import KnowledgeBase


class ExpertSystem:
    def __init__(self, kb: KnowledgeBase):
        self.kb = kb

    # --- проверка на "Исправен" ---

    def _is_all_normal(self, instance):
        for feat, val in instance.items():
            info = self.kb.features[feat]
            normals = info["normal"]

            # integer: нормальные значения — диапазон
            if info["type"] == "integer":
                low, high = normals
                if not (low <= val <= high):
                    return False

            # binary/categorical: нормальные значения — список строк
            else:
                if val not in normals:
                    return False

        return True

    # --- публичный метод диагностики ---

    def diagnose(self, instance):
        # Если все признаки в норме → вернуть диагноз "Исправен"
        if self._is_all_normal(instance):
            return [self.kb.healthy], {}

        explanations = {}
        suitable = []

        for diag in self.kb.diagnoses.keys():
            reasons = self._build_refutation(diag, instance)

            if reasons:
                explanations[diag] = reasons
            else:
                suitable.append(diag)

        return suitable, explanations

    # --- построение причин опровержения ---

    def _build_refutation(self, diag: str, instance: Dict[str, Any]) -> List[str]:
        """
        Возвращает список текстов причин опровержения.
        Если список пуст — диагноз не опровергнут.
        """
        reasons: List[str] = []
        diag_feats = set(self.kb.get_diag_features(diag))

        # 1) признаки, НЕ входящие в описание диагноза, должны быть нормальными
        for feat, value in instance.items():
            if feat not in diag_feats:
                normals = self.kb.get_normal_values(feat)
                if value not in normals:
                    reasons.append(
                        f'значение признака «{feat}» = «{value}» не является нормальным для данного признака'
                    )

        if reasons:
            return reasons

        # 2) признаки, входящие в описание диагноза, должны попадать в значения для диагноза
        for feat in diag_feats:
            value = instance[feat]
            allowed = self.kb.get_diag_values(diag, feat)
            if value not in allowed:
                reasons.append(
                    f'значение признака «{feat}» = «{value}» не соответствует описанию диагноза'
                )

        return reasons
