from util import console, parse_file_as_list, time_function
from itertools import cycle
import re

test_file = parse_file_as_list('input/8_test.txt')
day_file = parse_file_as_list('input/8.txt')


@time_function()
def run_a(file: list[str]):
    # convert LR to index 0 1
    instructions = cycle([0 if char == 'L' else 1 for char in file[0]])
    node_destination_dict = {match.group(1): (match.group(2), match.group(3)) for match in [re.match('([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)', line) for line in file[2:]]}

    location = 'AAA'
    steps = 0
    while location != 'ZZZ':
        steps += 1
        direction = next(instructions)
        location = node_destination_dict[location][direction]
    return steps


@time_function()
def run_b(file: list[str]):
    # convert LR to index 0 1
    instructions = cycle([0 if char == 'L' else 1 for char in file[0]])
    node_destination_dict = {match.group(1): (match.group(2), match.group(3)) for match in [re.match('([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)', line) for line in file[2:]]}

    starting_nodes = {node for node in node_destination_dict if node[2] == 'A'}
    end_nodes = {node for node in node_destination_dict if node[2] == 'Z'}

    console.print(starting_nodes)
    console.print(end_nodes)

    steps = 0
    while True:
        direction = next(instructions)
        steps += 1
        new_locations = set()
        for node in starting_nodes:
            location = node_destination_dict[node][direction]
            new_locations.add(location)
        if new_locations == end_nodes:
            break
        starting_nodes = new_locations

    return steps



if __name__ == '__main__':
    answer_a = run_a(day_file)
    answer_b = run_b(day_file)

    console.print(f'solution A: {answer_a}')
    console.print(f'solution B: {answer_b}')
