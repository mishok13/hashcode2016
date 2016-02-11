#!/usr/bin/env python
# -*- coding: utf-8 -*-


import math
from collections import *
from itertools import *
import sys


Point = namedtuple("Point", field_names=['a', 'b'])


def distance(x, y):
    return int(math.ceil(math.sqrt((x.a - y.a)**2 + (x.b - y.b)**2)))


def nline(f):
    val = f.readline().strip()
    return val

def choose_drone(order_index, drone_positions, drone_turns, sim_deadline):
    index = order_index % len(drone_positions)
    if drone_turns[index] + 1200 < sim_deadline:
        return index
    else:
        for index in range(len(drone_positions)):
            if drone_turns[index] + 1200 < sim_deadline:
                return index
    return None

def main(f):
    rows, columns, drone_quantity, sim_deadline, drone_max_load = map(int, nline(f).split())
    nline(f)
    products = dict(enumerate(map(int, nline(f).split())))
    num_warehouses = int(nline(f))
    warehouses = defaultdict(dict)
    for index in range(num_warehouses):
        warehouses[index]['pos'] = Point(*map(int, nline(f).split()))
        warehouses[index]['products'] = list(map(int, nline(f).split()))
    num_orders = int(nline(f))
    orders = defaultdict(dict)
    for index in range(num_orders):
        orders[index]['pos'] = Point(*map(int, nline(f).split()))
        nline(f)
        orders[index]['products'] = list(sorted(map(int, nline(f).split())))
    retired_drones = set()
    drone_positions = {x: warehouses[0]['pos'] for x in range(drone_quantity)}
    drone_turns = {x: 0 for x in range(drone_quantity)}
    moves = []
    for order_index, order in orders.items():
        for order_product in order['products']:
            potential_warehouses = [i for i, w in warehouses.items() if w['products'][order_product]]
            w = min(potential_warehouses, key=lambda i: distance(order['pos'], warehouses[i]['pos']))
            drone = choose_drone(order_index, drone_positions, drone_turns, sim_deadline)
            if drone is None:
                break
            quantity = 1
            moves.append("{} L {} {} {}".format(drone, w, order_product, quantity))
            drone_turns[drone] += 1 + distance(drone_positions[drone], warehouses[w]['pos'])
            drone_positions[drone] = warehouses[w]['pos']
            warehouses[w]['products'][order_product] -= 1
            moves.append("{} D {} {} {}".format(drone, order_index, order_product, quantity))
            drone_turns[drone] += 1 + distance(drone_positions[drone], order['pos'])
            drone_positions[drone] = order['pos']
    print(len(moves))
    for move in moves:
        print(move)




if __name__ == '__main__':
    main(open(sys.argv[1]))
