from datetime import datetime
from Entities.ob83 import OB83
from Entities.dependencies.credenciais import Credential
import os
from Entities.dependencies.logs import Logs, traceback
from Entities.dependencies.config import Config

if __name__ == "__main__":
    try:
        crd:dict = Credential(Config()['credential']['crd']).load()
    
        date = datetime.now()
    
        bot:OB83 = OB83(user=crd['user'], password=crd['password'], ambiente=crd['ambiente'], date=date)
        print(bot.execute(fechar_sap_no_final=True))
        
        Logs().register(status='Concluido', description="Automação FInalizada com Sucesso!")
    except Exception as err:
        Logs().register(status='Error', description=str(err), exception=traceback.format_exc())