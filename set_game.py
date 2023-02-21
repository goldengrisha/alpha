import random


class Card:
    def __init__(self, *attrs):
        self.attrs = attrs

    def isset(self, card1, card2):
        def all_same(v0, v1, v2):
            return v0 == v1 and v1 == v2

        def all_different(v0, v1, v2):
            return len({v0, v1, v2}) == 3

        return all(
            all_same(v0, v1, v2) or all_different(v0, v1, v2)
            for (v0, v1, v2) in zip(self.attrs, card1.attrs, card2.attrs)
        )

    @staticmethod
    def get_all_combinations():
        return [
            Card(att0, att1, att2, att3)
            for att0 in (0, 1, 2)
            for att1 in (0, 1, 2)
            for att2 in (0, 1, 2)
            for att3 in (0, 1, 2)
        ]


class Deck:
    def __init__(self, n=12):
        self.all_cards = Card.get_all_combinations()
        self.n = n

    def find_sets(self):
        random.shuffle(self.all_cards)

        found = []
        cards = self.all_cards[: self.n]
        self.all_cards = self.all_cards[self.n :]
        for i, ci in enumerate(cards):
            for j, cj in enumerate(cards[i + 1 :], i + 1):
                for k, ck in enumerate(cards[j + 1 :], j + 1):
                    if ci.isset(cj, ck):
                        found.append((ci, cj, ck))

        return found


class Game:
    def __init__(self):
        self.deck = Deck()

    def start(self):
        total_score = 0
        while len(self.deck.all_cards) >= 3:
            found_sets = self.deck.find_sets()
            total_score += len(found_sets)

        print("\nYour score is", total_score)


if __name__ == "__main__":
    game = Game()
    game.start()
