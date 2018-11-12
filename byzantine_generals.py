from collections import Counter


class Lieutenant:
    def __init__(self, id, traitor=False):
        self.id = id
        self.lieutenants = []
        self.vals = []
        self.traitor = traitor

    def __call__(self, m):
        self._om_algorithm(general=self,
                           m=m,
                           val=True,
                           )

    def _om_algorithm(self, general, m, val):
        if m < 0:
            self.vals.append(val)
        if m == 0:
            for l in self.lieutenants:
                l(self,
                  general=self,
                  m=(m - 1),
                  val=((not val) if self.traitor else val),
                  )
            else:
                for l in self.lieutenants:
                    if l is not self and l is not general:
                        l(self, m - 1, val)

        @property
        def decision(self):
            c = Counter(self.lieutenants)


def init_lieutenants(num, traitors=0):
    lieutenants = []
    for i in range(num):
        lieutenants.append(Lieutenant(i))
    for l in lieutenants[-traitors:]:
        l.traitor = True
    for l in lieutenants:
        l.lieutenants = lieutenants
    return lieutenants


def print_decisions(lieutenants):
    for i, l in enumerate(lieutenants):
        print("Lieutenant {}: {}".format(i, l.decision))


def main():
    lieutenants = init_lieutenants(num=5, traitors=1)
    lieutenants[0](3)
    print_decisions(lieutenants)


if __name__ == "__main__":
    main()
