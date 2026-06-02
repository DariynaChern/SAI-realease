from knowledge_base import KnowledgeBase
from expert_system import ExpertSystem

kb = KnowledgeBase("knowledge_base.json")
es = ExpertSystem(kb)

instance = {
    "Запах гари": "отсутствует",
    "Наличие известкового налета": 1,
    "Автоматическое выключение при достижении 100 градусов": "присутствует",
    "Протечка": "отсутствует",
    "Температура нагрева": "(80-100] градусов",
    "Видимые повреждения корпуса": "отсутствуют",
    "Нажатие кнопки включения/выключения": "присутствует"
}

suitable, explanations = es.diagnose(instance)

print("Подходящие диагнозы:", suitable)
for d, rs in explanations.items():
    for r in rs:
        print(f"Диагноз «{d}» исключен, так как {r}.")
