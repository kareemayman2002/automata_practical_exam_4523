from collections import deque, defaultdict

def epsilon_closure(nfa, states):

    closure = set(states)
    queue = deque(states)
    
    while queue:
        state = queue.popleft()
        for next_state in nfa.get((state, ''), []):
            if next_state not in closure:
                closure.add(next_state)
                queue.append(next_state)
    return frozenset(closure)

def nfa_to_dfa(nfa, start_state, accept_states, alphabet):

    alphabet = [a for a in alphabet if a != '']
    
    initial = epsilon_closure(nfa, {start_state})
    dfa = {}
    dfa_states = {}
    state_id = 0
    dfa_states[initial] = f"q{state_id}"
    state_id += 1
    
    unprocessed = deque([initial])
    
    while unprocessed:
        current = unprocessed.popleft()
        
        for symbol in alphabet:
            next_states = set()
            for nfa_state in current:
                for next_state in nfa.get((nfa_state, symbol), []):
                    next_states.add(next_state)
            
            if not next_states:
                continue
                
            next_closure = epsilon_closure(nfa, next_states)
            
            if next_closure not in dfa_states:
                dfa_states[next_closure] = f"q{state_id}"
                state_id += 1
                unprocessed.append(next_closure)
            
            if (dfa_states[current], symbol) not in dfa:
                dfa[(dfa_states[current], symbol)] = dfa_states[next_closure]
    
    dfa_accept = set()
    for state_set, state_name in dfa_states.items():
        if any(s in accept_states for s in state_set):
            dfa_accept.add(state_name)
    
    return dfa, dfa_states[initial], dfa_accept


nfa = {
    ('q0', 'a'): ['q0', 'q1'],
    ('q0', 'b'): ['q0', 'q3'],
    ('q0', ''): ['q7'],
    ('q1', 'a'): ['q2'],
    ('q3', 'b'): ['q4'],
    ('q7', ''): ['q5'],
    ('q5', 'a'): ['q6'],
    ('q6', 'a'): ['q2'],
    ('q5', 'b'): ['q8'],
    ('q8', 'b'): ['q4']
}
start = 'q0'
accept = {'q2', 'q4'}
alphabet = ['a', 'b', '']  
dfa, dfa_start, dfa_accept = nfa_to_dfa(nfa, start, accept, alphabet)

print("DFA Transitions:")
for (state, symbol), next_state in dfa.items():
    print(f"δ({state}, {symbol}) = {next_state}")

print("\nDFA Start State:", dfa_start)
print("DFA Accept States:", dfa_accept)