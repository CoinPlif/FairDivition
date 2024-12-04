import numpy as np

class Item:
    def __init__(self, c1, c2, index):
        self.c1 = c1
        self.c2 = c2
        self.index = index
        self.part_1 = None
        self.part_2 = None


def calc_sum(standardized_p1, standardized_p2):
    # print(f'{standardized_p1=}')
    # print(f'{standardized_p2=}')

    diff = standardized_p1/standardized_p2

    # print(f'{diff=}')

    sum_p1 = np.sum(standardized_p1[diff > 1])
    sum_p2 = np.sum(standardized_p2[diff < 1])

    # print(f'{sum_p1=}')
    # print(f'{sum_p2=}')

    item_array = []

    for i in range(diff.shape[0]):
        item_array.append(Item(standardized_p1[i], standardized_p2[i], i))

    if sum_p1 < sum_p2:
        items_2 = []
        for i in range(diff.shape[0]):
            if item_array[i].c1 < item_array[i].c2:
                item_array[i].part_1 = np.float64(0)
                item_array[i].part_2 = np.float64(1)
                items_2.append([item_array[i], item_array[i].c2/item_array[i].c1])
            else:
                item_array[i].part_2 = np.float64(0)
                item_array[i].part_1 = np.float64(1)
        items_2 = sorted(items_2, key=lambda x: x[1])

        idx = 0
        while sum_p1 != sum_p2:
            a = items_2[idx][0].c1
            b = items_2[idx][0].c2

            if a + sum_p1 < sum_p2 - b:
                item_array[items_2[idx][0].index].part_1 = np.float64(1)
                item_array[items_2[idx][0].index].part_2 = np.float64(0)
                sum_p1 += a
                sum_p2 -= b
                idx += 1
            else:
                part_2 = (sum_p1-sum_p2)/(a+b)+1
                part_1 = 1 - part_2
                sum_p1 = sum_p1 + part_1*a
                sum_p2 = sum_p2 - b + part_2*b

                item_array[items_2[idx][0].index].part_1 = part_1
                item_array[items_2[idx][0].index].part_2 = part_2
                break
    else:
        items_1 = []
        for i in range(diff.shape[0]):
            if item_array[i].c1 < item_array[i].c2:
                item_array[i].part_1 = 0
                item_array[i].part_2 = 1
            else:
                item_array[i].part_2 = 0
                item_array[i].part_1 = 1
                items_1.append([item_array[i], item_array[i].c1 / item_array[i].c2])
        items_1 = sorted(items_1, key=lambda x: x[1])

        idx = 0
        while sum_p1 != sum_p2:
            a = items_1[idx][0].c1
            b = items_1[idx][0].c2

            if sum_p1 - a > sum_p2 + b:
                item_array[items_1[idx][0].index].part_1 = 0
                item_array[items_1[idx][0].index].part_2 = 1
                sum_p1 -= a
                sum_p2 += b
                idx += 1
            else:
                part_1 = (sum_p2 - sum_p1) / (a + b) + 1
                part_2 = 1 - part_1
                sum_p1 = sum_p1 - a + part_1 * a
                sum_p2 = sum_p2 + part_2 * b

                item_array[items_1[idx][0].index].part_1 = part_1
                item_array[items_1[idx][0].index].part_2 = part_2
                break



    # print(sum_p1, sum_p2)

    return sum_p1, sum_p2, item_array