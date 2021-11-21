import csv


class Save:

    def __init__(self) -> None:
        self.database = []
        with open('history.csv', 'r') as data_file:
            data = csv.DictReader(data_file)
            for each_data in data:
                each_data['wincount'] = int(each_data['wincount'])
                self.database.append(each_data)

    def update_database(self):
        with open('history.csv', 'w') as f:
            writer = csv.DictWriter(f, fieldnames=['game', 'name', 'wincount'])
            writer.writeheader()

            for data in self.database:
                writer.writerow(data)

    def save(self, game, name, wincount):
        print('Saving a progess...')
        print(f'name = {name}')

        for data in self.database:
            if data['game'] == game and data['name'] == name:
                data['wincount'] = wincount
        
        self.update_database()

        print('Progess Saved :)\n')

    def load(self, game, name):
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

    def delete(self, game, name):
        if not self.load(game, name)['wincount']:
            print(f'Player name {name} doesnt exist')
            return

        print('deleting data...')
        for i, data in enumerate(self.database):
            if data['game'] == game and data['name'] == name:
                del self.database[i]
                self.update_database()

    def reset(self, **game):
        if '