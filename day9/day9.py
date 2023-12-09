#!/usr/bin/env python3

with open("input9.txt") as f:
    initial_sequences = [list(map(int, l.strip().split())) for l in f.readlines()]


def differences(sequence):
    return [sequence[i] - sequence[i-1] for i in range(1,len(sequence))]

def all_equal(sequence):
    return all([x==sequence[0] for x in sequence])

# Basic tests
print(initial_sequences[0])
print(all_equal(initial_sequences[0]))
print(differences(initial_sequences[0]))
print(all_equal(differences(initial_sequences[0])))

forward_total = 0
backward_total = 0

for seq in initial_sequences:
    sequences = [seq]
    while not all_equal(sequences[-1]):
        sequences.append(differences(sequences[-1]))
    print(seq, sequences)

    # Now we can extrapolate the next values.
    sequences[-1].append(sequences[-1][-1])
    for seq_index in reversed(range(0, len(sequences)-1)):
        sequences[seq_index].append(sequences[seq_index][-1] + sequences[seq_index+1][-1])

    forward_total += sequences[0][-1]

    # Now extrapolate backwards.
    sequences[-1].insert(0, sequences[-1][0])
    for seq_index in reversed(range(0, len(sequences)-1)):
        sequences[seq_index].insert(0, sequences[seq_index][0] - sequences[seq_index+1][0])

    backward_total += sequences[0][0]

    print(seq, sequences)

print(f"Total for part 1: {forward_total}")
print(f"Total for part 2: {backward_total}")
