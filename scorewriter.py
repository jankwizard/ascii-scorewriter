#!/usr/bin/env python3
# Basic musical keyboard scorewriter :)

# TODO
# ====
# * make output less confusing (flats/sharps...)
# * make the range programmable and more flexible. issues:
#   - octaves are hardcoded
#   - output takes up loads of width. `setterm -linewrap off` helps..
# * method to delete previous tab/line
# * export formatted score to txt file
# * save and load. csv where value is a "tab"?

# input rules
# ===========
# [a-g]#? -> take letter and space or # or b
# [1-5]   -> change octave
# return  -> submit tab
#
# regex
# =====
# tab    : ( [0-9]? ( [a-g]#? ) )* ;
# though there's basically no error checking right now. other input is ignored
#
# Things are internally a 3D array:
# [tabnum][octave][note]
# 0: [3:e]
# 1: [3:f#]
# 2: [4:c,g]

import re

def note2num(note):
    l = [ 'c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b' ]
    try:
        return l.index(note)
    except:
        return "" # ignore things like b# ...
def num2note(num):
    l = [ 'c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b' ]
    return l[num]

def tab_oct2str(tab):
    s = ''
    notenums = []
    for note in tab:
        notenums.append(note2num(note))

    for i in range(0, 12):
        if i in notenums:
            s += ' ' + num2note(i).ljust(2) + ' |'
        else:
            s += '    |'
    return s

def tab2str(tab):
    lo_oct = 3
    hi_oct = 5
    s = "|"
    for i in range(lo_oct, hi_oct+1):
        try:
            oct_tab = tab[i]
        except KeyError:
            tab[i] = []
            oct_tab = tab[i]
        s += tab_oct2str(oct_tab)
    return s

# define lexer
octave = "[0-9]"
note   = "[a-g]#?"
regex = "(" + octave + "|" + note + ")"
lexer   = re.compile( octave + "|" + note )

def tokenise(tab):
    return lexer.findall(tab)

def process_octave(x, state):
    state["octave"] = x

def update_tab_state(tokens, state):
    state["tab"] = {}
    for token in tokens:
        if re.search(octave, token) != None:
            state["octave"] = int(token)
        elif re.search(note, token) != None:
            try:
                state["tab"][state["octave"]] += [token]
            except KeyError:
                state["tab"][state["octave"]] = [token]

# main
state = {}
state["octave"] = 3
state["tab"] = {}
mytabs = []
while (1):
    string = input("tab: ")
    tokens = tokenise(string)
    update_tab_state(tokens, state)
    mytabs.append(state["tab"])
    # print the whole score
    for tab in mytabs:
        tabstr = tab2str(tab)
        print(tabstr)

exit()
