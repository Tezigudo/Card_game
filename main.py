from rich import print as printcolor
from rich.console import Console

from Game import Pok_deng, Black_Jack

console = Console()


def main() -> None:
    """This is main part
    """
    while True:
        printcolor('[blue]LOBBY[/blue]')
        printcolor('1 [blue]-->[/blue] [cyan]BlackJack[cyan]')
        printcolor('2 [blue]-->[/blue] [cyan]Pok-Deng[cyan]')
        printcolor(
            '[red]q[/red][bold cyan]|[/bold cyan][red]Q[/red] [blue] to [red]EXIT[/red]')
        printcolor('Which choice: ', end='')
        choice = input().strip()
        match choice:
            case '1':
                # if user choose 1 will run main function on blackjack
                Black_Jack.main()
            case '2':
                # if user choose 2 will run main function on Pokdeng
                Pok_deng.main()
            case 'Q' | 'q':
                # if user enter Q or q it will exit the entire program
                return
            case _:  # other case it will be invalid input
                console.print('INVALID INPUT\n', style='red')


if __name__ == '__main__':
    main()
