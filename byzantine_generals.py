from argparse import ArgumentParser
from collections import Counter


class Lieutenant:
    def __init__(self, id, is_traitor=False):
        self.id = id
        self.lieutenants = []
        self.orders = []
        self.is_traitor = is_traitor

    def __call__(self, m, order):
        self.om_algorithm(commander=self,
                          m=m,
                          order=order,
                          )

    def _next_order(self, is_traitor, order, i):
        if is_traitor:
            if i % 2 == 0:
                return "ATTACK" if order == "RETREAT" else "RETREAT"
        return order

    def om_algorithm(self, commander, m, order):
        if m < 0:
            self.orders.append(order)
        elif m == 0:
            for i, l in enumerate(self.lieutenants):
                l.om_algorithm(
                    commander=self,
                    m=(m - 1),
                    order=self._next_order(self.is_traitor, order, i)
                )
        else:
            for i, l in enumerate(self.lieutenants):
                if l is not self and l is not commander:
                    l.om_algorithm(
                        commander=self,
                        m=(m - 1),
                        order=self._next_order(self.is_traitor, order, i)
                    )

    @property
    def decision(self):
        c = Counter(self.orders)
        return c.most_common()


def init_lieutenants(generals):
    lieutenants = []
    for i, g in enumerate(generals):
        l = Lieutenant(i)
        if g == "l":
            pass
        elif g == "t":
            l.is_traitor = True
        else:
            print("Error, bad input in generals list: {}".format(generals))
            exit(1)
        lieutenants.append(l)
    # Add list of other lieutenants to each lieutenant.
    for l in lieutenants:
        l.lieutenants = lieutenants
    return lieutenants


def print_decisions(lieutenants):
    for i, l in enumerate(lieutenants):
        print("Lieutenant {}: {}".format(i, l.decision))


def main():
    parser = ArgumentParser()
    parser.add_argument("-m", type=int, dest="recursion",
                        help=" The level of recursion in the algorithm, where M > 0")
    parser.add_argument("-G", type=str, dest="generals",
                        help=" A string of generals (ie 'l,t,l,l,l'...), where l is loyal and t is a traitor.  "
                             "The first general is the Commander.")
    parser.add_argument("-O", type=str, dest="order",
                        help=" The order the commander gives to its lieutenants (Oc ∈ {ATTACK,RETREAT})")

    args = parser.parse_args()

    generals = [x.strip() for x in args.generals.split(',')]

    lieutenants = init_lieutenants(generals=generals)
    lieutenants[0](m=args.recursion, order=args.order)
    print_decisions(lieutenants)


if __name__ == "__main__":
    main()
