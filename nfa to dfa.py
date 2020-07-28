from states import State

file = open("NFA_Input_2.txt", "r")
output = open("DFA_Output_2.txt", "w+")

# reading the whole file into an arrey
lines = file.readlines()
file.close()

# An nfa is represented by a five tuple(Q, sigma, delta, q0, F)
# Q is the finit set of states
# sigma is the finit set of input symbols
# delta is the transition function
# q0 id the initial state
# F is the set of states, which are disinguished as accepting states

# gettin q0
first_state = lines[2].strip()

# getting F
finall_nfa_states = lines[3].strip().split(" ")

# gettin Q
Q = lines[1].strip().split(" ")

finall_dfa_stated = set()
nfa_states = {}
dfa_states = {}

for x in Q:
    # making the State objects according to Q
    nfa_states[x] = State(x)

    # speify the real states of the states in Q
    nfa_states[x].add_real_state(x)

for x in finall_nfa_states:
    # specify the states in nfa_states which are final
    nfa_states[x].set_final()

for i in range(len(lines[4:])):
    # getting the transitions and add them to the relevant state deltas
    splited = lines[i + 4].split()
    nfa_states[splited[0]].add_delta(splited[2], splited[1])

for x in nfa_states:
    # check if the following state has the transition char 't'
    if 't' in nfa_states[x].deltas:
        # if it has, it will add all the transitions of the states that are reachable from 't' to the following state
        for y in nfa_states[x].deltas['t']:
            for char in nfa_states[y].deltas.keys():
                for state in nfa_states[y].deltas[char]:
                    nfa_states[x].add_delta(state, char)
        # if one state can transform to a state which has got 't' transition char, it can also reach all the states reachable from 't'
        for y in nfa_states.keys():
            for char in nfa_states[y].deltas.keys():
                if nfa_states[x].name in nfa_states[y].deltas[char]:
                    for state in nfa_states[x].deltas['t']:
                        nfa_states[y].add_delta(state, char)

        # eleminata the 't' transition char from the following state thus we implemented all its impacts on the nfa_states
        nfa_states[x].deltas.pop('t')

# making the initial state of dfa_states and initialize it
first_dfa_state = State(first_state)
first_dfa_state.add_real_state(first_state)
dfa_states[first_state] = first_dfa_state
dfa_states_real_states = set()

# it will become true if we find new state in iterating the dfa_states destinations
has_new_dfa_state = True

# it will continue as long as we a reach a new state
while has_new_dfa_state:
    has_new_dfa_state = False

    # we make a copy of dfa_states and iterate on the, because we cant concurrently add new state and iterate the states
    # we iterate the copy one, and the new states to the original one
    dfa_states_copy = dfa_states.copy()

    # iterate the states in dfa_states
    for x in dfa_states_copy.keys():
        # for instance we reach x in the previous iteration, now it will iterate the real_states of x
        for y in dfa_states_copy[x].real_states:
            # it will iterate the transition chars of the specified real_state
            for char in nfa_states[y].deltas:
                # name of the new state, base on its real_states
                string_of_real_states = ""
                dfa_states_real_states.clear()

                # find all the destinations of the specified char, reached in the previous iteration from the whole real_states of x
                # and add them to a set to make the new state (by finding the real_states of the new state)
                for real_state in dfa_states_copy[x].real_states:
                    if char in nfa_states[real_state].deltas:
                        for state in nfa_states[real_state].deltas[char]:
                            dfa_states_real_states.add(state)

                # convert the mentioned set to a list so that we can sort the list
                list_of_real_states = list(dfa_states_real_states)
                list_of_real_states.sort(key=lambda item: ([str, int].index(type(item)), item))

                # join all the elements of the mentioned list to make a single string which is the name of new state
                string_of_real_states = ''.join(list_of_real_states)

                # check wheather we have the new state in dfa_states
                if string_of_real_states not in dfa_states.keys():
                    # we find a new state so the while should continue
                    has_new_dfa_state = True
                    # making the new state
                    new_state = State(string_of_real_states)

                    # specify the real_states of the new state
                    for z in list_of_real_states:
                        if z in nfa_states:
                            new_state.add_real_state(z)
                            if nfa_states[z].isFinal:
                                # if the new state has got one of the final states in its real_states, it should also become a final state
                                new_state.set_final()
                    # add the new state to dfa_states
                    dfa_states[string_of_real_states] = new_state

                # specify the dfa_states reachable from x
                dfa_states[x].add_delta(string_of_real_states, char)

# specify all the dfa_final states
for x in dfa_states:
    if dfa_states[x].isFinal:
        finall_dfa_stated.add(x)

# making the output pattern same as the input
output.writelines(lines[0])
output.writelines(s + " " for s in dfa_states)
output.writelines("\n")
output.writelines(lines[2])
output.writelines(s + " " for s in finall_dfa_stated)
for x in dfa_states:
    for char in dfa_states[x].deltas:
        for state in dfa_states[x].deltas[char]:
            output.writelines("\n" + x + " " + char + " " + state)

output.close()
