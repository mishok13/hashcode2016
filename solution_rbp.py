#!/usr/bin/env python
# -*- coding: utf-8 -*-


import math
from collections import *
from itertools import *
import sys


Point = namedtuple("Point", field_names=['a', 'b'])


class Move:
    def __init__(self, load, deliver):
        self.load = load
        self.deliver = deliver

class Load:
    def __init__(self, drone, warehouse, warehouse_index, product_type, quantity):
        self.drone = drone
        self.warehouse = warehouse
        self.warehouse_index = warehouse_index
        self.product_type = product_type
        self.quantity = quantity

    def __str__(self):
        return "{} L {} {} {}".format(self.drone, self.warehouse, self.product_type, self.quantity)


class Deliver:
    def __init__(self, drone, order, order_index, product_type, quantity):
        self.drone = drone
        self.order = order
        self.order_index = order_index
        self.product_type = product_type
        self.quantity = quantity
    
    def __str__(self):
        return "{} D {} {} {}".format(self.drone, self.order, self.product_type, self.quantity)


def distance(x, y):
    return int(math.ceil(math.sqrt((x.a - y.a)**2 + (x.b - y.b)**2)))


def nline(f):
    val = f.readline().strip()
    return val

def choose_drone(order, order_index, drone_positions, drone_turns, sim_deadline, max_turns):
    index = max(drone_positions.keys(), key=lambda d: distance(order['pos'], drone_positions[d]))
    # index = order_index % len(drone_positions)
    if drone_turns[index] + 2 * max_turns < sim_deadline:
        return index
    else:
        for index in range(len(drone_positions)):
            if drone_turns[index] + 2 * max_turns < sim_deadline:
                return index
    return None

def main(f):
    rows, columns, drone_quantity, sim_deadline, drone_max_load = map(int, nline(f).split())
    max_turns = distance(Point(0, 0), Point(rows, columns)) + 1
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
        orders[index]['product_qty'] = defaultdict(int)
        for p in orders[index]['products']:
            orders[index]['product_qty'][p] += 1

    retired_drones = set()
    drone_positions = {x: warehouses[0]['pos'] for x in range(drone_quantity)}
    drone_turns = {x: 0 for x in range(drone_quantity)}
    moves = []
    for order_index, order in sorted(orders.items(), key=lambda o: len(o[1]['products'])):
        for order_product, qty in order['product_qty'].items():
            drone = choose_drone(order, order_index, drone_positions, drone_turns, sim_deadline, max_turns)
            potential_warehouses = [i for i, w in warehouses.items() if w['products'][order_product]]
            w = min(potential_warehouses, key=lambda i: distance(order['pos'], warehouses[i]['pos']))
            if drone is None:
                break
            max_qty = drone_max_load // products[order_product]
            qty_left = min(max_qty, qty)

            while qty_left > 0:
                potential_warehouses = [i for i, w in warehouses.items() if w['products'][order_product]]
                w = min(potential_warehouses,
                        key=lambda i: distance(drone_positions[drone], warehouses[i]['pos']) + \
                        distance(warehouses[i]['pos'], order['pos']))
                quantity = min(qty_left, warehouses[w]['products'][order_product])
                qty_left -= quantity

                moves.append(Move(
                    Load(drone, warehouses[w], w, order_product, quantity),
                    Deliver(drone, order, order_index, order_product, quantity)
                ))

                drone_turns[drone] += 1 + distance(drone_positions[drone], warehouses[w]['pos'])
                drone_positions[drone] = warehouses[w]['pos']
                warehouses[w]['products'][order_product] -= quantity
                drone_turns[drone] += 1 + distance(drone_positions[drone], order['pos'])
                drone_positions[drone] = order['pos']

    moves_per_order = defaultdict(list)
    for m in moves:
        moves_per_order[m.deliver.order_index].append(m)
    for i, move_list in moves_per_order.items():
        move_list.sort(key=lambda m: distance(m.deliver.order['pos'], m.load.warehouse['pos']))

    order_moves = []
    for m in moves:
        # Assign drones
        pass
            
    print(len(moves))
    for move in moves:
        print(move.load)
        print(move.deliver)




if __name__ == '__main__':
    main(open(sys.argv[1]))
