from util import console, parse_file_as_list, time_function, get_the_hood_8
import numpy as np
import re
from string import punctuation

test_file = parse_file_as_list('input/3_test.txt')
day_file = parse_file_as_list('input/3.txt')


@time_function()
def run_a(file):
    valid_engine_symbols = set(punctuation)
    valid_engine_symbols.remove('.')

    pattern = re.compile('([0-9])+')
    y_numbers_dict = {index: [match for match in pattern.finditer(line)] for index, line in enumerate(file)}

    engine = np.array([list(line) for line in file])
    the_hood = get_the_hood_8(engine)

    engine_part_numbers = []
    for y, number_matches in y_numbers_dict.items():
        # skip emtpy values
        if not number_matches:
            continue

        for match in number_matches:
            valid_number = check_engine_number(y, match, engine, valid_engine_symbols, the_hood)
            if valid_number:
                engine_part_numbers.append(valid_number)

    return sum(engine_part_numbers)


def check_engine_number(y, match, engine, valid_engine_symbols, the_hood):
    for x in range(match.span()[0], match.span()[1]):
        for coord_value in the_hood[y, x]:
            symbol = engine[coord_value]
            if symbol in valid_engine_symbols:
                return int(match.group(0))


@time_function()
def run_b(file):
    pass


if __name__ == '__main__':
    answer_a = run_a(day_file)
    answer_b = run_b(test_file)

    console.print(f'solution A: {answer_a}')
    console.print(f'solution B: {answer_b}')
