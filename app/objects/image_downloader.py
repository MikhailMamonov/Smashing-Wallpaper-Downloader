import re

class ImageDownloader:

    def __init__(self, resolution:str):
        self.resolution = self.__validate_input(resolution)
    
    @staticmethod
    def __validate_input(resolution: str) -> str:
        match = re.search('^\d{3,4}x\d{3,4}$', resolution)
        if match:
            return resolution
        raise ValueError('Resolution value is not valid', resolution)
    
    