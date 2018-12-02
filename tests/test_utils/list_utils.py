import itertools


def lists_almost_equal(list1, list2, delta):
    if len(list1) != len(list2):
        return False
    for p in itertools.permutations(list2):
        for i, elem in enumerate(p):
            if (list1[i][0] - elem[0]) ** 2 + (list1[i][1] - elem[1]) ** 2 > delta ** 2:
                break
        else:
            return True
    return False


def list_contains_almost(elem, elems_list, delta):
    for item in elems_list:
        if (item[0] - elem[0]) ** 2 + (item[1] - elem[1]) ** 2 < delta ** 2:
            return True
    return False
