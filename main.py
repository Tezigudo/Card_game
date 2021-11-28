from rich import print as printcolor
from rich.console import Console

from Game import Pok_deng, Black_Jack

console = Console()


def main() -> None:
    """This is main part
    """
    printcolor('[blue]LOBBY[/blue]')
    printcolor('1 [blue]-->[/blue] [cyan]BlackJack[cyan]')
    printcolor('2 [blue]-->[/blue] [cyan]Pok-Deng[cyan]')
    printcolor(
        '[red]q[/red][bold cyan]|[/bold cyan][red]Q[/red] [blue] to [red]EXIT[/red]')
    printcolor('Which choice: ', end='')
    choice = input().strip()
    match choice:
        case '1':
            Black_Jack.main()
        case '2':
            Pok_deng.main()
        case 'Q' | 'q':
            return

        case _:
            console.print('INVALID INPUT\n', style='red')
    main()


if __name__ == '__main__':
    main()
