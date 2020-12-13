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
            oct_tab = tab[str(i)]
        except KeyError:
            tab[str(i)] = []
            oct_tab = tab[str(i)]
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
            state["octave"] = token
        elif re.search(note, token) != None:
            try:
                state["tab"][state["octave"]] += [token]
            except KeyError:
                state["tab"][state["octave"]] = [token]

import json
def save_score(score):
    # Serialize data into file:
    json.dump( score, open( "/tmp/score.json", 'w' ) )

def load_score(state, f):
    # Read data from file:
    state["score"] = json.load( open( f ) )
    print(state["score"])

def print_score(score):
    for tab in score:
        tabstr = tab2str(tab)
        print(tabstr)

# main
state = {}
state["octave"] = '3'
state["tab"] = {}
state["score"] = []
usage = '''usage:
======
default entry (tabs): (''' + octave + note + ''')+
control options:
\tsave            - saves score
\ttsave            - saves score
\tload <filename> - loads score
\tclear           - clear score
\tquit            - quit"'''
print(usage)
while (1):
    string = input(": ")
    if string.startswith('save') or string.startswith('load'):
        try:
            f = string.split()[1]
            if 'save' == string.split()[0]:
                save_score(state["score"])
                print("saved to " + f)
            elif 'load' == string.split()[0]:
                load_score(state, f)
                print_score(state["score"])
                print(f + " loaded.")
        except:
            print("ERR: can't access file or no file given")
    elif string == 'quit':
        exit()
    elif string == 'clear':
        state.clear()
        state["octave"] = '3'
        state["score"] = []
    else:
        # assume a new tab was entered
        tokens = tokenise(string)
        update_tab_state(tokens, state)
        state["score"].append(state["tab"])
        # print the whole score
        print_score(state["score"])


exit()
