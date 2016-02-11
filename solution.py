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
    for order_index, order in orders.items():
        print(2 * len(order['products']))
        for order_product in order['products']:
            w = next(i for i, w in warehouses.items() if w['products'][order_product])
            drone = 0
            quantity = 1
            print("{} L {} {} {}".format(drone, w, order_product, quantity))
            print("{} D {} {} {}".format(drone, order_index, order_product, quantity))
        break




if __name__ == '__main__':
    main(open(sys.argv[1]))
