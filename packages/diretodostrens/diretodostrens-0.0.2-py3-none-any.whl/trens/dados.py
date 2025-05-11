import sys
import requests
from typing import Optional, Union

# todos(futuro):
    # - separar linhas por metrô, trem, viamobilidade e viaquatro
    # - colorizar com colorama
        # diferenciar cores entre linhas e empresas
class Linhas:
    """
    Representa todas as linhas do transporte ferroviário paulista, suportadas pela API:
         
     https://www.diretodostrens.com.br/api
    """
    
    __lista = {
        1: "Azul", 2: "Verde",
        3: "Vermelha",
        4: "Amarela", 5: "Lilás",
        7: "Rubi", 8: "Diamante",
        9: "Esmeralda", 
        10: "Turquesa", 
        11: "Coral", 12: "Safira", 
        13: "Jade", 15: "Prata"
    }
     
    def __init__(self):
        self.dados = self.__api_request()
        self.nomes = self.lista()
        self.numeros = self.ver_nomes().keys
        self.statuss = False
    
    @classmethod
    def lista(cls) -> dict[int, str]:
        return cls.__lista
        # return cls.__lista
        
    def geral(self, escrever: bool=False) -> Optional[str]:
        """
        Retorna (ou imprime) a situação de todas as linhas retornadas pela API
        
        :return: string
        """
        valores = ""
        
        for data in self.dados:
            valores += ("="*10)+"\n"
            for key, value in data.items():
                valores += f"{key}: {value}\n"
                
        if not escrever:
            return valores
        print(valores)
            
    def teste(self) -> int:
        return 2
        
    def ver_nomes(self) -> dict[int, str]:
        """
        Retorna um dicionário com todas as linhas e seus códigos
        """
        return self.nomes
    
    def codigos() -> list[str]:
        """
        Retorna uma lista com todos os números das linhas
        
        :return: Lista
        """
        return [ infos["codigo"] for infos in self.dados]
        
    def estado(self) -> Union[bool, list[str]]:
        """
        Exibe o estado das linhas.
        Se todas estiverem em Operação Normal, retornará True
        Mas, se tiver pelo menos uma linha com estado anormal, será mostrado a situação dela(s) em formato string.
        
        :return: Bool ou string
        """
        anormais = []
        for i in self.dados:
            if not "Operação Normal" in i["situacao"]:
                 anormais += [i]
        return True if not anormais else anormais
        
    def __api_request(self) -> dict[Union[int, str, None], Optional[str]]:
        """
        Método privado para fazer requisições a API
        
        :return: JSON com todos os dados retornados
        """
        try:
            resposta = requests.get("https://www.diretodostrens.com.br/api/status")
            if resposta.status_code == 200:
                return resposta.json()
            return {None: None}
        except requests.exceptions.ConnectionError:
            print("Sem conexão!")
            
            sys.exit()
        
class Linha(Linhas):
    """
    Representa uma linha dentre as 13 existentes
    """
    def __init__(self, nome: str):
        super().__init__()
        self.nome = nome
        self.numero = 10
        self.statu = "status"
        self.situacao = "normal"
        
    def teste(self) -> int:
        # Todo: remover
        return 1
        
    def estado(self, booleano: bool=False) -> Union[bool, str, None]:
        """
        Retorna o estado apenas da linha referenciada no atributo :attr:`nome`
        
        :return: Booleano
        """
        if not self.nome == None:
            st = next((x for x in self.dados if x["codigo"] == self.numero), None)
            if booleano:
                if st["situacao"] == "Operação Normal":
                    return True
                return False
            return st
        return None
        
    @property
    def numero(self):
        return self._numero
        
    @numero.setter
    def numero(self, valor: int):
        self._numero = next((int(k) for k, v in self.ver_nomes().items() if v == self.nome), None)
        
    @property
    def nome(self) -> str:
        return self._name
        
    @nome.setter
    def nome(self, valor: int):
        self._name = ( valor 
        if valor in self.nomes.values()
            else None )
        