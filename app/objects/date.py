from datetime import datetime
import calendar 

class Date: 
    def __init__(self, date:str):
        self._month = self.validate_month_input(date[:2])
        self._year = self.validate_year_input(date[2:])
    
    @staticmethod
    def validate_month_input(month: str)-> str:
        if month.isdigit() and 1<= int(month)<=12:
            return month
        raise ValueError('Month value is not valid', month)
    
    @staticmethod
    def validate_year_input(year: str)-> int:
        if year.isdigit() and 2000 <= int(year)<=datetime.now().year:
            return int(year)
        raise ValueError('Year value is not valid', year)
    
    @property
    def month_name(self)-> str: 
        return calendar.month_name[int(self._month)]
    
    @property
    def month_number(self)-> int: 
        return int(self._month)
    
    @property
    def year(self) -> int:
        return self._year 
