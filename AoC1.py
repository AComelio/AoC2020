# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 09:14:26 2020

@author: Adam.Comelio
"""

'''
--- Day 1: Report Repair ---
After saving Christmas five years in a row, you've decided to take a vacation at a nice resort on a tropical island. Surely, Christmas will go on without you.

The tropical island has its own currency and is entirely cash-only. The gold coins used there have a little picture of a starfish; the locals just call them stars. None of the currency exchanges seem to have heard of them, but somehow, you'll need to find fifty of these coins by the time you arrive so you can pay the deposit on your room.

To save your vacation, you need to get all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

Before you leave, the Elves in accounting just need you to fix your expense report (your puzzle input); apparently, something isn't quite adding up.

Specifically, they need you to find the two entries that sum to 2020 and then multiply those two numbers together.

For example, suppose your expense report contained the following:

1721
979
366
299
675
1456
In this list, the two entries that sum to 2020 are 1721 and 299. Multiplying them together produces 1721 * 299 = 514579, so the correct answer is 514579.

Of course, your expense report is much larger. Find the two entries that sum to 2020; what do you get if you multiply them together?
'''

from itertools import combinations
from functools import reduce
import time

with open('Inputs/day1.txt', 'r') as f:
    expenses = tuple(map(int, f.read().split('\n')))

st = time.process_time_ns()

def prod_from_sum_target(num_list, comb_size, target):
    for comb in combinations(num_list, comb_size):
        if sum(comb) == target:
            return comb, reduce(lambda x, y: x*y, comb)

print('Part 1 solution: {}'.format(prod_from_sum_target(expenses, 2, 2020)))
print('Part 1 done in {} nanoseconds'.format((time.process_time_ns()-st)))
st = time.process_time_ns()

'''
--- Part Two ---
The Elves in accounting are thankful for your help; one of them even offers you a starfish coin they had left over from a past vacation. They offer you a second one if you can find three numbers in your expense report that meet the same criteria.

Using the above example again, the three entries that sum to 2020 are 979, 366, and 675. Multiplying them together produces the answer, 241861950.

In your expense report, what is the product of the three entries that sum to 2020?
'''

print('Part 2 solution: {}'.format(prod_from_sum_target(expenses, 3, 2020)))

print('Part 2 done in {} seconds'.format((time.process_time_ns()-st)/1000000000))