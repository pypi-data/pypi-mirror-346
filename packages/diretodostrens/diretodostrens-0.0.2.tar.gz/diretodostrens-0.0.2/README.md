# Direto dos Trens API

Essa biblioteca em python utiliza a seguinte API REST:
 
https://static.diretodostrens.com.br/swagger/

Para obter informações sobre o estado das linhas de trem da região metropolitana de São Paulo.

Obrigado ao [@CTassisF](https://github.com/CTassisF) pela API pública :)

> [!NOTE]
> Esse projeto está em fase beta (sem Semver, mas já acho que faz sentido chamar assim)
>
> Ele está disponível no PyPI:
    
```sh
pip install diretodostrens
```

## Usos:
    
```python
from trens import Linha

diamante = Linha("Diamante")
# ou
esmeralda = Linha(9)

print(diamante.estado())
print(esmeralda.estado())
```