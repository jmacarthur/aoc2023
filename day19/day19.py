#!/usr/bin/env python3

import re

default_rule_regex = re.compile("[A-Za-z]+$")
rule_regex = re.compile("([xmas])([<>])(\d+):([A-Za-z]+)$")

class Part():
    def __init__(self, fields):
        self.n = {}
        for f in fields:
            (cat, quant) = tuple(f.split("="))
            self.n[cat] = int(quant)
    def __str__(self):
        return ",".join([f"{cat}={quant}" for (cat, quant) in self.n.items()])
    def score(self):
        return sum(self.n.values())

class Rule():
    def __init__(self, rule_text=None):
        if rule_text:
            m = default_rule_regex.match(rule_text)
            if m:
                self.result = m.group(0)
                self.variable = None
                return
            m = rule_regex.match(rule_text)
            assert m
            self.variable = m.group(1)
            self.operator = m.group(2)
            self.threshold = int(m.group(3))
            self.result = m.group(4)
        else:
            self.variable = None
            self.operator = None
            self.threshold = None
            self.result = None
    def test(self, part):
        if self.variable is None:
            return self.result
        elif self.operator == '>' and part.n[self.variable]>self.threshold:
            return self.result
        elif self.operator == '<' and part.n[self.variable]<self.threshold:
            return self.result
        else:
            return None
    def __str__(self):
        if self.variable:
            return f"{self.variable}{self.operator}{self.threshold}: {self.result}"
        else:
            return self.result
    def __repr__(self):
        if self.variable:
            return f"{self.variable}{self.operator}{self.threshold}: {self.result}"
        else:
            return self.result
    def opposite(self):
        assert self.variable
        r = Rule()
        r.variable = self.variable
        if self.operator == '>':
            r.operator = '<'
            r.threshold = self.threshold+1
        elif self.operator == '<':
            r.operator = '>'
            r.threshold = self.threshold-1
        return r

parts = []
workflows = {}

with open("test19.txt") as f:
    for l in f.readlines():
        l = l.strip()
        if l.startswith("{"):
            fields = l.strip("{}").split(",")
            parts.append(Part(fields))
        elif l != "":
            name = l[:l.index("{")]
            rules_text = l[l.index("{")+1:l.index("}")]
            rules = rules_text.split(",")
            workflows[name] = [Rule(rule_text) for rule_text in rules]

total_score = 0
for p in parts:
    current_flow = "in"
    while True:
        rules = workflows[current_flow]
        for rule in rules:
            if rule.test(p):
                current_flow = rule.test(p)
                break
        else:
            print("Ran off end of rules without matching")
            assert False

        if current_flow == "A" or current_flow == "R":
            break

    print(p, current_flow)
    if current_flow=='A':
        total_score += p.score()

print(f"Part 1 total score: {total_score}")

results = {}
for flow in workflows.values():
    for rule in flow:
        if rule.result == 'R' or rule.result == 'A':
            continue
        assert rule.result not in results, f"{rule.result} exists as a destination twice"
        results[rule.result] = 1

# Create chains to 'accept':
accepted_rules = []

def trace_flows(flow_name, path_so_far):
    global accepted_rules
    rules = workflows[flow_name]
    for r in rules:
        if r.result == "R":
            return None
        elif r.result == "A":
            accepted_rules.append(path_so_far+[r])
        else:
            trace_flows(r.result, path_so_far+[r])
        if r.variable:
            path_so_far += [r.opposite()]


trace_flows("in", [])
print(accepted_rules)
total_combinations = 0
for a in accepted_rules:
    minimums = {}
    maximums = {}
    for i in ['x','m','a','s']:
        minimums[i] = 1
        maximums[i] = 4000
    for step in a:
        if step.variable:
            if step.operator == '<':
                maximums[step.variable] = min(maximums[step.variable], step.threshold-1)
            elif step.operator == '>':
                minimums[step.variable] = max(minimums[step.variable], step.threshold+1)

    print(a)
    combinations = 1
    for i in ['x','m','a','s']:
        print(f"{i}: min {minimums[i]} -> max {maximums[i]}")
        combinations *= (maximums[i]-minimums[i]+1)
    print(f"{combinations} combinations.")
    total_combinations += combinations

print(f"{total_combinations} total combinations")

