import csv


class Save:

    def __init__(self) -> None:
        """Initilize with all current history(database)
        """
        self.database = []
        # open and load data into file
        with open('history.csv', 'r') as data_file:
            data = csv.DictReader(data_file)
            for each_data in data:
                each_data['wincount'] = int(each_data['wincount'])
                self.database.append(each_data)

    def update_database(self) -> None:
        """update database into file
        """
        with open('history.csv', 'w') as f:
            writer = csv.DictWriter(f, fieldnames=['game', 'name', 'wincount'])
            writer.writeheader()  # write header

            for data in self.database:
                writer.writerow(data)

    @staticmethod
    def check_valid_game_and_nickname(data: dict, game: str, name: str) -> bool:
        """check whether game and name is valid

        Parameters
        ----------
        data : Dict
            this is dict from iterating self.database
        game : str
            str of game name
        name : str
            name of the player

        Returns
        -------
        bool
            True if it equal False otherwise
        """
        return data['game'] == game and data['name'] == name

    def save(self, game: str, name: str, wincount: int) -> None:
        """save the progess

        Parameters
        ----------
        game : str
            str of game name
        name : str
            name of the player
        wincount : int
            wincount of name player
        """
        print('Saving a progess...')
        print(f'name = {name}')

        for data in self.database:
            if self.check_valid_game_and_nickname(data, game, name):
                data['wincount'] = wincount

        self.update_database()

        print('Progess Saved :)\n')

    def load(self, game: str, name: str) -> dict:
        """load the progess(if have) other wise will create
        a new progess which wincount = 0

        Parameters
        ----------
        game : str
            str of game name
        name : str
            name of the player

        Returns
        -------
        Dict
            it will be dict of data(if it exist)
            otherwise it will be dict that wincount = 0
        """
        with open('history.csv', 'r') as old_data:
            history = csv.DictReader(old_data)
            for data in history:
                if data['game'] == game and data['name'] == name:
                    data['wincount'] = int(data['wincount'])
                    return data
            else:
                print('No Save found')
                new_data = {'game': game, 'name': name, 'wincount': 0}
                self.database.append(new_data)
                return new_data

    def add_score(self, game: str, name: str, amount: int) -> None:
        """add an entire amount of score

        Parameters
        ----------
        game : str
            str of game name
        name : str
            name of the player
        amount : int
            amount of wincount that user want to add
        """
        data = self.load(game, name)
        self.save(game, name, data['wincount'] + amount)

    def delete(self, game: str, name: str) -> None:
        """delete progess for game for name

        Parameters
        ----------
        game : str
            str of game name
        name : str
            name of the player
        """
        if not self.load(game, name)['wincount']:
            print(f'Player name {name} doesnt exist')
            return

        print('deleting data...')
        for i, data in enumerate(self.database):
            if data['game'] == game and data['name'] == name:
                del self.database[i]
                self.update_database()

    def game_history(self, game: str) -> dict:
        """

        Parameters
        ----------
        game : str
            str of game name

        Returns
        -------
        dict
            a dict of player which key is name of player
            and value us each wincount of player
        """

        return {data['name']: int(data['wincount']) for data in self.database
                if data['game'] == game}

    def reset(self, *game: str) -> None:
        """reset progress of database of game in game list
        if user not entergame it will reset all the database and history.
        """
        if not game:
            self.database = []
        else:
            self.database = [
                data for data in self.database if data['game'] not in game]
        self.update_database()
