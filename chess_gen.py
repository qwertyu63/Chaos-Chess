# This program randomly generates chess variants.
# It randomly selects the board size and then generates an assortment of pieces to fill it.
# It considers the board size when creating pieces to create.
# It runs a check to make sure all pawns are protected in the opening layout, starting over if it isn't.
# It then displays the new variant in an easily readable format.
from random import randint
from math import ceil
from copy import deepcopy

# Listing the atoms pieces can be made from.
nor_atoms = ["W", "F", "D", "A", "N", "R", "B"]
big_atoms = ["C", "Z", "H"]
long_atoms = ["M", "G", "S"]

atom_values = [2,2,1,1,3,4,5,3,2,1,5,2,2]
atom_bind = [0,1,2,3,0,0,1,1,0,0,0,1,2]

atom_sight = [0,1,"","",2,0,1,3,"","",2,"",""]
extra_sight = ["","",0,2,1,"","","",3,0,1,0,0]

long_convert = {"M": "NN", "G": "DD", "S": "AA"}

# This is a list of default piece names.
prebuild = {
    "W": "Wazir",
    "F": "Ferz",
    "D": "Dabbaba",
    "A": "Alfil",
    "N": "Knight",
    "R": "Rook",
    "B": "Bishop",
    "C": "Camel",
    "Z": "Zebra",
    "WF": "Man",
    "WD": "Woodman",
    "WA": "Phoenix",
    "WN": "Marquis",
    "WB": "Archbishop",
    "WC": "Sorcerer",
    "WZ": "Ranger",
    "FD": "Scout",
    "FA": "Preacher",
    "FN": "Priest",
    "FR": "Tower",
    "FC": "Wizard",
    "FZ": "Druid",
    "DA": "Spider",
    "DN": "Archer",
    "DR": "Acrobat",
    "DB": "Paladin",
    "AN": "Hunter",
    "AR": "Soldier",
    "AB": "Shaman",
    "NR": "Chancellor",
    "NB": "Cardinal",
    "NC": "Wildebeest",
    "NZ": "Moose",
    "NH": "Warlord",
    "RB": "Queen",
    "RC": "Barbarian",
    "RZ": "Monk",
    "BC": "Caliph",
    "BZ": "Witch",
    "CZ": "Ram",
    "WFN": "Centaur",
    "DAN": "Squirrel",
    "NCZ": "Dragon",
    "NN": "Nightrider",
    "BNN": "Unicorn",
    "RNN": "Pegasus",
    "DD": "Warmachine",
    "AA": "Elephant Rider"
}

# This fuction checks for duplicate moves or copied moves. It also adds a 50% failure chance to jumping riders.
def clearcheck(new, list):
    if new in list:
        return False
    locks = {
        "W": "R", "R": "W",
        "F": "B", "B": "F",
        "N": "M", "M": "N",
        "D": "G", "G": "D",
        "A": "S", "S": "A",
    }
    if new in locks.keys():
        if locks[new] in list:
            return False
    if len(list) > 0 and new in long_atoms:
        return bool(randint(0,1))
    return True

# This function converts the generated list of piece moves into a valid piece.
def compile_piece(code):
    label = ""
    value = -1
    bind = 9
    sight = [[],[]]
    for i in range(len(atoms)-1):
        if atoms[i] in code:
            if atoms[i] in long_atoms:
                label += long_convert[atoms[i]]
            else:
                label += atoms[i]
            value += atom_values[i]+1
            if bind > atom_bind[i]:
                bind = atom_bind[i]
            if atom_sight[i] != "":
                sight[0].append(atom_sight[i])
            if extra_sight[i] != "":
                sight[1].append(extra_sight[i])
    value -= bind
    if label == "H":
        value = 0
    name = label
    if label in prebuild.keys():
        name = prebuild[label]
    else:
        name = make_name(label)
    return (label, value, name, sight)

# This function generates a name for a piece, using the letters from its name.
def make_name(word):
    name = ""
    for i in word:
        name += i
        if i not in ["A", "E", "I", "O", "U"]:
            name += ["A", "E", "I", "O", "U"][randint(0,4)]
    return name.title()

# This function selects a letter to represent a piece.
def getalpha(name, code):
    if len(code) == 1:
        return code
    if code == "RB":
        return "Q"
    step = 0
    while True:
        if step >= len(name):
            try:
                return default.pop(0)
            except IndexError:
                return "G"
        elif name[step].upper() in piece_label or name[step].upper() in atoms or name[step].upper() in ["Q", "P"]:
            step+=1
        else:
            if name[step].upper() in default:
                default.remove(name[step].upper())
            return name[step].upper()

# This function tracks the names and values of pieces to eventually name the chess variant.
def game_name_check(name, value, code):
    global name_hold, name_value, backup_name, backup_value
    if code not in prebuild.keys():
        if value >= name_value:
            name_hold = name
            name_value = value
    else:
        if value >= backup_value:
            backup_name = name
            backup_value = value

# This function checks which pawns the specified piece can see in the opening setup.
def pawn_vision(list, slot, numbers):
    for i in numbers:
        if slot-i>=0:
            list[slot-i]=True
        if slot+i<len(list):
            list[slot-i]=True
    return list

# ---------------------------------
# This is the start of the loop that only breaks when a valid variant is generated.
# ---------------------------------

while True:
    # This is a placeholder for where the name of the variant will be generated.
    game_name = "Chaos Chess"
    name_hold = ""
    name_value = 0
    backup_name = ""
    backup_value = 0

    default = ["X", "Z", "J", "K", "V", "Y"]

    # Setting the size and arrangement of the board.
    files = randint(6,13)
    ranks = randint(6,13)
    camp = 1
    if ranks >= randint(9,12):
        camp = 2
    sym = False
    if files >= randint(6,10):
        sym = True
    mirror = bool(randint(0,1))
    
    # This generates a list of moves to be used. The longer range moves are only used if the board is big enough.
    atoms = deepcopy(nor_atoms)
    if ranks-camp > 5:
        atoms += big_atoms
        if randint(0,1):
            atoms += long_atoms
    
    # Create a list of pieces.
    pieces = ["K"]
    piece_desc = ["K: King (WF)"]
    piece_label = ["K"]
    piece_sight = {"K": [[0,1],[]]}

    # Determine how many pieces need to be created.
    piece_count = (files * camp)
    if sym:
        piece_count = ceil(piece_count/2)
    else:
        piece_count -= 1
    
    # Start creating the pieces.
    die = [1,2,2,3]
    while piece_count:
        parts = die[randint(0,len(die)-1)]
        code = []
        value = 0
        bind = 9
        while parts:
            roll = randint(0, len(atoms)-1)
            if clearcheck(atoms[roll], code):
                code.append(atoms[roll])
            parts -= 1
        new_piece = compile_piece(code)
        if new_piece[1] > 0 and new_piece[1] < 11 and new_piece not in pieces:
            pieces.append(new_piece[0])
            label = getalpha(new_piece[2], new_piece[0])
            desc = label + ": "+new_piece[2]+ " (" + new_piece[0] + ")"
            piece_desc.append(desc)
            piece_label.append(label)
            piece_sight[label] = new_piece[3]
            game_name_check(new_piece[2], new_piece[1], new_piece[0])
            piece_count-=1
    
    # Creating the initial board state.
    home_row = ["-"] * files
    king_home = (files//2)
    
    counter = 1
    for i in range(0, king_home):
        home_row[i] = piece_label[counter]
        counter += 1
    
    if not sym:
        for i in range(king_home+1, files):
            home_row[i] = piece_label[counter]
            counter += 1
    else:
        new_count = 1
        for i in range(1, king_home+1):
            home_row[i*-1] = piece_label[new_count]
            new_count += 1
    
    home_row[king_home] = "K"
    
    if camp == 2:
        extra_row = ["-"] * files
        if not sym:
            for i in range(0, files):
                extra_row[i] = piece_label[counter]
                counter += 1
        else:
            try:
                for i in range(0, king_home):
                    extra_row[i] = piece_label[counter]
                    extra_row[(i+1)*-1] = piece_label[counter]
                    counter += 1
                if extra_row[king_home] == "-":
                    extra_row[king_home] = piece_label[counter]
            except IndexError:
                print("Files: "+str(files))
                print("Pieces: "+str(piece_label))
                print("Count: "+str(counter))

    # This section checks to make sure every pawn is protected in the opening lineup.
    vision_field = [False] * files
    if camp == 1:
        for i, j in enumerate(home_row):
            vision_field = pawn_vision(vision_field, i, piece_sight[j][0])
    if camp == 2:
        for i, j in enumerate(extra_row):
            vision_field = pawn_vision(vision_field, i, piece_sight[j][0])
        for i, j in enumerate(home_row):
            vision_field = pawn_vision(vision_field, i, piece_sight[j][1])

    # Finally, this checks if every pawn is protected in the opening layout. If they all are, it approves the variant.
    success = True
    for i in vision_field:
        if not i:
            success = False
    if success:
        break

# -------------------------
# This is the end of the loop. If we get here, a valid chess variant has been created.
# -------------------------

# Creating and naming the variant. It is named after the strongest piece that doesn't have a predefined name; if no such pieces exist, it defaults to the strongest piece overall.
if name_hold:
    game_name = name_hold + " Chess"
else:
    game_name = backup_name + " Chess"
print(game_name + ":\n")

ranks_left = ranks

letters = "abcdefghijklmnopqrstuvwxyz"
if ranks >= 10:
    print("   ", end="")
else:
    print("  ", end="")
for i in range(0,files):
    print(letters[i], end="")
print()

# Displaying the initial board state. 
rank_count=ranks

def label_rank(count):
    if ranks >= 10 and count < 10:
        print(" "+str(rank_count)+" ", end="")
    else:
        print(str(rank_count)+" ", end="")
    return count-1

rank_count = label_rank(rank_count)
for i in home_row:
    print(i.lower(), end="")
print()
ranks_left -= 2

if camp == 2:
    rank_count = label_rank(rank_count)
    for i in extra_row:
        print(i.lower(), end="")
    print()
    ranks_left -= 2

rank_count = label_rank(rank_count)
for i in ["P"] * files:
    print(i.lower(), end="")
print()
ranks_left -= 2

while ranks_left != 0:
    rank_count = label_rank(rank_count)
    for i in ["-"] * files:
        print(i, end="")
    print()
    ranks_left -= 1

if mirror:
    home_row.reverse()
    if camp == 2:
        extra_row.reverse()

rank_count = label_rank(rank_count)
for i in ["P"] * files:
    print(i, end="")
print()

if camp == 2:
    rank_count = label_rank(rank_count)
    for i in extra_row:
        print(i, end="")
    print()

rank_count = label_rank(rank_count)
for i in home_row:
    print(i, end="")
print()

print("\nPiece List:")

entries = []
for i in piece_desc:
    if i not in entries:
        entries.append(i)
        print(i)
