from typing import Callable
from app.logger.terminal_logger import TerminalLogger

class ActionHandler:
    def __init__(self, terminal_logger: TerminalLogger) -> None:
        self.terminal_logger = terminal_logger
        self.action_list = []

    def add_action(self, label: str, func: Callable[[], None]) -> None:
        self.action_list.append(
            {
                "label": label,
                "func": func
            }
        )

    def show_actions(self) -> None:
        """ shows a list of actions """
        self.terminal_logger.notice("Actions list\n")
        for i, action in enumerate(self.action_list):
            print(f"{i}) {action["label"]}")
        print("")

    def __get_action_func(self) -> Callable[[], None]:
        """ Prompts the user to select an action and returns the corresponding function.  """
        try:
            input_number = int(input("Your option: "))
            return self.action_list[input_number]["func"]
        except (ValueError, IndexError):
            self.terminal_logger.error("\nCould not handle this action, please provide one of the list\n")
            self.show_actions()
            return self.__get_action_func()

    def handle_actions(self) -> None:
        """ Executes the selected action. """
        func = self.__get_action_func()
        func()
        
        self.show_actions()