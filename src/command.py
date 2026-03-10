from enum import Enum
from trello import List as TrelloList, Checklist
from dataclasses import dataclass, field


class TaskType(Enum):
    RUN_PAYLOAD = "RUN_PAYLOAD"
    REMOVE_CLIENTS = "REMOVE_CLIENTS"


@dataclass(order=True)
class ParsedCommand:
    priority: int
    checklist: Checklist = field(compare=False)
    task_type: TaskType = field(compare=False)
    params: list[str] = field(compare=False)


@dataclass
class ParsedDesc:
    priority: int
    params: list[str]


class Command:
    def __init__(self, list_commands: TrelloList):
        self._tasks: list[ParsedCommand] = []
        for card in list_commands.list_cards(card_filter="open")[1:]:
            if any("Execute" in label.name for label in card.labels):
                task_type = self._task_from_name(card.name)
                if isinstance(task_type, TaskType):
                    task_data = self._parse_description(card.desc)
                    parsed_cmd = ParsedCommand(
                        priority=task_data.priority,
                        checklist=card.checklists[0],
                        task_type=task_type,
                        params=task_data.params,
                    )
                    self._tasks.append(parsed_cmd)

    def get_commands(self) -> list[ParsedCommand]:
        return self._tasks

    def _task_from_name(self, name: str) -> TaskType | None:
        try:
            return TaskType(name)
        except ValueError:
            print(f"Onbekende taak genegeerd: {name}")
            return None

    def _parse_description(self, desc: str) -> ParsedDesc:
        params: list[str] = []
        priority: int = 0
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
                    params = [p.strip() for p in value.split(",")]

                elif key == "PRIORITY":
                    priority = int(value)

        return ParsedDesc(priority, params)
