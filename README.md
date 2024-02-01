# Chaos-Chess
A Python script for randomly generating new chess variants. Just run the script and it generates a brand-new version of chess, with randomly generated pieces in a never-before-seen arrangement. The moves of each piece are recorded in Betza's funny notation <https://en.wikipedia.org/wiki/Betza%27s_funny_notation>.

# Features
* The script generates names and labels for every piece. Pieces common to variant chess keep their normal names, while more novel pieces have randomly generated names.
* The generated layout is checked to ensure that every pawn is protected at the start of the game.

# Example Output
```Rudade Chess:

  abcdefghi
9 oliukuilo
8 ftexwxetf
7 ppppppppp
6 ---------
5 ---------
4 ---------
3 PPPPPPPPP
2 FTEXWXETF
1 OLIUKUILO

Piece List:
K: King (WF)
O: Rohu (RH)
L: Paladin (DB)
I: Soldier (AR)
U: Buhu (BH)
F: Ferz (F)
T: Tower (FR)
E: Rudade (RDD)
X: Archbishop (WB)
W: Wazir (W)```
