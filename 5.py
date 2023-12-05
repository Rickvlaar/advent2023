from util import console, parse_file_as_list, time_function
from itertools import starmap
import re

test_file = parse_file_as_list('input/5_test.txt')
day_file = parse_file_as_list('input/5.txt')


@time_function()
def run_a(file):
    seeds = [int(seed_no) for seed_no in file[0].split('seeds: ')[1].split(' ')]
    bal_dict = parse_file(file)
    locations = determine_locations(seeds, bal_dict)
    return min(locations)


@time_function()
def run_b(file):
    seed_range_pairs = [int(seed_no) for seed_no in file[0].split('seeds: ')[1].split(' ')]

    seed_ranges = [(seed_range_start, seed_range_start + range_len) for seed_range_start, range_len in zip(seed_range_pairs[::2], seed_range_pairs[1::2])]

    console.print(len(seed_ranges))
    console.print(seed_ranges)

    bal_dict = parse_file(file)
    console.print(bal_dict)

    # seeds = [num for this_range in seed_ranges for num in this_range]
    # only check ranges with values that will change:

    # locations = determine_locations(seeds, bal_dict)
    # return min(locations)


def parse_file(file: list[str]):
    pattern = '([a-z]*)-to-([a-z]*)'
    bal_dict = {}
    for index, line in enumerate(file):
        if 'map' in line:
            source_target = re.match(pattern, line).groups()
            bal_dict[source_target] = create_source_dest_map(file=file, start_index=index + 1)
        else:
            continue
    return bal_dict


def determine_locations(seeds: list[int], bal_dict: dict[tuple: list[list:int]]):
    # destination_start, source_start, range
    locations = []
    for seed_no in seeds:
        for ranges in bal_dict.values():
            for seed_range in ranges:
                source_range_start = seed_range[1]
                source_range_end = source_range_start + seed_range[2] - 1
                if source_range_start <= seed_no <= source_range_end:
                    diff = seed_no - source_range_start
                    destination_range_start = seed_range[0]
                    seed_no = destination_range_start + diff
                    break
        locations.append(seed_no)
    return locations


def create_source_dest_map(file: list[str], start_index: int):
    seed_nos = []
    for line in file[start_index:]:
        if line == '':
            return seed_nos
        seed_nos.append([int(seed_no) for seed_no in line.split(' ')])
    return seed_nos


if __name__ == '__main__':
    answer_a = run_a(day_file)
    answer_b = run_b(day_file)

    console.print(f'solution A: {answer_a}')
    console.print(f'solution B: {answer_b}')
