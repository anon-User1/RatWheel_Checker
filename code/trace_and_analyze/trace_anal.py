from grammar import Grammar
import re
import difflib

def param_similarity(p1, p2):
    return difflib.SequenceMatcher(None, p1, p2).quick_ratio()

def param_compare(trace_file_clean, first_pos, last_pos , pattern_len):
    """compare whether the params in pattern are the same"""
    param_set = []
    param = ''
    pos_count = -1
    file = open(trace_file_clean, 'r')
    line_no = 0
    start_flag = 0
    cmp_ans = 1
    for line in file:
        if line_no == first_pos:
            pos_count = 0
            param = ''
            start_flag = 1
        if pos_count == pattern_len:
            start_flag = 2
            pos_count = 0
        if line_no == last_pos:
            break
        if start_flag == 1:
            tmp = line.split(' ')
            tmp = tmp[1].strip()
            param_set.append(tmp)
            pos_count = pos_count + 1
        if start_flag == 2:
            tmp = line.split(' ')
            tmp = tmp[1].strip()
            if tmp != param_set[pos_count]:
                cmp_ans = 0
                break
            pos_count = pos_count + 1
        line_no = line_no + 1
    return cmp_ans


def find_pattern_pos(trace_str, pattern):
    return [substr.start() for substr in re.finditer(pattern, trace_str)]

def get_freq_pattern(patterns):
    """get 3 most frequent pattern"""
    #TODO: get 3 instead of 1
    max_num = 0
    freq_pattern_no = ' '
    for pattern in patterns:
        if pattern.freq > 10:
            if pattern.freq > max_num:
                max_num = pattern.freq
                freq_pattern_no = pattern.no
    return freq_pattern_no

def get_pattern_num(patterns):
    """get total number of patterns in trace"""
    first_pattern = patterns[0]
    pattern_num = first_pattern.rule.strip().split(' ')
    pattern_num = pattern_num[-1]
    return pattern_num

#make clean trace file into a string
def simplify_trace(trace_file):
    trace = ''
    for line in trace_file:
        trace = trace + line[0]
        line = line.split('$')
        if 'write' in line or 'read' or 'open' in line:
            variable = line[1]
            trace = trace + variable[0]
        if 'clone' in line:
            variable = line[-1].strip()
            trace = trace + variable[0]
    return trace

def trace_anal(trace):
    g = Grammar()
    g.train_string(trace)
    print (g.print_grammar())
    patterns = g.get_rules()
    freq_pattern_no = get_freq_pattern(patterns)
    for pattern in patterns:
        if pattern.no == freq_pattern_no:
            print (pattern.rule)
            print (pattern.freq)
    pattern_num = get_pattern_num(patterns)
#    print (pattern_num)

