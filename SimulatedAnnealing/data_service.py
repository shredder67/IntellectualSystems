import argparse

def get_parsed_args():
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('--path', '-p', type=str,
                        help='path to data-source file')

    arg_parser.add_argument('--ans', '-a', type=float,
                        help='optional answer, for result validation')

    args = arg_parser.parse_args()
    return args.path, args.ans

# Ленивая чтение данных по строкам данных
# (строка - состояние из множества решений)
def read_data_by_rows(file):
    with open(file) as f:
        n = int(f.readline())
        for i in range(n):
            row = []
            while len(row) < 100:
                row.append(list(map( lambda num: int(num), 
                            f.readline().split())))
            yield row
            


