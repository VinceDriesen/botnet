import heapq
from trello import List as TrelloList
from src.runner import Runner
from .command import ParsedCommand, TaskType


class Schedular:
    def __init__(self, unique_id: str, list_commands: list[ParsedCommand], payload_list: TrelloList):
        self.unique_id = unique_id
        self.commands = self._filter_commands(list_commands)
        self._run_commands(payload_list)

    def _filter_commands(self, list_commands: list[ParsedCommand]) -> list[ParsedCommand]:
        results = []
        for cmd in list_commands:
            if any(self.unique_id in client for client in cmd.clients):
                heapq.heappush(results, cmd)
                print(
                    f"[*] Match gevonden voor id: {self.unique_id} (Prioriteit: {cmd.priority})")

        return results

    def _run_commands(self, payload_list: TrelloList):
        while self.commands:
            cmd = heapq.heappop(self.commands)
            runner = Runner()
            match cmd.task_type:
                case TaskType.REMOVE_CLIENTS:
                    runner.remove_client(self.unique_id)
                case TaskType.RUN_PAYLOAD:
                    for payload_name in cmd.params:
                        print(f"[>] Voert payload uit: {
                              payload_name} (Task: {cmd.task_type.name})")
                        runner.execute_command(payload_name, payload_list)
