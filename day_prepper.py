import requests
import os


COOKIES = {
        'session': os.environ['SESSION_KEY']
}


def get_input_and_write_to_file(day: int):
    puzzle_input_url = f'https://adventofcode.com/2023/day/{day}/input'
    input_response = requests.get(puzzle_input_url, cookies=COOKIES)

    puzzle_input_file = open(file=f'input/{day}.txt', mode='w')
    puzzle_input_file.write(input_response.text)
    puzzle_input_file.close()

    puzzle_test_input_file = open(file=f'input/{day}_test.txt', mode='x')
    puzzle_test_input_file.write('')
    puzzle_test_input_file.close()


def prepare_python_file(day: int):
    template_file = open(file=f'template.py', mode='r')
    filled_template_file = template_file.read().replace('{day_no}', str(day))
    day_file = open(file=f'{day}.py', mode='x')
    day_file.write(filled_template_file)
    day_file.close()


if __name__ == '__main__':
    day_number = 7
    get_input_and_write_to_file(day_number)
    prepare_python_file(day_number)
