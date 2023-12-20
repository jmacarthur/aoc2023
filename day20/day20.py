#!/usr/bin/env python3

import sys

class FlipFlop():
    def __init__(self, name, outputs):
        self.name = name
        self.state = False
        self.outputs = outputs
    def update_input(self, inputname, value):
        if value == True:
            return []
        else:
            self.state = not self.state
            return [(self.name, self.state, output) for output in self.outputs]

class Combinator():
    def __init__(self, name, outputs):
        self.name = name
        self.inputsignals = {}
        self.outputs = outputs
    def update_input(self, inputname, value):
        self.inputsignals[inputname] = value
        outputval = not all(self.inputsignals.values())
        return [(self.name, outputval, output) for output in self.outputs]

class Broadcaster():
    def __init__(self, name, outputs):
        self.name = name
        self.outputs = outputs
    def update_input(self, inputname, value):
        return [(self.name, value, out) for out in self.outputs]

devices = {}
with open("input20.txt") as f:
    for line in [l.strip() for l in f.readlines()]:
        fields = line.split(" -> ")
        name = fields[0]
        outputs = fields[1].split(", ")
        if name.startswith("%"):
            devices[name[1:]] = FlipFlop(name[1:],outputs)
        elif name.startswith("&"):
            devices[name[1:]] = Combinator(name[1:], outputs)
        elif name == "broadcaster":
            devices[name] = Broadcaster(name, outputs)

# Proceed through everything that outputs to a combinator and initialise its inputs low
for (devicename, device) in devices.items():
    for output in device.outputs:
        if output in devices:
            if isinstance(devices[output], Combinator):
                devices[output].inputsignals[devicename] = False

button_presses = 100000000
high_pulses = 0
low_pulses = 0
for i in range(0,button_presses):
    pulse_chain = [('button', False, 'broadcaster')]
    while pulse_chain:
        (inputname, value, target) = pulse_chain.pop(0)
        if value:
            high_pulses += 1
        else:
            low_pulses += 1
        if target in devices:
            new_pulses = devices[target].update_input(inputname, value)
            if target == "dr" and value:
                print(i, devices[target].inputsignals.values())

            pulse_chain.extend(new_pulses)
        elif target == "rx" and value==False:
            print(f"rx pressed on button {i+1}")
            sys.exit(0)

print(f"Total pulses: {low_pulses} + {high_pulses}")
print(f"Product: {low_pulses*high_pulses}")
