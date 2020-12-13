# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 09:22:51 2020

@author: Adam.Comelio
"""
"""
--- Day 7: Handy Haversacks ---
You land at the regional airport in time for your next flight. In fact, it looks like you'll even have time to grab some food: all flights are currently delayed due to issues in luggage processing.

Due to recent aviation regulations, many rules (your puzzle input) are being enforced about bags and their contents; bags must be color-coded and must contain specific quantities of other color-coded bags. Apparently, nobody responsible for these regulations considered how long they would take to enforce!

For example, consider the following rules:

light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
These rules specify the required contents for 9 bag types. In this example, every faded blue bag is empty, every vibrant plum bag contains 11 bags (5 faded blue and 6 dotted black), and so on.

You have a shiny gold bag. If you wanted to carry it in at least one other bag, how many different bag colors would be valid for the outermost bag? (In other words: how many colors can, eventually, contain at least one shiny gold bag?)

In the above rules, the following options would be available to you:

A bright white bag, which can hold your shiny gold bag directly.
A muted yellow bag, which can hold your shiny gold bag directly, plus some other bags.
A dark orange bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.
A light red bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.
So, in this example, the number of bag colors that can eventually contain at least one shiny gold bag is 4.

How many bag colors can eventually contain at least one shiny gold bag? (The list of rules is quite long; make sure you get all of it.)
"""

from utils import tokenise_input_file, time_me

rules = tokenise_input_file('Inputs/day7.txt')

def process_rule(rule):
    result = list()
    k, other = rule.split(' bags contain ')
    if other == 'no other bags.':
        return k, tuple()
    for part in other.split(', '):
        num, colour = part.split(' ', 1)
        num = int(num)
        for text in ('bags', 'bag', '.'):
            colour = colour.replace(text, '')
        colour = colour.strip()
        result.append((colour, num))
    return k, tuple(result)

def process_rules(rules):
    rules_dict = dict()
    for rule in rules:
        k, v = process_rule(rule)
        rules_dict[k] = v
    return rules_dict

@time_me
def part1_no_recursion(rules):
    import networkx
    g = networkx.DiGraph()
    for rule in rules:
        k, v = process_rule(rule)
        for dest, num in v:
            g.add_edge(k, dest, weight=num)
    return sum(networkx.has_path(g, n, 'shiny gold') for n in g if n != 'shiny gold')

@time_me
def part1(rules):
    def search_dict(val, goal):
        t = 0
        for colour, _ in rules_dict[val]:
            if colour == goal:
                t += 1
            t += search_dict(colour, goal)
        return t
    rules_dict = process_rules(rules)
    t = 0
    for k in rules_dict:
        r = search_dict(k, 'shiny gold')
        if r:
            t += 1
    return t

print('%s bags could eventually contain a shiny gold bag no recursion\n' % part1_no_recursion(rules))
print('%s bags could eventually contain a shiny gold bag with recursion\n' % part1(rules))
"""
--- Part Two ---
It's getting pretty expensive to fly these days - not because of ticket prices, but because of the ridiculous number of bags you need to buy!

Consider again your shiny gold bag and the rules from the above example:

faded blue bags contain 0 other bags.
dotted black bags contain 0 other bags.
vibrant plum bags contain 11 other bags: 5 faded blue bags and 6 dotted black bags.
dark olive bags contain 7 other bags: 3 faded blue bags and 4 dotted black bags.
So, a single shiny gold bag must contain 1 dark olive bag (and the 7 bags within it) plus 2 vibrant plum bags (and the 11 bags within each of those): 1 + 1*7 + 2 + 2*11 = 32 bags!

Of course, the actual rules have a small chance of going several levels deeper than this example; be sure to count all of the bags, even if the nesting becomes topologically impractical!

Here's another example:

shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.
In this example, a single shiny gold bag must contain 126 other bags.

How many individual bags are required inside your single shiny gold bag?
"""

@time_me
def part2(rules):
    def search_dict(rules_dict, val):
        t = 1
        for colour, num in rules_dict[val]:
            t += num * search_dict(rules_dict, colour)
        return t
    rules_dict = process_rules(rules)
    return search_dict(rules_dict, 'shiny gold') - 1

print('My shiny gold bag contains %s other bags' % part2(rules))
