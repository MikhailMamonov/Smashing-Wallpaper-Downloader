from app.parser import parse_args
from constants.api import *
from app.objects.date import Date
from app.objects.image_downloader import ImageDownloader



def run_cli():
    args = parse_args()
    date = Date(args.my)
    downloader = ImageDownloader(args.resolution)
    print(date.month, date.year, downloader.resolution)


