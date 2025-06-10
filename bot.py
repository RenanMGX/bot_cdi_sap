"""
WARNING:

Please make sure you install the bot dependencies with `pip install --upgrade -r requirements.txt`
in order to get all the dependencies on your Python environment.

Also, if you are using PyCharm or another IDE, make sure that you use the SAME Python interpreter
as your IDE.

If you get an error like:
```
ModuleNotFoundError: No module named 'botcity'
```

This means that you are likely using a different Python interpreter than the one used to install the dependencies.
To fix this, you can either:
- Use the same interpreter as your IDE and install your bot with `pip install --upgrade -r requirements.txt`
- Use the same interpreter as the one used to install the bot (`pip install --upgrade -r requirements.txt`)

Please refer to the documentation for more information at
https://documentation.botcity.dev/tutorials/custom-automations/python-custom/
"""

# Import for integration with BotCity Maestro SDK
from botcity.maestro import * #type: ignore
import traceback
from patrimar_dependencies.gemini_ia import ErrorIA
from datetime import datetime
from Entities.ob83 import OB83
from time import sleep

# Disable errors if we are not connected to Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False #type: ignore


class Execute:
    @staticmethod
    def start():
        date_param = execution.parameters.get("date")
        if date_param:
            date = datetime.strptime(str(date_param), "%d/%m/%Y")
        else:
            date = datetime.now() # Data de exemplo, pode ser alterada conforme necessário
        
        crd_param = execution.parameters.get("crd")
        if not isinstance(crd_param, str):
            raise ValueError("Parâmetro 'crd_param' deve ser uma string representando o label da credencial.")
        
        try:
            bot:OB83 = OB83(
                maestro=maestro,
                user=maestro.get_credential(label=crd_param, key="user"),
                password=maestro.get_credential(label=crd_param, key="password"),
                ambiente=maestro.get_credential(label=crd_param, key="ambiente"),
                date=date
            )
            bot.execute()
        finally:
            bot.fechar_sap() # type: ignore    
        

if __name__ == '__main__':
    maestro = BotMaestroSDK.from_sys_args()
    execution = maestro.get_execution()
    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")

    for _ in range(3):
        try:
            Execute.start()
            
            maestro.finish_task(
                        task_id=execution.task_id,
                        status=AutomationTaskFinishStatus.SUCCESS,
                        message="Tarefa Registrar CDI no SAP finalizada com sucesso",
                        total_items=1, # Número total de itens processados
                        processed_items=1, # Número de itens processados com sucesso
                        failed_items=0 # Número de itens processados com falha
            )
            break
            
            
        except Exception as error:
            ia_response = "Sem Resposta da IA"
            try:
                token = maestro.get_credential(label="GeminiIA-Token-Default", key="token")
                if isinstance(token, str):
                    ia_result = ErrorIA.error_message(
                        token=token,
                        message=traceback.format_exc()
                    )
                    ia_response = ia_result.replace("\n", " ")
            except Exception as e:
                maestro.error(task_id=int(execution.task_id), exception=e)

            maestro.error(task_id=int(execution.task_id), exception=error, tags={"IA Response": ia_response})
            
        sleep(60 * 5)
