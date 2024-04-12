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
    except:
        error = traceback.format_exc()
        print(error)
        path:str = "logs/"
        if not os.path.exists(path):
            os.makedirs(path)
        data_log:str = datetime.now().strftime('%d%m%Y%H%M%S')
        file_name = f"{path}LogError_{data_log}.txt"
        with open(file_name, 'w', encoding='utf-8')as _file:
            _file.write(error)