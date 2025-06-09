import os
import requests
from datetime import datetime
from copy import deepcopy
from dateutil.relativedelta import relativedelta
from botcity.maestro import * #type: ignore

class IndiceBacen:
    def __init__(self, *, maestro:BotMaestroSDK, cod_indice:str|int, date: datetime=datetime.now(), months:int=6) -> None:
        dataInicial = (date - relativedelta(months=months)).strftime('%d/%m/%Y')
        dataFinal = date.strftime('%d/%m/%Y')
        self.__indices:list = requests.get(f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{cod_indice}/dados?formato=json&dataInicial={dataInicial}&dataFinal={dataFinal}").json()
        
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
    maestro = BotMaestroSDK.from_sys_args()
    execution = maestro.get_execution()
    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")
    
    date = datetime.strptime("12/03/2025", "%d/%m/%Y")
    bot = IndiceBacen(maestro=maestro, cod_indice=4389)
    
    
    #print(bot.indices)
    print(bot.indice_p_data(date))
    