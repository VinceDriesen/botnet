from enum import Enum
from trello import List as TrelloList


class TaskType(Enum):
    RUN_PAYLOAD = "RUN_PAYLOAD"


class Command:
    def __init__(self, list_commands: TrelloList):
        self._tasks: list[tuple[TaskType, dict]] = []
        for card in list_commands.list_cards(card_filter="open")[1:]:
            task_type = self._task_from_name(card.name)

            task_data = self._parse_description(card.desc)
            if isinstance(task_type, TaskType):
                self._tasks.append((task_type, task_data))
            else:
                print("Is ut eh man, geen valid tasktype")

    def _task_from_name(self, name: str) -> TaskType | None:
        try:
            return TaskType(name)
        except ValueError:
            print(f"Onbekende taak genegeerd: {name}")
            return None

    def _parse_description(self, desc: str) -> dict:
        parsed_data = {
            "params": [],
            "clients": [],
            "priority": 0
        }

        for line in desc.splitlines():
            line = line.strip()
            if not line:
                continue

            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip().upper()
                value = value.strip()

                if not value:
                    continue

                if key == "PARAMS":
                    parsed_data["params"] = [p.strip()
                                             for p in value.split(",")]
                elif key == "CLIENTS":
                    parsed_data["clients"] = [c.strip()
                                              for c in value.split(",")]
                elif key == "PRIORITY":
                    parsed_data["priority"] = int(value)

        return parsed_data
