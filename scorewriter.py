#!/usr/bin/env python3
# Basic musical keyboard scorewriter :)

# TODO
# ====
# * make output less confusing (flats/sharps...)
# * make the range programmable and more flexible. issues:
#   - output takes up loads of width. `setterm -linewrap off` helps..

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
import json
import sys

# defaults
fmt = {
    "oct_lo": '3',
    "oct_hi": '4',
    "note_lo": 'c',
    "note_hi": 'b',
}

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
    s = "|"
    for i in range(int(fmt["oct_lo"]), int(fmt["oct_hi"])+1):
        try:
            oct_tab = tab[str(i)]
        except KeyError:
            tab[str(i)] = []
            oct_tab = tab[str(i)]
        s += tab_oct2str(oct_tab)

    lo = note2num(fmt["note_lo"])
    hi = note2num(fmt["note_hi"])
    if hi == 11:
        return s[lo*5:]
    else:
        return s[lo*5:(-11+hi)*5]

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

def save_score(score):
    # Serialize data into file:
    json.dump( score, open( "/tmp/score.json", 'w' ) )

def load_score(state, f):
    # Read data from file:
    state["score"] = json.load( open( f ) )
    print(state["score"])

def score2string(score):
    tabstr = ""
    for tab in score:
        tabstr += tab2str(tab) + '\n'
    return tabstr

# main
state = {}
state["octave"] = '3'
state["tab"] = {}
state["score"] = []
usage = '''usage:
======
default entry (tabs): (''' + octave + note + ''')+
control options:
\tsave              - saves score
\tload <filename>   - loads score
\texport <filename> - exports score as | formatted | text | file |
\tdel               - delete most recent tab
\tclear             - clear entire score
\tset <op> <val>    - sets formatting options for score [EXPERIMENTAL]
\tprint             - print score
\t\tops : oct_lo, oct_hi, note_lo, note_hi
\thelp              - print this
\tquit              - quit"'''
print(usage)
while (1):
    string = input(": ")
    if string.startswith('save') or string.startswith('load') or string.startswith('export'):
        try:
            f = string.split()[1]
            if 'save' == string.split()[0]:
                save_score(state["score"])
                print("saved to " + f)
            if 'load' == string.split()[0]:
                load_score(state, f)
                print(score2string(state["score"]))
                print(f + " loaded.")
            elif 'export' == string.split()[0]:
                with open(f, 'w') as fh:
                    fh.write(score2string(state["score"]))
                print("exported to " + f)
        except:
            print("ERR: can't access file or no file given")
    elif string == 'quit':
        exit()
    elif string == 'del':
        if len(state["score"]):
            state["score"].pop()
            print(score2string(state["score"]))
        else:
            print("ERR: score empty")
    elif string == '?' or string == 'help':
        print(usage)
    elif string == 'print':
        print(score2string(state["score"]))
    elif string == 'clear':
        state.clear()
        state["octave"] = '3'
        state["score"] = []
    elif string.startswith('set'):
        try:
            fmt[string.split()[1]] = string.split()[2]
            print("set fmt[" + string.split()[1] + "] = " + string.split()[2])
        except:
            print("ERR: set args are wrong. doing nothing")
    else:
        # assume a new tab was entered
        tokens = tokenise(string)
        update_tab_state(tokens, state)
        state["score"].append(state["tab"])
        # print the whole score
        print(score2string(state["score"]))


exit()
