# Chaos-Chess
A Python script for randomly generating new chess variants. Just run the script and it generates a brand-new variant of chess, with randomly generated pieces in a never-before-seen arrangement. The moves of each piece are recorded in Betza's funny notation <https://en.wikipedia.org/wiki/Betza%27s_funny_notation>.

# Features
* The script generates names and labels for every piece. Pieces common to variant chess keep their normal names, while more novel pieces have randomly generated names.
* The generated layout is checked to ensure that every pawn is protected at the start of the game.
* Randomly generated pieces are usually simple, but sometimes include "chaos" aspects, such as:
  * Movement restrictions: movements that can only be used peacefully or when capturing.
  * Direction restictions: movements that only work in specific directions.
  * Bent moves: movements that are a sequence of other moves, such as "make a Wazir move, then a Bishop move".
* A summary of rule tweaks are included, adjusting the pawns and castling to account for the board size.

# Example Output
```
Dotowa Chess:

  abcdefghi
8 qosukxtml
7 ppppppppp
6 ---------
5 ---------
4 ---------
3 ---------
2 PPPPPPPPP
1 QOSUKXTML

Piece List:
K: King (WF)
Q: Queen (RB)
O: Dotowa (Dt[WN])
S: Marquis (WN)
U: Fewefu (FWfb)
X: Woodman (WD)
T: Acrobat (DR)
M: Shaman (AB)
L: Cardinal (NB)

Rules:
All normal chess rules apply, except as noted below.
The King can castle with the pieces in the corners of its starting rank.
All normal castling rules apply; the king moves two spaces towards the other piece.
When promoting, Pawns may promote to any piece in this variant, except for the King.

```
