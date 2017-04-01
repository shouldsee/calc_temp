def repack(oldrule):
    helper1 = [0]*2;

    for i in range(2):
        helper1[i] = [
            { "0": 0 },
            { "c": 0, "e": 0    },
            { "a": 0, "c": 0, "e": 0, "i": 0, "k": 0, "n": 0    },
            { "a": 0, "c": 0, "e": 0, "i": 0, "j": 0, "k": 0, "n": 0, "q": 0, "r": 0, "y": 0 },
            { "a": 0, "c": 0, "e": 0, "i": 0, "j": 0, "k": 0, "n": 0, "q": 0, "r": 0, "t": 0, "w": 0, "y": 0, "z": 0 },
            { "a": 0, "c": 0, "e": 0, "i": 0, "j": 0, "k": 0, "n": 0, "q": 0, "r": 0, "y": 0 },
            { "a": 0, "c": 0, "e": 0, "i": 0, "k": 0, "n": 0    },
            { "c": 0, "e": 0    },
            { "0": 0 }
        ]

    state = ''
    survive = 1
    direction = 1
    oldrule += '.'
    for char in oldrule:
        if char in '012345678./_Ss':
            if char != state:
                if state and state in '012345678' and 0 == max([i[1] for i in helper1[survive][int(state)].iteritems()]):
                    for j, k in helper1[survive][int(state)].iteritems():
                        helper1[survive][int(state)][j] = 1
                state = char
            if char in 'sS':
                survive = 1
            elif char in '/_':
                survive = 1 - survive
            direction = 1
        elif char.lower() in 'aceijknqrtwyz':
            helper1[survive][int(state)][char.lower()] = direction
        elif char == '-':
            direction = 0
            for i in helper1[survive][int(state)].iteritems():
                helper1[survive][int(state)][i[0]] = 1
        elif char.lower() =='b':
            survive = 0
            direction = 1

    newrule = "B"
    for base in range(2):
        for state in range(9):
            helper2 = [i[1] for i in helper1[base][state].iteritems()]
            if 1 == max(helper2):
                helper3 = ''
                if 0 == min(helper2):
                    if helper2.count(1)/(1.0*len(helper2))<=0.501:
                        helper3 = [j for j, k in helper1[base][state].iteritems() if ((k==1) and (j!='0'))]
                        helper3.sort()
                        helper3 = ''.join(helper3)
                    else:
                        helper3 = [j for j, k in helper1[base][state].iteritems() if ((k==0) and (j!='0'))]
                        helper3.sort()
                        helper3 = '-' + ''.join(helper3)
                newrule += str(state) + helper3
        if base == 0:
            newrule += '/S'
    return newrule
repack('b3ianjrecqyks2ac3i2e3a2k3nj2i3re2n3cqyk')