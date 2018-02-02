def list_range(l):
    return max(l) - min(l)  

# inefficient!
def closest_subseq(l, points):
    subseq = l[:points]
    min_range = list_range(subseq) 
    min_sub = subseq
    for i in range(len(l)):
        subseq = l[i:points+i]
        lr = list_range(subseq)
        if lr < min_range:
            min_range = lr
            min_sub = subseq
    return min_sub
