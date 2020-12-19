# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 10:24:01 2020

@author: adamc
"""
"""
--- Day 17: Conway Cubes ---

As your flight slowly drifts through the sky, the Elves at the Mythical Information Bureau at the North Pole contact you. They'd like some help debugging a malfunctioning experimental energy source aboard one of their super-secret imaging satellites.

The experimental energy source is based on cutting-edge technology: a set of Conway Cubes contained in a pocket dimension! When you hear it's having problems, you can't help but agree to take a look.

The pocket dimension contains an infinite 3-dimensional grid. At every integer 3-dimensional coordinate (x,y,z), there exists a single cube which is either active or inactive.

In the initial state of the pocket dimension, almost all cubes start inactive. The only exception to this is a small flat region of cubes (your puzzle input); the cubes in this region start in the specified active (#) or inactive (.) state.

The energy source then proceeds to boot up by executing six cycles.

Each cube only ever considers its neighbors: any of the 26 other cubes where any of their coordinates differ by at most 1. For example, given the cube at x=1,y=2,z=3, its neighbors include the cube at x=2,y=2,z=2, the cube at x=0,y=2,z=3, and so on.

During a cycle, all cubes simultaneously change their state according to the following rules:

    If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active. Otherwise, the cube becomes inactive.
    If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active. Otherwise, the cube remains inactive.

The engineers responsible for this experimental energy source would like you to simulate the pocket dimension and determine what the configuration of cubes should be at the end of the six-cycle boot process.

For example, consider the following initial state:

.#.
..#
###

Even though the pocket dimension is 3-dimensional, this initial state represents a small 2-dimensional slice of it. (In particular, this initial state defines a 3x3x1 region of the 3-dimensional space.)

Simulating a few cycles from this initial state produces the following configurations, where the result of each cycle is shown layer-by-layer at each given z coordinate (and the frame of view follows the active cells in each cycle):

Before any cycles:

z=0
.#.
..#
###


After 1 cycle:

z=-1
#..
..#
.#.

z=0
#.#
.##
.#.

z=1
#..
..#
.#.


After 2 cycles:

z=-2
.....
.....
..#..
.....
.....

z=-1
..#..
.#..#
....#
.#...
.....

z=0
##...
##...
#....
....#
.###.

z=1
..#..
.#..#
....#
.#...
.....

z=2
.....
.....
..#..
.....
.....


After 3 cycles:

z=-2
.......
.......
..##...
..###..
.......
.......
.......

z=-1
..#....
...#...
#......
.....##
.#...#.
..#.#..
...#...

z=0
...#...
.......
#......
.......
.....##
.##.#..
...#...

z=1
..#....
...#...
#......
.....##
.#...#.
..#.#..
...#...

z=2
.......
.......
..##...
..###..
.......
.......
.......

After the full six-cycle boot process completes, 112 cubes are left in the active state.

Starting with your given initial configuration, simulate six cycles. How many cubes are left in the active state after the sixth cycle?
"""

from utils import time_me, tokenise_input_file
from itertools import product

test_lines = '''.#.
..#
###'''.split('\n')

lines = tokenise_input_file('Inputs/day17.txt')

initial_grid_3d = dict()
initial_grid_4d = dict()
for j, line in enumerate(lines):
    for i, c in enumerate(line):
        if c == '#':
            initial_grid_3d[(i,j,0)] = c
            initial_grid_4d[(i,j,0,0)] = c

def simulate_grid(grid, turns, rules):
    difs = (-1,0,1)
    for _ in range(turns):
        tmp_grid = grid.copy()
        del_cells = list()
        for loc, state in grid.items():
            ranges = tuple(tuple(map(lambda x: x + v, difs)) for v in loc)
            check_cells = product(*ranges)
            seen_life = 0
            for check_cell in check_cells:
                if check_cell == loc:
                    continue
                if check_cell in grid:
                    seen_life += 1
                else:
                    tmp_grid[check_cell] = '.'
            #print(loc, state, seen_life)
            if seen_life not in rules['Remain Active']:
                del_cells.append(loc)
        for loc in tmp_grid:
            if tmp_grid[loc] == '#':
                continue
            ranges = tuple(tuple(map(lambda x: x + v, difs)) for v in loc)
            check_cells = product(*ranges)
            seen_life = 0
            for check_cell in check_cells:
                if check_cell == loc:
                    continue
                if check_cell in grid:
                    seen_life += 1
            if seen_life in rules['Become Active']:
                tmp_grid[loc] = '#'
            else:
                del_cells.append(loc)
        for cell in del_cells:
            del tmp_grid[cell]
        grid = tmp_grid
    return grid

@time_me
def part1(p1_grid):
    p1_rules = {'Remain Active': (2,3),
                'Become Active': (3,)}
    new_grid = simulate_grid(p1_grid, 6, p1_rules)
    return new_grid, sum(v=='#' for v in new_grid.values())

grid, ans = part1(initial_grid_3d.copy())

def print_grid(grid):
    coords = tuple(grid.keys())
    dims = len(next(iter(grid.keys())))
    xmax = max([v[0] for v in coords])
    xmin = min([v[0] for v in coords])
    ymax = max([v[1] for v in coords])
    ymin = min([v[1] for v in coords])
    coord_other_dims = [v[2:] for v in coords]
    maxes = [max([v[i] for v in coord_other_dims]) for i in range(dims-2)]
    mins = [min([v[i] for v in coord_other_dims]) for i in range(dims-2)]
    other_dims_combs = product(*tuple(tuple(range(mins[i], maxes[i]+1)) for i in range(dims-2)))
    for others in other_dims_combs:
        dims_line = ''
        for dim_num, d in enumerate(others):
            dims_line += ', Dimension %s: ' % (dim_num+3)
            dims_line += str(d)
        print(dims_line[2:])
        for y in range(ymin, ymax+1):
            outline = str(y) + ' '
            for x in range(xmin, xmax+1):
                loc = tuple([x, y, *others])
                if loc in grid:
                    outline += grid[loc]
                else:
                    outline += '.'
            print(outline)
        print()

print(ans)

"""
--- Part Two ---

For some reason, your simulated results don't match what the experimental energy source engineers expected. Apparently, the pocket dimension actually has four spatial dimensions, not three.

The pocket dimension contains an infinite 4-dimensional grid. At every integer 4-dimensional coordinate (x,y,z,w), there exists a single cube (really, a hypercube) which is still either active or inactive.

Each cube only ever considers its neighbors: any of the 80 other cubes where any of their coordinates differ by at most 1. For example, given the cube at x=1,y=2,z=3,w=4, its neighbors include the cube at x=2,y=2,z=3,w=3, the cube at x=0,y=2,z=3,w=4, and so on.

The initial state of the pocket dimension still consists of a small flat region of cubes. Furthermore, the same rules for cycle updating still apply: during each cycle, consider the number of active neighbors of each cube.

For example, consider the same initial state as in the example above. Even though the pocket dimension is 4-dimensional, this initial state represents a small 2-dimensional slice of it. (In particular, this initial state defines a 3x3x1x1 region of the 4-dimensional space.)

Simulating a few cycles from this initial state produces the following configurations, where the result of each cycle is shown layer-by-layer at each given z and w coordinate:

Before any cycles:

z=0, w=0
.#.
..#
###


After 1 cycle:

z=-1, w=-1
#..
..#
.#.

z=0, w=-1
#..
..#
.#.

z=1, w=-1
#..
..#
.#.

z=-1, w=0
#..
..#
.#.

z=0, w=0
#.#
.##
.#.

z=1, w=0
#..
..#
.#.

z=-1, w=1
#..
..#
.#.

z=0, w=1
#..
..#
.#.

z=1, w=1
#..
..#
.#.


After 2 cycles:

z=-2, w=-2
.....
.....
..#..
.....
.....

z=-1, w=-2
.....
.....
.....
.....
.....

z=0, w=-2
###..
##.##
#...#
.#..#
.###.

z=1, w=-2
.....
.....
.....
.....
.....

z=2, w=-2
.....
.....
..#..
.....
.....

z=-2, w=-1
.....
.....
.....
.....
.....

z=-1, w=-1
.....
.....
.....
.....
.....

z=0, w=-1
.....
.....
.....
.....
.....

z=1, w=-1
.....
.....
.....
.....
.....

z=2, w=-1
.....
.....
.....
.....
.....

z=-2, w=0
###..
##.##
#...#
.#..#
.###.

z=-1, w=0
.....
.....
.....
.....
.....

z=0, w=0
.....
.....
.....
.....
.....

z=1, w=0
.....
.....
.....
.....
.....

z=2, w=0
###..
##.##
#...#
.#..#
.###.

z=-2, w=1
.....
.....
.....
.....
.....

z=-1, w=1
.....
.....
.....
.....
.....

z=0, w=1
.....
.....
.....
.....
.....

z=1, w=1
.....
.....
.....
.....
.....

z=2, w=1
.....
.....
.....
.....
.....

z=-2, w=2
.....
.....
..#..
.....
.....

z=-1, w=2
.....
.....
.....
.....
.....

z=0, w=2
###..
##.##
#...#
.#..#
.###.

z=1, w=2
.....
.....
.....
.....
.....

z=2, w=2
.....
.....
..#..
.....
.....

After the full six-cycle boot process completes, 848 cubes are left in the active state.

Starting with your given initial configuration, simulate six cycles in a 4-dimensional space. How many cubes are left in the active state after the sixth cycle?
"""

@time_me
def part2(p1_grid):
    p2_rules = {'Remain Active': (2,3),
                'Become Active': (3,)}
    new_grid = simulate_grid(p1_grid, 6, p2_rules)
    return new_grid, sum(v=='#' for v in new_grid.values())

grid, ans = part2(initial_grid_4d.copy())

print(ans)
