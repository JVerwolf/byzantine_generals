# The Byzantine Generals Problem
### Background
This problem was introduced by Leslie Lamport in his paper 
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

As such, it is imperative that the loyal generals work as a together 
as a unit, else they run the risk of being routed by the 
enemy.

### Algorithm

In his paper, Lamport describes an algorithm that uses oral 
messages.  He shows that when using oral messages, this 
problem is solvable if-and-only-if more than two thirds of 
the generals are loyal. 

Lamport’s algorithm is as follows _(Note that the parameter 
“m” is the degree of recursion)_:
 


> **Algorithm OM(0)** (Base Case)
> 1. The commander sends his value to every lieutenant.
> 2. Each lieutenant uses the value he receives from the 
> commander, or uses the value RETREAT if he receives no value. 
> 
> **Algorithm OM(m), m > O.** 
> 1. The commander sends his value to every lieutenant. 
> 2. For each i, let v\[i] be the value General i receives 
> from the commander, or else be RETREAT if he receives no 
> value. General i acts as the commander in Algorithm 
> OM(m - 1) to send the value vi to each of the n - 2 other 
> lieutenants. 
> 3. For each i, and each j != i, let v\[j] be the value 
> General i received from General j in step (2) (using 
> Algorithm  OM(m  -  1)), or else RETREAT if he received no 
> such value. General i uses the value majority 
> (v\[0].....v\[n]).
> 
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
  -O ORDER          The order the commander gives to the other generals (O ∈
                    {ATTACK,RETREAT})
```

For example:
```
% python3 byzantine_generals.py -m 4 -G l,t,l,l,l -O ATTACK
General 0: [('RETREAT', 62), ('ATTACK', 46)]
General 1: [('ATTACK', 55), ('RETREAT', 53)]
General 2: [('RETREAT', 62), ('ATTACK', 46)]
General 3: [('ATTACK', 55), ('RETREAT', 53)]
General 4: [('RETREAT', 62), ('ATTACK', 46)]
```
 
### Testing:
In his paper, Lamport proves that:
> For any m, Algorithm OM(m) satisfies conditions that
> *All loyal generals decide upon the same plan of action* and
> *A small number of traitors cannot cause the loyal 
> generals to adopt a bad plan* if there are more than 3m 
> generals and at most m traitors. 

Lets pick m to be 3, with 10 (>3m) generals and 3 (=m) traitors:
```
% python3 byzantine_generals.py -m 3 -G l,l,l,t,t,l,l,t,l -O ATTACK
General 0: [('ATTACK', 303), ('RETREAT', 273)]
General 1: [('ATTACK', 403), ('RETREAT', 173)]
General 2: [('ATTACK', 303), ('RETREAT', 273)]
General 3: [('ATTACK', 403), ('RETREAT', 173)]
General 4: [('ATTACK', 303), ('RETREAT', 273)]
General 5: [('ATTACK', 403), ('RETREAT', 173)]
General 6: [('ATTACK', 303), ('RETREAT', 273)]
General 7: [('ATTACK', 403), ('RETREAT', 173)]
General 8: [('ATTACK', 303), ('RETREAT', 273)]
General 9: [('ATTACK', 403), ('RETREAT', 173)]
```
As shown, this works as expected. Each general votes for
the correct course of action.

Now, let's examine what will happen if we set the number of 
generals to be less that what is specified in Lamport's
proof.

Lets pick m to be 3, with 9 (=3m) generals and 3 (=m) traitors:
```
%python3 byzantine_generals.py -m 3 -G l,l,l,t,t,l,l,t,l -O ATTACK
General 0: [('RETREAT', 210), ('ATTACK', 182)]
General 1: [('ATTACK', 244), ('RETREAT', 148)]
General 2: [('RETREAT', 210), ('ATTACK', 182)]
General 3: [('ATTACK', 244), ('RETREAT', 148)]
General 4: [('RETREAT', 210), ('ATTACK', 182)]
General 5: [('ATTACK', 244), ('RETREAT', 148)]
General 6: [('RETREAT', 210), ('ATTACK', 182)]
General 7: [('ATTACK', 244), ('RETREAT', 148)]
General 8: [('RETREAT', 210), ('ATTACK', 182)]
```
Here we see that the condition no longer holds.  Note that
while Lamport only specifies the conditions for the 
success case, there is no guarantee that a given configuration
of parameters will cause failure: sometimes it will work, 
and other times it will not.
