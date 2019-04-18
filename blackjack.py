import random


class BlackJack:

    def __init__(self):
        self.deck = Deck()
        self.players = []
        self.dealer = Player('dealer')

    def play(self):
        self.__print_welcome_message()
        self.__get_game_players()
        self.__deal_inital_player_hands()
        self.__deal_and_show_initial_dealer_hand()
        self.__players_play()
        self.__dealer_play()
        self.__get_winners()

    def __print_welcome_message(self):
        print('welcome to blackjack')

    def __get_player_num(self):
        num_players = input('How many players?')
        return int(num_players)

    def __get_game_players(self):
        num_players = None
        while not num_players:
            try:
                num_players = self.__get_player_num()
            except ValueError:
                print('must enter a number!')

        for n in range(num_players):
            player_name = input('Please enter player name:')
            self.players.append(Player(player_name))

    def __deal_inital_player_hands(self):
        for player in self.players:
            player.hit(self.deck.deal())
            player.hit(self.deck.deal())

    def __deal_and_show_initial_dealer_hand(self):
        self.dealer.hit(self.deck.deal())
        self.dealer.print_hand()

    def __players_play(self):
        for player in self.players:
            player.print_hand()
            self.__handle_player_score(player)
            while not player.sticking:
                response = input('Would you like to hit or stick?')
                if response == 'h':
                    player.hit(self.deck.deal())
                    player.print_hand()
                    self.__handle_player_score(player)
                elif response == 's':
                    player.stick()

    def __handle_player_score(self, player):
        if player.hand_score() > 21:
            print('You are BUST!')
            player.stick()
        elif player.hand_score() == 21:
            print('BLACKJACK!')
            player.stick()

    def __dealer_play(self):
        self.dealer.print_hand()
        while self.dealer.hand_score() < 17:
            self.dealer.hit(self.deck.deal())
            self.dealer.print_hand()
            if self.dealer.hand_score() > 21:
                print('Dealer BUST!')
            if self.dealer.hand_score() == 21:
                print('Dealer has BLACKJACK!')

    def __get_winners(self):
        potential_winners = list(filter(lambda x: x.hand_score() <= 21, self.players))
        if self.dealer.hand_score() == 21:
            print('Dealer has won!')
        else:
            for player in potential_winners:
                if player.hand_score() > self.dealer.hand_score():
                    print(f'{player.name} has won!')

class Card:

    value_lookup = {
         'A': 11, '2': 2, '3': 3, '4': 4, '5': 5,
         '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
         'J': 10, 'Q': 10, 'K': 10
        }

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def is_ace(self):
        if self.rank == 'A':
            return True
        return False

    def value(self):
        return self.value_lookup[self.rank]

    def __str__(self):
        return self.rank + self.suit


class Deck:

    suits = ['D', 'H', 'S', 'C']
    ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

    def __init__(self):
        self.cards = self.__shuffled_deck()

    def __shuffled_deck(self):
        cards = []
        for s in self.suits:
            for r in self.ranks:
                cards.append(Card(s, r))
        random.shuffle(cards)
        return cards

    def deal(self):
        return self.cards.pop()


class Player:

    def __init__(self, name):
        self.name = name
        self.hand = []
        self.sticking = False

    def hit(self, card):
        self.hand.append(card)

    def stick(self):
        self.sticking = True

    def hand_score(self):
        score = 0
        for card in self.hand:
            score += card.value()
        return score

    def print_hand(self):
        print(f"{self.name}'s hand is: {' '.join(str(c) for c in self.hand)} ({self.hand_score()})")


if __name__ == '__main__':
    BlackJack().play()

