import argparse

def parse_args()-> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Дата и разрешение экрана")
    parser.add_argument('--resolution', type=str, required=True, help='Разрешение экрана' )
    parser.add_argument('--my', type=str, required=True, help='Месяц и год' )
    return parser.parse_args()