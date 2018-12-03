import itertools


def _tuples_almost_equal(t1, t2, delta, places):
    for i in range(places):
        if abs(t1[i] - t2[i]) > delta:
            return False
    return True


def lists_almost_equal(list1, list2, delta, places=None):
    if len(list1) == 0 and len(list2) == 0:
        return True
    if len(list1[0]) != len(list2[0]) and places is None:
        return False
    if len(list1) != len(list2):
        return False
    places = places if places is not None else len(list1[0])
    for p in itertools.permutations(list2):
        for i, elem in enumerate(p):
            if not _tuples_almost_equal(list1[i], elem, delta, places):
                break
        else:
            return True
    return False


def list_contains_almost_equal(elem, elems_list, delta):
    for item in elems_list:
        if (item[0] - elem[0]) ** 2 + (item[1] - elem[1]) ** 2 < delta ** 2:
            return True
    return False


def list_difference(l1, l2):
    return list(set([tuple(l) for l in l1]) - set([tuple(l) for l in l2]))

