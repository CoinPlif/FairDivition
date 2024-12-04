import random

import numpy as np
from calc_static import calc_sum


class StandartScaler:
    def __init__(self):
        self.alpha = None

    def fit(self, a):
        self.alpha = np.sum(a)/100

    def transform(self, a):
        return a/self.alpha

    def reverse_transform(self, a):
        return a*self.alpha


class Item:
    def __init__(self, c1, c2, index):
        self.c1 = c1
        self.c2 = c2
        self.index = index
        self.part_1 = None
        self.part_2 = None


def ten2binary(x, power):
    s = ''
    for i in range(power):
        if x%2 == 0:
            s = '0' + s
        else:
            s = '1' + s
        x = x//2
    return s


def print_results(player_1, player_2, item_array, ss1, ss2, max_sum):
    print(f'Ценности предметов изначальные точечные для 1 человека', np.round(player_1, 3))
    print(f'Ценности предметов изначальные точечные для 2 человека', np.round(player_2, 3))

    print(f'Стандартизированная ценности каждого предмета для 1 человека: {np.round(ss1.transform(player_1), 3)}')
    print(f'Стандартизированная ценности каждого предмета для 2 человека: {np.round(ss2.transform(player_2), 3)}')

    print(f'Доли предметов, которые получит 1 игрок {[np.round(item_part.part_1, 3) for item_part in item_array]}')
    print(f'Доли предметов, которые получит 2 игрок {[np.round(item_part.part_2, 3) for item_part in item_array]}')

    print('Финальная ценность суммарная нестандартизованная', np.round(max_sum, 3))

    item_parts_1 = []
    item_parts_2 = []

    for item in item_array:
        item_parts_1.append(item.part_1)
        item_parts_2.append(item.part_2)

    final_sum_1 = np.sum(item_parts_1 * player_1)
    final_sum_2 = np.sum(item_parts_2 * player_2)

    print(f'Финальная ценность 1 человека стандартизованная {np.round(final_sum_1, 3)}')
    print(f'Финальная ценность 2 человека стандартизованная {np.round(final_sum_2, 3)}')


p1_l1, p1_r1 = map(int, input("Введите person1_l1 person1_r1:").split())
p1_l2, p1_r2 = map(int, input("Введите person1_l2 person1_r2:").split())
p1_l3, p1_r3 = map(int, input("Введите person1_l3 person1_r3:").split())

p2_l1, p2_r1 = map(int, input("Введите person2_l1 person2_r1:").split())
p2_l2, p2_r2 = map(int, input("Введите person2_l2 person2_r2:").split())
p2_l3, p2_r3 = map(int, input("Введите person2_l3 person2_r3:").split())

p1 = np.array([[p1_l1, p1_r1],
              [p1_l2, p1_r2],
              [p1_l3, p1_r3]])

p2 = np.array([[p2_l1, p2_r1],
              [p2_l2, p2_r2],
              [p2_l3, p2_r3]])

mean_p1 = np.mean(p1, axis=1)
mean_p2 = np.mean(p2, axis=1)

ss1 = StandartScaler()
ss2 = StandartScaler()

ss1.fit(mean_p1)
ss2.fit(mean_p2)

standardized_p1 = ss1.transform(mean_p1)
standardized_p2 = ss2.transform(mean_p2)

sum_p1, sum_p2, item_array = calc_sum(standardized_p1, standardized_p2)

player_1 = np.round(ss1.reverse_transform(standardized_p1), 3)
player_2 = np.round(ss2.reverse_transform(standardized_p2), 3)

print("Дележ с точечными оценками")

print_results(player_1, player_2, item_array, ss1, ss2, sum_p1)

best_player_1 = []
best_player_2 = []
best_item_array = []

max_sum = 0

standardized_p1 = ss1.transform(p1)
standardized_p2 = ss2.transform(p2)

n = len(p1)
for drop_1 in range(n):
    for drop_2 in range(n):
        for combination_1 in range(2**n):
            for combination_2 in range(2**n):
                comb_1 = ten2binary(combination_1, n)
                comb_2 = ten2binary(combination_2, n)
                player_1 = [0]*n
                player_2 = [0]*n
                for i in range(n):
                    if i != drop_1:
                        player_1[i] = standardized_p1[i][int(comb_1[i])]
                    if i != drop_2:
                        player_2[i] = standardized_p2[i][int(comb_2[i])]

                player_1 = np.array(player_1)
                player_2 = np.array(player_2)

                additional_1 = 100 - np.sum(player_1)
                additional_2 = 100 - np.sum(player_2)

                if standardized_p1[i][0] <= additional_1 <= standardized_p1[i][1] and standardized_p2[i][0] <= additional_2 <= standardized_p2[i][1]:
                    player_1[drop_1] = additional_1
                    player_2[drop_2] = additional_2
                    sum_p1, sum_p2, item_array = calc_sum(player_1, player_2)
                    if sum_p1 > max_sum:
                        max_sum = sum_p1
                        best_player_1 = player_1
                        best_player_2 = player_2
                        best_item_array = item_array


best_player_1 = ss1.reverse_transform(np.array(best_player_1))
best_player_2 = ss2.reverse_transform(np.array(best_player_2))

print('\n\n')
print("Дележ с интервальными оценками")

print_results(best_player_1, best_player_2, best_item_array, ss1, ss2, max_sum)

rand_res_final = []
rand_res_1 = []
rand_res_2 = []


for i in range(10000):
    rand_p1 = [0]*n
    rand_p2 = [0]*n

    for idx, boundary in enumerate(p1):
        l, r = float(boundary[0]), float(boundary[1])
        rand_p1[idx] = random.randrange(l*1000, r*1000)/1000

    for idx, boundary in enumerate(p2):
        l, r = float(boundary[0]), float(boundary[1])
        if l == r:
            rand_p2[idx] = l
        else:
            rand_p2[idx] = random.randrange(l*1000, r*1000)/1000

    # print(rand_p1)
    # print(rand_p2)

    ss3 = StandartScaler()
    ss4 = StandartScaler()

    ss3.fit(rand_p1)
    ss4.fit(rand_p2)

    rand_p1 = ss3.transform(rand_p1)
    rand_p2 = ss4.transform(rand_p2)

    sum_1, sum_2, item_array = calc_sum(np.array(rand_p1), np.array(rand_p2))

    rand_res_1.append(np.round(ss1.reverse_transform(sum_1), 3))
    rand_res_2.append(np.round(ss2.reverse_transform(sum_2), 3))
    rand_res_final.append(sum_1)


print('\n\n')
print(f'Случайная генерация точек на интервалах')
print(f'Средний результат по финальной полезности - {np.mean(np.array(rand_res_final))}')

max_val_index = rand_res_final.index(max(rand_res_final))

print(f'Средний результат по ценности 1 человека - {np.mean(np.array(rand_res_1))}')
print(f'Средний результат по ценности 2 человека - {np.mean(np.array(rand_res_2))}')
print(f'Max результат по финальной полезности - {rand_res_final[max_val_index]}')
print(f'Max результат по ценности 1 человека - {rand_res_1[max_val_index]}')
print(f'Max результат по ценности 2 человека - {rand_res_2[max_val_index]}')
