from collections import defaultdict

class Grammar:
    def __init__(self):
        self.productions = defaultdict(list)
        self.start_symbol = None
    
    def add_production(self, lhs, rhs):
        """Add a production rule: lhs -> rhs"""
        self.productions[lhs].append(rhs)
        if not self.start_symbol:
            self.start_symbol = lhs
    
    def is_ambiguous(self, string):
        """Check if the string has more than one parse tree"""
        parse_trees = []
        
        def derive(symbol, remaining_string, derivation):
            if not remaining_string:
                if symbol == '':
                    parse_trees.append(derivation)
                return
            
            if symbol in self.productions:
                for production in self.productions[symbol]:
                    new_derivation = derivation + [(symbol, production)]
                    derive(production, remaining_string, new_derivation)
            elif symbol == remaining_string[0]:
                derive(remaining_string[1:], remaining_string[1:], derivation)
        
        derive(self.start_symbol, string, [])
        return len(parse_trees) > 1

# Example usage
grammar = Grammar()
grammar.add_production('S', 'a S b S')
grammar.add_production('S', 'b S a S')
grammar.add_production('S', '')

test_string = "a b a b"
if grammar.is_ambiguous(test_string):
    print(f"The grammar is ambiguous for string '{test_string}'")
else:
    print(f"The grammar is not ambiguous for string '{test_string}'")