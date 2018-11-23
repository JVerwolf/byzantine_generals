# Byzantine Generals
### Background
This problem was introduced by Leslie Lamport in the paper 
[The Byzantine Generals Problem](https://www.microsoft.com/en-us/research/uploads/prod/2016/12/The-Byzantine-Generals-Problem.pdf), 
where he describes the problem as follows:

> “Reliable computer systems must handle malfunctioning 
> components that give conflicting information to different 
> parts of the system. This situation can be expressed 
> abstractly in terms of a group of generals of the Byzantine 
> army camped with     their troops around an enemy city. 
> Communicating only by messenger, the generals must agree 
> upon a common battle plan. However, one or more of them may 
> be traitors who will try     to confuse the others. The 
> problem is to find an algorithm to ensure that the loyal 
> generals will reach agreement.”

It is imperative that the loyal generals work as a together 
as a unit, or else they run the risk of being routed by the 
enemy.

In his paper, Lamport goes on to describe an algorithm that 
uses oral messages.  He shows that, when using oral messages, 
this problem is solvable if-and-only-if more than two thirds 
of the generals are loyal. 


### Algorithm
Lamport’s algorithm is as follows. Note that the parameter 
“m” is the degree of recursion.

**Algorithm OM(0)** (Base Case)
1. The commander sends his value to every lieutenant.
2. Each lieutenant uses the value he receives from the 
commander, or uses the value RETREAT if he receives no value. 

**Algorithm OM(m), m > O.** 
1. The commander sends his value to every lieutenant. 
2. For each i, let vi be the value Lieutenant i receives 
from the commander, or else be RETREAT if he receives no 
value. Lieutenant i acts as the commander in Algorithm 
OM(m - 1) to send the value vi to each of the n - 2 other 
lieutenants. 
3. For each i, and each j ~ i, let vj be the value 
Lieutenant i received from Lieutenant j in step (2) (using 
Algorithm  OM(m  -  1)), or else RETREAT if he received no 
such value. Lieutenant i uses the value majority 
(vl.....v,-1).

### Implementation
Lamport's OM algorithm is implemented 
[here](byzantine_generals.py).  The program can be run as follows:
```
% python3 byzantine_generals.py -h       
usage: byzantine_generals.py [-h] [-m RECURSION] [-G GENERALS] [-O ORDER]

optional arguments:
  -h, --help        show this help message and exit
  -m RECURSION      The level of recursion in the algorithm, where M > 0
  -G GENERALS       A string of generals (ie 'l,t,l,l,l'...), where l is loyal and
                    t is a traitor. The first general is the Commander.
  -O ORDER          The order the commander gives to its lieutenants (O ∈
                    {ATTACK,RETREAT})
```

For example:
```
% python3 byzantine_generals.py -m 4 -G l,t,l,l,l -O ATTACK
Lieutenant 0: [('RETREAT', 62), ('ATTACK', 46)]
Lieutenant 1: [('ATTACK', 55), ('RETREAT', 53)]
Lieutenant 2: [('RETREAT', 62), ('ATTACK', 46)]
Lieutenant 3: [('ATTACK', 55), ('RETREAT', 53)]
Lieutenant 4: [('RETREAT', 62), ('ATTACK', 46)]
```
 
