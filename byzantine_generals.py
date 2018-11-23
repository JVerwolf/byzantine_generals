from argparse import ArgumentParser
from collections import Counter


class General:
    def __init__(self, id, is_traitor=False):
        self.id = id
        self.other_generals = []
        self.orders = []
        self.is_traitor = is_traitor

    def __call__(self, m, order):
        """When a general is called, it acts as the commander,
        and begins the OM algorithm by passing its command to
        all the other generals.

        Args:
            m (int): The level of recursion.
            order (str): The order, such that order ∈ {"ATTACK","RETREAT"}.

        """
        self.om_algorithm(commander=self,
                          m=m,
                          order=order,
                          )

    def _next_order(self, is_traitor, order, i):
        """A helper function to determine what each commander
        should pass on as the next order. Traitors will pass-
        on the opposite command if the index of the general
        in their `other_generals` list is odd.

        Args:
            is_traitor (bool): True for traitors.
            order (str): The received order, such that
                order ∈ {"ATTACK","RETREAT"}.
            i(int): The index of the general in question.

        Returns:
            str: The resulting order ("ATTACK" or "RETREAT").

        """
        if is_traitor:
            if i % 2 == 0:
                return "ATTACK" if order == "RETREAT" else "RETREAT"
        return order

    def om_algorithm(self, commander, m, order):
        """The OM algorithm from Lamport's paper.

        Args:
            commander (General): A reference to the general
                who issued the previous command.
            m (int): The level of recursion .
            order (str): The received order, such that
                order ∈ {"ATTACK","RETREAT"}.

        """
        if m < 0:
            self.orders.append(order)
        elif m == 0:
            for i, l in enumerate(self.other_generals):
                l.om_algorithm(
                    commander=self,
                    m=(m - 1),
                    order=self._next_order(self.is_traitor, order, i)
                )
        else:
            for i, l in enumerate(self.other_generals):
                if l is not self and l is not commander:
                    l.om_algorithm(
                        commander=self,
                        m=(m - 1),
                        order=self._next_order(self.is_traitor, order, i)
                    )

    @property
    def decision(self):
        """Returns a tally of the General's received commands.

        """
        c = Counter(self.orders)
        return c.most_common()


def init_generals(generals_spec):
    """Creates a list of generals, given a string
    input from arg-parse.

    Args:
        generals_spec (list): A list of generals
            of the form 'l,t,l,t...", where "l"
            is loyal and "t" is a traitor.

    Returns:
        list: A list of initialized generals.
    """
    generals = []
    for i, spec in enumerate(generals_spec):
        general = General(i)
        if spec == "l":
            pass
        elif spec == "t":
            general.is_traitor = True
        else:
            print("Error, bad input in generals list: {}".format(generals_spec))
            exit(1)
        generals.append(general)
    # Add list of other generals to each general.
    for general in generals:
        general.other_generals = generals
    return generals


def print_decisions(generals):
    for i, l in enumerate(generals):
        print("General {}: {}".format(i, l.decision))


def main():
    parser = ArgumentParser()
    parser.add_argument("-m", type=int, dest="recursion",
                        help=" The level of recursion in the algorithm, where M > 0")
    parser.add_argument("-G", type=str, dest="generals",
                        help=" A string of generals (ie 'l,t,l,l,l'...), where l is loyal and t is a traitor.  "
                             "The first general is the Commander.")
    parser.add_argument("-O", type=str, dest="order",
                        help=" The order the commander gives to the other generals (O ∈ {ATTACK,RETREAT})")
    args = parser.parse_args()

    generals_spec = [x.strip() for x in args.generals.split(',')]
    generals = init_generals(generals_spec=generals_spec)
    generals[0](m=args.recursion, order=args.order)
    print_decisions(generals)


if __name__ == "__main__":
    main()
