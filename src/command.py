from enum import Enum
from trello import List as TrelloList
from dataclasses import dataclass, field


class TaskType(Enum):
    RUN_PAYLOAD = "RUN_PAYLOAD"
    REMOVE_CLIENTS = "REMOVE_CLIENTS"


@dataclass(order=True)
class ParsedCommand:
    priority: int
    task_type: TaskType = field(compare=False)
    params: list[str] = field(default_factory=list, compare=False)
    clients: list[str] = field(default_factory=list, compare=False)


class Command:
    def __init__(self, list_commands: TrelloList):
        self._tasks: list[ParsedCommand] = []
        for card in list_commands.list_cards(card_filter="open")[1:]:
            if any('Execute' in label.name for label in card.labels):
                task_type = self._task_from_name(card.name)
                if isinstance(task_type, TaskType):
                    task_data = self._parse_description(card.desc)
                    parsed_cmd = ParsedCommand(
                        priority=task_data["priority"],
                        task_type=task_type,
                        params=task_data["params"],
                        clients=task_data["clients"]
                    )
                    self._tasks.append(parsed_cmd)
                else:
                    print(f"Is ut eh man, geen valid tasktype: {card.name}")
            else:
                print(f"card met id: {card.id}, had geen execute label")

    def get_commands(self) -> list[ParsedCommand]:
        return self._tasks

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
