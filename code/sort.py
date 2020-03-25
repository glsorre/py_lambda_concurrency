from copy import copy

def selection_sort(l):
    l = copy(l)
    sorted_l = []
    while len(l) > 0:
        smaller = 2147483647
        for n in l:
            if n < smaller:
                smaller = n
        sorted_l.append(smaller)
        l.remove(smaller)
    return sorted_l

def quick_sort(l):
    if len(l) < 2:
        return l
    else:
        pivot = l[0]
        bigger = [n for n in l[1:] if n >= pivot]
        smaller = [n for n in l[1:] if n < pivot]
        return [*quick_sort(smaller), pivot, *quick_sort(bigger)]
