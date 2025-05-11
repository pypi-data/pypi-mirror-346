from .dados import *
        
lines = Linhas()
json = lines.dados
linhas = lines.ver_nomes()

#todo: 
    # - remover
    # - ou servir de alias para um método da classe Linha
    # - ou ser mais otimizado
def da_linha(valor: Union[int, str], completo: bool=True, verboso: bool=True):
    """
    Retorna o estado de uma linha.
    
    :param valor: Nome ou número da linha a ser pesquisada
    :param completo: A resposta deve ser completa?
    :param verboso: Deve ser printado qual condição foi retornada?
    """
    valor = str(valor)
    linhas = lines.ver_nomes()
    
    if valor.isnumeric():
        if valor in linhas.keys():
            if verboso:
                print("Numero da linha encontrado")
            if completo:
                return [y for y in filter(
                lambda x: True 
                    if x["codigo"] == int(valor) 
                else False, json
                )]
            return linhas[valor]
        else:
            return "Número da linha inválido"
    elif valor in linhas.values():
        if verboso:
            print("Nome encontrado")
        nome=next((k for k, v in linhas.items() if v == valor), None)
        return nome
    else:
        return "Nome da linha inválido"
