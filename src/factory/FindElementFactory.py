from selenium.webdriver.common.by import By

class FindElementFactory:
    def __init__(self):
        pass

    def getArgs(self, element):
        match element.keys():
            case "id":
                tipo = By.ID
            case _:
                return None
        retorno = (tipo, element.values())
        return retorno