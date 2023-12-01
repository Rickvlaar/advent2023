from util import console, parse_file_as_list, time_function

test_file = parse_file_as_list('input/_test.txt')
day_file = parse_file_as_list('input/.txt')


@time_function()
def run_a(file):
    pass


@time_function()
def run_b(file):
    pass


if __name__ == '__main__':
    answer_a = run_a(test_file)
    answer_b = run_b(test_file)

    console.print(f'solution A: {answer_a}')
    console.print(f'solution B: {answer_b}')
