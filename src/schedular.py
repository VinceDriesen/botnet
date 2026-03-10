import heapq
from trello import Checklist, List as TrelloList
from src.runner import Runner
from .command import ParsedCommand, TaskType
from .status_updater import StatusUpdater


class Schedular:
    def __init__(
        self,
        unique_id: str,
        list_commands: list[ParsedCommand],
        payload_list: TrelloList,
        status_updater: StatusUpdater,
    ):
        self.unique_id = unique_id
        self.commands = self._filter_commands(list_commands)
        self.status_updater = status_updater
        self._run_commands(payload_list)

    def _filter_commands(
        self, list_commands: list[ParsedCommand]
    ) -> list[ParsedCommand]:
        results = []
        for cmd in list_commands:
            for item in cmd.checklist.items:
                if item.get("name") == self.unique_id:
                    if item.get("checked") is False:
                        heapq.heappush(results, cmd)

        return results

    def _run_commands(self, payload_list: TrelloList):
        while self.commands:
            cmd = heapq.heappop(self.commands)
            runner = Runner(self.status_updater)
            match cmd.task_type:
                case TaskType.REMOVE_CLIENTS:
                    runner.remove_client()
                case TaskType.RUN_PAYLOAD:
                    for payload_name in cmd.params:
                        if runner.execute_command(payload_name, payload_list):
                            self._completed_command(cmd.checklist)

    def _completed_command(self, checklist: Checklist):
        checklist.set_checklist_item(self.unique_id, True)
