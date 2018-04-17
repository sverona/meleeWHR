# Bracket representation

## Winner's side
Winner's bracket is represented as a heap; item N represents the match played by the
winner of the match between 2N and 2N + 1:

       1
     2   3
    4 5 6 7 
    ...

## Loser's side
Loser's bracket also has what is fundamentally a heap structure, but the representation
differs slightly:

        1
        2
     3     5
     4     6
    7  9 11 13
    8 10 12 14
    ...

The numbering is as follows:
 
* _Odd_ indices refer to rounds whose matches are between the winner of
a loser's bracket match and the loser of a winner's bracket match (LF, LQ.)
 - The child of odd-numbered item N is item N + 1.
 - The parent of odd-numbered item N is item 2 * round(N / 4).
* _Even_ indices refer to rounds whose matches are between two winners of
loser's bracket matches (LS, L8, ...).
 - The children of even-numbered item N are items 2N - 1, 2N + 1.
 - The parent of even-numbered item N is item N - 1.
 
Some nice properties of this system:
 * The ``round number'' (GF = 0, WF = 1...) is given by a constant plus the log_2 of 

## Grand finals
Winner's side (set 1) is located at winner's bracket item 0.
Loser's side (set 2) is located at loser's bracket item 0.
