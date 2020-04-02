from abc import ABC
from typing import List

from core.intentdefinition import IntentDefinition


class IntentDefinitionSource(ABC):
    def get_intent_definitions(self) -> List[IntentDefinition]:
        pass
