import argparse

def get_parsed_args():
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('--path', '-p', type=str,
                        help='path to data-source file', default='./data/assign100.txt')

    arg_parser.add_argument('--ans', '-a', type=float,
                        help='optional answer, for result validation',
                        default=305)

    args = arg_parser.parse_args()
    return args.path, args.ans

# Ленивая чтение данных по строкам данных
# (строка - состояние из множества решений)
def read_data_by_rows(file):
    with open(file) as f:
        numbers = f.read().strip().split(' ')
        n = int(numbers[0])
        i = 1
        while i < len(numbers):
            j = 0
            row = []
            while j < n:
                row.append(int(numbers[i]))
                j += 1
                i += 1
            yield row
            


