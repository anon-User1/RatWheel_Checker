from symbol import Symbol
from rule import Rule
import re

class Pattern(object):
    def __init__(self):
        super(Pattern, self).__init__()
        self.no = 0
        self.rule = ""
        self.freq = 0

class Grammar(object):
    """docstring for Grammar"""
    def __init__(self):
        super(Grammar, self).__init__()
        self.digram_index = {}
        self.root_production = Rule(self)

    def train_string(self, string):
        """docstring for train_string"""
        input_sequence = [c for c in string]
        if (0 < len(input_sequence)):
            self.root_production.last().insert_after(Symbol.factory(self, input_sequence.pop(0)))
        while (0 < len(input_sequence)):
            self.root_production.last().insert_after(Symbol.factory(self, input_sequence.pop(0)))
            match = self.get_index(self.root_production.last().prev)
            if not match:
                self.add_index(self.root_production.last().prev)
            elif match.next != self.root_production.last().prev:
                self.root_production.last().prev.process_match(match)

    def add_index(self, digram):
        """docstring for index"""
        self.digram_index[digram.hash_value()] = digram

    def get_index(self, digram):
        """docstring for get"""
        return self.digram_index.get(digram.hash_value())

    def clear_index(self, digram):
        """docstring for clear_index"""
        if self.digram_index.get(digram.hash_value()) == digram:
            self.digram_index[digram.hash_value()] = None

    def print_grammar(self):
        """docstring for print_grammar"""
        output_array = []
        rule_set = [self.root_production]
    
        i = 0
        for rule in rule_set:
            output_array.append("%s --(%d)--> " % (i, rule.reference_count))
            line_length = rule.print_rule(rule_set, output_array, len("%s --(%d)--> " % (i, rule.reference_count)))
        
            if i > 0:
                output_array.append(' ' * (57 - line_length))
                line_length = rule.print_rule_expansion(rule_set, output_array, line_length)
            output_array.append('\n');
            i += 1
        return "".join(output_array)

    def get_rules(self):
        """docstring for get_rules"""
        num_re = '\(.*\)' 
        output_array = self.print_grammar()
        rules = output_array.split('\n')
        patterns = []
        for rule in rules:
            num = re.search(num_re, rule, re.M|re.I)
            if num:
                reference_count = num.group().replace('(','').replace(')','')
            reference_count = int(reference_count)
            if reference_count == 0:
                m_pattern = Pattern()
                rule = rule.split('>')
                m_pattern.rule = rule[-1]
                m_pattern.no = '0'
                m_pattern.freq = 0
                patterns.append(m_pattern)
            else:
                m_pattern = Pattern()
                rule = rule.split(' ')
                m_pattern.no = rule[0]
                m_pattern.rule = rule[-1]
                m_pattern.freq = reference_count
                patterns.append(m_pattern)
        return patterns

