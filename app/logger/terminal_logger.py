from colorama import Style, Fore

class TerminalLogger:
    def error(self, description: str) -> None:
        """ prints a red colored message """
        print(f"{Fore.RED}{description}{Style.RESET_ALL}")

    def success(self, description: str) -> None:
        """ prints a green colored message """
        print(f"{Fore.GREEN}{description}{Style.RESET_ALL}")
        
    def notice(self, description: str) -> None:
        """ prints a yellow colored message """
        print(f"{Fore.YELLOW}{description}{Style.RESET_ALL}")