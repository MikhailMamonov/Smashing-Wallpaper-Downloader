import argparse

def parse_args()-> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Дата и разрешение экрана")
    parser.add_argument('-r','--resolution', type=str, required=True, help='Разрешение экрана' )
    parser.add_argument('-m','--my', type=str, required=True, help='Месяц и год' )
    return parser.parse_args()