import json


class Save:

    def save(self, player, game):
        print('Saving a progess...')
        print(f'name = {player.name}')


        # try:
        #     with open('history.json', 'r') as data:
        #         history = json.load(data)

        # except FileNotFoundError:
        #     with open('history.json', 'w') as data:
        #         json.dump(nick_score, data, indent=4)

        # else:
        #     history.update(nick_score)
        #     with open('history.json', 'w') as data:
        #         json.dump(history, data, indent=4)

        print('Progess Saved :)')

    def load(self, nickname):
        with open('history.json', 'r') as data:
            progess = json.load(data)

        if nickname.capitalize() in progess:
            print(f'Progess Found with {nickname=} score = {progess[nickname]}')

            prompt = input('do you want to load the progess?(Y/N)')

            if prompt.upper() == 'Y':
                print('Progess loaded')
                return {nickname: progess[nickname]}
            else:
                print('your progess will be reset')
                return {nickname: 0}

        else:
            print('No Save found')
