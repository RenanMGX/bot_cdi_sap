from sap import SAPManipulation
from indice import IndiceBacen
from datetime import datetime
from copy import deepcopy
from dateutil.relativedelta import relativedelta
from typing import List
from time import sleep

class OB83(SAPManipulation, IndiceBacen):
    def __init__(self, *, user: str, password: str, ambiente: str, date:datetime, cod_indice:int=4389) -> None:
        SAPManipulation.__init__(self, user=user, password=password, ambiente=ambiente)
        IndiceBacen.__init__(self, cod_indice=cod_indice)
        
        if not isinstance(date, datetime):
            raise TypeError(f"{date=} não é um 'datetime'")
        self.__date:datetime = date
    
    @property
    def date(self) -> datetime:
        return self.__date
    
    @SAPManipulation.usar_sap
    def execute(self, fechar_sap_no_final=False) -> None:
        self.session.findById("wnd[0]/tbar[0]/okcd").text = "/n ob83"
        self.session.findById("wnd[0]").sendVKey(0)

        ultima_data_STR:str = self.session.findById("wnd[0]/usr/tblSAPLFREFINTVTCTRL_V_T056P/txtV_T056P-DATAB[2,0]").text #coleta a ultima data lançada
        ultima_data = datetime.strptime(ultima_data_STR, '%d.%m.%Y')
        print(f"{ultima_data}")
        
        if ultima_data == self.date.strftime('%d.%m.%Y'):
            raise Exception("ultimo indice lançado é o atual")
        
        lista_datas_lancar:List[datetime] = self.separar_indices(ultima_data)
        
        if not lista_datas_lancar:
            raise Exception("não existe indices para lançamento!")
        
        self.session.findById("wnd[0]/tbar[1]/btn[5]").press()
        
        contador:int = 0
        for data in lista_datas_lancar:
            novo_indice_lancar:dict
            try:
                novo_indice_lancar = self.indice_p_data(data)
            except ValueError as error:
                novo_indice_lancar = {}
                print(type(error), error)
                continue
            if not novo_indice_lancar:
                print("'novo_indice_lancar' está vazio")
                continue

            self.session.findById(f"wnd[0]/usr/tblSAPLFREFINTVTCTRL_V_T056P/ctxtV_T056P-REFERENZ[0,{contador}]").text = "CDI"
            self.session.findById(f"wnd[0]/usr/tblSAPLFREFINTVTCTRL_V_T056P/txtV_T056P-DATAB[2,{contador}]").text = data.strftime('%d.%m.%Y')
            self.session.findById(f"wnd[0]/usr/tblSAPLFREFINTVTCTRL_V_T056P/txtV_T056P-ZSOLL[3,{contador}]").text = str(novo_indice_lancar['valor']).replace(".",",")
            
            contador += 1
            
        self.session.findById("wnd[0]/tbar[0]/btn[11]").press()

        if (infor_bar:=self.session.findById("wnd[0]/sbar").text) == 'Já existe uma entrada com a mesma chave':
            print(f"{infor_bar=}")

                
        sleep(5)
        
    def separar_indices(self, last_date:datetime) -> List[datetime]:
        last_date_temp:datetime = deepcopy(last_date)
        list_date:list = []
        while self.date > last_date_temp:
            last_date_temp += relativedelta(days=1)
            list_date.append(deepcopy(last_date_temp))
        
        return list_date

if __name__ == "__main__":
    pass
    # string_data:str = "27/03/2024"
    # data_temp:datetime = datetime.strptime(string_data, '%d/%m/%Y')
    
    # crd:dict = Credential("SAP_QAS").load()
    
    # bot:OB83 = OB83(user=crd['user'], password=crd['password'], ambiente="S4Q", date=datetime.now())
    
    # print(bot.execute(fechar_sap_no_final=True))
    
    # #bot.fechar_sap()
    # # bot.conectar_sap()
    
    