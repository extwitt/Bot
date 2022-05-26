import requests
import random

activeGames = {}

def newGame(chatID, newGame):
    activeGames.update({chatID: newGame})
    return newGame

def getGame(chatID):
    return activeGames.get(chatID)

def stopGame(chatID):
    activeGames.pop(chatID)



class Card:
    emo_SPADES = "U0002660"
    emo_CLUBS = "U0002663"
    emo_HEARTS = "U0002665"
    emo_DIAMONDS = "U0002666"

    def __init__(self, card):
        if isinstance(card, dict):
            self.__card_JSON = card
            self.code = card["code"]
            self.suit = card["suit"]
            self.value = card["value"]
            self.cost = self.get_cost_card()
            self.color = self.get_color_card()
            self.__imagesPNG_URL = card["images"]["png"]
            self.__imagesSVG_URL = card["images"]["svg"]

        elif isinstance(card, str):
            self.__card_JSON = None
            self.code = card

            value = card[0]
            if value == "J":
                self.value = "JACK"
            elif value == "Q":
                self.value = "QUEEN"
            elif value == "K":
                self.value = "KING"
            elif value == "A":
                self.value = "ACE"
            elif value == "J":
                self.value = "JACK"
            else:
                self.value = value

            suit = card[1]
            if suit == "S":
                self.suit = "SPADES"
            elif suit == "C":
                self.suit = "CLUBS"
            elif suit == "H":
                self.suit = "HEARTS"
            elif suit == "D":
                self.suit = "DIAMONDS"

            self.cost = self.get_cost_card()
            self.color = self.get_color_card()

    def get_cost_card(self):
        if self.value == "JACK":
            return 2
        elif self.value == "QUEEN":
            return 3
        elif self.value == "KING":
            return 4
        elif self.value == "ACE":
            return 11
        elif self.value == "JOKER":
            return 1
        else:
            return int(self.value)

    def get_color_card(self):
        if self.suit == "SPADES":
            return "BLACK"
        elif self.suit == "CLUBS":
            return "BLACK"
        elif self.suit == "HEARTS":
            return "RED"
        elif self.suit == "DIAMONDS":
            return "RED"


class Game21:
    def __init__(self, deck_count=1):
        new_pack = self.new_pack(deck_count)
        if new_pack is not None:
            self.pack_card = new_pack
            self.remaining = new_pack["remaining"],
            self.card_in_game = []
            self.arr_cards_URL = []
            self.score = 0
            self.status = None

    def new_pack(self, deck_count):
        response = requests.get(f"https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count={deck_count}")
        if response.status_code != 200:
            return None
        pack_card = response.json()
        return pack_card

    def get_cards(self, card_count=1):
        if self.pack_card == None:
            return None
        if self.status != None:
            return None

        deck_id = self.pack_card["deck_id"]
        response = requests.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count={card_count}")
        if response.status_code != 200:
            return False

        new_cards = response.json()
        if new_cards["success"] != True:
            return False
        self.remaining = new_cards["remaining"]

        arr_newCards = []
        for card in new_cards["cards"]:
            card_obj = Card(card)
            arr_newCards.append(card_obj)
            self.card_in_game.append(card_obj)
            self.score = self.score + card_obj.cost
            self.arr_cards_URL.append(card["image"])

        if self.score > 21:
            self.status = False
            text_game = "Очков: " + str(self.score) + " ВЫ ПРОИГРАЛИ!"

        elif self.score == 21:
            self.status = True
            text_game = "ВЫ ВЫИГРАЛИ!"
        else:
            self.status = None
            text_game = "Очков: " + str(self.score) + " в колоде осталось карт: " + str(self.remaining)

        return text_game

class GameRPS:
    values = ["Камень", "Ножницы", "Бумага"]

    def __init__(self):
        self.computerChoice = self.__class__.getRandomChoice()

    def newGame(self):
        self.computerChoice = self.__class__.getRandomChoice()

    @classmethod
    def getRandomChoice(cls):
        lenValues = len(cls.values)
        import random
        rndInd = random.randint(0, lenValues-1)
        return cls.values[rndInd]

    def playerChoice(self, player1Choice):
        winner = None

        code = player1Choice[0] + self.computerChoice[0]
        if player1Choice == self.computerChoice:
            winner = "Ничья!"
        elif code == "КН" or code == "БК" or code == "НБ":
            winner = "Вы выиграли!"
        else:
            winner = "Компьютер выиграл!"

        return f"{player1Choice} vs {self.computerChoice} = " + winner

    @staticmethod
    def onlineRPS(p1Choice, p2Choice):
        winner = None
        code = p1Choice[0] + p2Choice[0]
        if p1Choice == p2Choice:
            winner = "Ничья!"
        elif code == "КН" or code == "БК" or code == "НБ" :
            winner = "Ты выиграл!"
        else :
            winner = "Ты проиграл!"

        return f"{p1Choice} vs {p2Choice} = " + winner



def bl(bot, chat_id, message):
            koloda = [6, 7, 8, 9, 10, 2, 3, 4, 11] * 4
            random.shuffle(koloda)
            count = 0
            countd = 0
            a = 0

            def inputBot(message, text, bot):
                a = []

                def ret(message):
                    a.clear()
                    a.append(message.text)
                    return False

                a.clear()
                mes = bot.send_message(message.chat.id, text)
                bot.register_next_step_handler(message, ret)
                while a == []:
                    pass
                return a[0]

            while True:
                choice = inputBot(message, text='Будете брать карту?')
                if choice == 'Давай попробуем':
                    current = koloda.pop()
                    bot.send_message(chat_id, 'Вам попалась карта достоинством %d' % current)
                    count += current
                    random.shuffle(koloda)
                    a = a + 1
                    if count > 21:
                        bot.send_message(chat_id, 'Извините, но вы проиграли > 21')
                        bot.send_message(chat_id, "Главное меню")
                        break
                    elif count == 21:
                        bot.send_message(chat_id, 'Поздравляю, У вас БлэДжек')
                        bot.send_message(chat_id, "Главное меню")
                        break
                    else:
                        bot.send_message(chat_id, 'У вас %d очков.' % count)
                    if a == 1:
                        random.shuffle(koloda)
                        currend = koloda.pop()
                    bot.send_message(chat_id, 'Карта Диллера %d' % currend)
                    bot.send_message(chat_id, 'У Диллера %d очков.' % currend)
                elif choice == 'Пожалуй Нет':
                    if a > 1:
                        countd += currend
                        while True:
                            if countd < count:
                                random.shuffle(koloda)
                                currend = koloda.pop()
                                countd += currend
                            else:
                                break
                        bot.send_message(chat_id, 'У вас %d очков.' % count)
                        bot.send_message(chat_id, 'У Диллера %d очков.' % countd)
                        if countd > count:
                            if countd > 21:
                                bot.send_message(chat_id, "У Диллера очков > 21, Вы победилт)")
                                bot.send_message(chat_id, "Главное меню")
                                break
                            bot.send_message(chat_id, "У Диллера больше очков, Вы проиграли(")
                            bot.send_message(chat_id, "Главное меню")
                        elif count > countd:
                            bot.send_message(chat_id, "У Вас больше очков, Вы победили)")
                            bot.send_message(chat_id, "Главное меню")
                        elif count == count:
                            bot.send_message(chat_id, "Ничья")
                            bot.send_message(chat_id, "Главное меню")
                        break

                    else:
                        bot.send_message(chat_id, "Главное меню")
                        break
                elif  choice == 'Начать игру' or "<--Нажимай" or "Нажимай-->":
                    bot.send_message(chat_id, "Сейчас эти кнопки не пригодятся(да-да, Автор очень ленивый)")

                else:
                    bot.send_message(chat_id, "не верное значение")
                    bot.send_message(chat_id, "Главное меню")
                    break





if __name__ == "__main__":
    print("Этот код должен использоваться ТОЛЬКО в качестве модуля!")