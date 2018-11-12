from collections import Counter


class Lieutenant:
    def __init__(self, id, is_traitor=False):
        self.id = id
        self.lieutenants = []
        self.vals = []
        self.is_traitor = is_traitor

    def __call__(self, m):
        self.om_algorithm(general=self,
                          m=m,
                          val=True,
                          )

    def om_algorithm(self, general, m, val):
        if m < 0:
            self.vals.append(val)
        elif m == 0:
            for l in self.lieutenants:
                l.om_algorithm(
                    general=self,
                    m=(m - 1),
                    # val=((not val) if self.is_traitor else val),
                    val=(not self.is_traitor),
                )
        else:
            for l in self.lieutenants:
                if l is not self and l is not general:
                    l.om_algorithm(
                        general=self,
                        m=(m - 1),
                        # val=((not val) if self.is_traitor else val),
                        val=(not self.is_traitor),
                    )

    @property
    def decision(self):
        c = Counter(self.vals)
        return c.most_common()


def init_lieutenants(num, traitors=0):
    lieutenants = []
    for i in range(num):
        lieutenants.append(Lieutenant(i))
    for l in lieutenants[-traitors:]:
        l.is_traitor = True
    for l in lieutenants:
        l.lieutenants = lieutenants
    return lieutenants


def print_decisions(lieutenants):
    for i, l in enumerate(lieutenants):
        print("Lieutenant {}: {}".format(i, l.decision))


def main():
    lieutenants = init_lieutenants(num=3, traitors=1)
    lieutenants[0](m=2)
    print_decisions(lieutenants)


if __name__ == "__main__":
    main()
