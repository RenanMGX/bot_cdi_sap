import os
import requests
from datetime import datetime
from copy import deepcopy

class IndiceBacen:
    def __init__(self, *, cod_indice:str|int) -> None:
        self.__indices:list = requests.get(f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{cod_indice}/dados?formato=json").json()
        
    @property
    def indices(self):
        return deepcopy(self.__indices)
    
    def indice_p_data(self, date:datetime) -> dict:
        if not isinstance(date, datetime):
            raise TypeError("aceito apenas Datetime")
        
        dateSTR:str = date.strftime("%d/%m/%Y")
        indice:list = [indice for indice in self.indices if indice['data'] == dateSTR]
        #indice = deepcopy(indice)
        if len(indice) > 0:
            return indice[0]
        else:
            raise ValueError(f"não existe indice para esta data {dateSTR}")

if __name__ == "__main__":
    date = datetime.strptime("09/04/2024", "%d/%m/%Y")
    bot = IndiceBacen(cod_indice=4389)
    
    print(bot.indices)
    