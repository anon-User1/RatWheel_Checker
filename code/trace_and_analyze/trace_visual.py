import matplotlib.pyplot as plt

def show_freq(patterns, freqs, trace_no):
#    plt.bar(range(len(freqs)), freqs, tick_label = patterns)
    plt.bar(range(len(freqs)), freqs)
    plt.title('trace pattern frequency: ' + trace_no)
    plt.xlabel('pattern_no')
    plt.ylabel('frequency')

    plt.ylim((0,150))

    plt.show()


#test
'''
patterns = ['1','2','3','4','5','6','7']
freqs = [1,1,2,4,5,20,145]
show_freq(patterns,freqs,'test')
'''