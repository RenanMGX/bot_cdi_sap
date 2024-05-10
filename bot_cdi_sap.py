from datetime import datetime
from Entities.ob83 import OB83
from Entities.credencial import Credential
import os
import traceback

if __name__ == "__main__":
    try:
        crd:dict = Credential("SAP_QAS").load()
    
        date = datetime.now()
    
        bot:OB83 = OB83(user=crd['user'], password=crd['password'], ambiente="S4Q", date=date)
        print(bot.execute(fechar_sap_no_final=True))
        
    except Exception as error:
        path:str = "logs/"
        if not os.path.exists(path):
            os.makedirs(path)
        file_name = path + f"LogError_{datetime.now().strftime('%d%m%Y%H%M%Y')}.txt"
        with open(file_name, 'w', encoding='utf-8')as _file:
            _file.write(traceback.format_exc())
        raise error
