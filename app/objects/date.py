from datetime import datetime

class Date: 
    def __init__(self, date:str):
        self.month = self.__validate_month_input(date[:2])
        self.year = self.__validate_year_input(date[2:])
    
    @staticmethod
    def __validate_month_input(month: str)-> str:
        if month.isdigit() and 1<= int(month)<=12:
            return month
        raise ValueError('Month value is not valid', month)
    
    @staticmethod
    def __validate_year_input(year: str)-> str:
        if year.isdigit() and 2000 <= int(year)<=datetime.now().year:
            return year
        raise ValueError('Year value is not valid', year)
