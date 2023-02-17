from grammar import Grammar
import os
import math
#import numpy as np
import trace_anal
import trace_visual

'''
def auto_norm(data):
	norm_data = []
	min_num = min(data)
	print (min_num)
	max_num = max(data)
	print (max_num)
	range = max_num-min_num
	for num in data:
		num = (num - min_num)/range
		num = round(num,2)
		norm_data.append(num)
	return norm_data
'''

def trace_visualization(trace, trace_no):
	g = Grammar()
	g.train_string(trace)
	patterns = g.get_rules()
	trace_patterns = []
	freqs = []
	for pattern in patterns:
		if len(pattern.rule) > 4 and pattern.freq > 0:
			trace_patterns.append(pattern.rule)
			freqs.append(pattern.freq)
#	norm_freqs = auto_norm(freqs)
	trace_visual.show_freq(trace_patterns, freqs, trace_no)


def case_anal(clean_trace_file_path):

	g = os.walk(clean_trace_file_path)

	for path,dir_list,file_list in g:
		for file in file_list:
			trace_file = open(os.path.join(path, file), 'r')

			simple_trace = trace_anal.simplify_trace(trace_file)
			trace_visualization(simple_trace, file)
			#trace_anal.trace_anal(simple_trace)


if __name__ == '__main__':
#    unittest.main()
	case_anal("path")