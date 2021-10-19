__author__ = 'Preawpan Thamapipol(Godiez1)'
__copyright__ = 'Godiez1 Github'
__email__ = 'godjangg@gmail.com'
__version__ = '1.0.1'
__status__ = 'working'

from rich import print as printcolor
from rich.console import Console

import Black_Jack
import Pok_deng
console = Console()


def main():
    printcolor('[blue]LOBBY[/blue]')
    printcolor('1 [blue]-->[/blue] [cyan]BlackJack[cyan]')
    printcolor('2 [blue]-->[/blue] [cyan]Pok-Deng[cyan]')
    printcolor('[red]q[/red][bold cyan]|[/bold cyan][red]Q[/red] [blue] to [red]EXIT[/red]')
    printcolor('Which choice: ', end='')
    choice = input()
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
