from fastapi import APIRouter, Body, HTTPException
from app.models.cat_question import lista_gatos, datas_nascimento
from pydantic import BaseModel
router = APIRouter()

class GatoNome(BaseModel):
    nome:str


class GatoRaca(BaseModel):
    raca:str


# Método que recebe um ID e retorna os dados do gato e sua data de nascimento
@router.get("/gato/{id}")
def get_gato_por_id(id: int):
    try:
        gato = next((g for g in lista_gatos if g.id == id), None)

        if not gato: #se não achar o id retorna um erro de not found
            raise HTTPException(status_code=404, detail="O gato não foi encontrado") 
        
        data_nascimento = next((d['data_nascimento'] for d in datas_nascimento if d['id'] == id), None)
        
        if data_nascimento is None: #se a data for vazia retorna o erro de não ter data? indisponivél
            raise HTTPException(status_code=422, detail="Data de nascimento não encontrada para o gato")

        return {
            'id': gato.id,
            'nome': gato.nome,
            'raca': gato.raca,
            'idade': gato.idade,
            'data_nascimento': data_nascimento
        }
    except HTTPException as e: #criando uma execeção que captura as exceções dentro do bloco e atribuindo a variavél e para capturar a exceção
        raise e
    except Exception as er: #pega toda execeção fora do bloco
        raise HTTPException(status_code=500, detail="Erro interno do servidor")
    
# Método que retorna a lista de gatos sem data de nascimento e sem idade
@router.get("/gato")
def get_gatos():
    try:
        gatos_sem_data_nascimento = []
        for gato in lista_gatos:
            if not any(d['id'] == gato.id for d in datas_nascimento):
                gatos_sem_data_nascimento.append({
                    'id': gato.id,
                    'nome': gato.nome,
                    'raca': gato.raca
                })
        return gatos_sem_data_nascimento
    except Exception as e:
        raise HTTPException(status_code=422, detail="Gatos gatos sem data de nascimento") #colocar erro pra falta de recurso

# Método que retorna uma lista de todos os gatos mais velhos com a mesma idade
@router.get("/gatos-mais-velhos")
def get_gatos_mais_velhos():
    try:
        # Encontra a idade máxima entre todos os gatos
        idade_maxima = max(gato.idade for gato in lista_gatos)
        
        # Lista para armazenar todos os gatos mais velhos com a mesma idade máxima
        gatos_mais_velhos = []
        for gato in lista_gatos:
            if gato.idade == idade_maxima:
                # Encontra a data de nascimento do gato
                data_nascimento_gato = next((d['data_nascimento'] for d in datas_nascimento if d['id'] == gato.id), None)
                if data_nascimento_gato is None:
                    raise HTTPException(status_code=422, detail="Os gatos não possuem data de nascimento")
                # Adiciona o gato à lista com sua data de nascimento
                gatos_mais_velhos.append({
                    'id': gato.id,
                    'nome': gato.nome,
                    'raca': gato.raca,
                    'idade': gato.idade,
                    'data_nascimento': data_nascimento_gato
                })
        return gatos_mais_velhos
    except HTTPException as er:
        raise er
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Método que busca gatos por um termo de busca no nome
@router.post("/buscar-gatos")
def buscar_gatos_por_nome(termo_busca: GatoNome = Body(...)):
    try:
        gatos_encontrados = []
        for gato in lista_gatos:
            if gato.nome.lower() == termo_busca.nome.lower():
                # Encontrar a data de nascimento do gato
                data_nascimento = next((d['data_nascimento'] for d in datas_nascimento if d['id'] == gato.id), None)
                
                if data_nascimento is None:
                    raise HTTPException(status_code=422, detail="Data de nascimento não encontrada para o gato com esse nome")
                
                # Adicionar o gato com sua data de nascimento
                gatos_encontrados.append({
                    'id': gato.id,
                    'nome': gato.nome,
                    'raca': gato.raca,
                    'idade': gato.idade,
                    'data_nascimento': data_nascimento
                })   
        if not gatos_encontrados: # erro se o array estiver vazio
            raise HTTPException(status_code=404, detail="Nenhum gato com esse nome foi encontrado")
        return {'gatos_encontrados': gatos_encontrados}
    except HTTPException as er:
        raise er
    except Exception as e: # erro de qualquer outra coisa
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@router.post("/buscar-raca")
def buscar_gatos_por_raca(termo_busca: GatoRaca = Body(...)):
    try:
        gatos_encontrados = []
        for gato in lista_gatos:
            if gato.raca.lower() == termo_busca.raca.lower():
                # Encontrar a data de nascimento do gato
                data_nascimento = next((d['data_nascimento'] for d in datas_nascimento if d['id'] == gato.id), None)
                
                if data_nascimento is None:
                    raise HTTPException(status_code=422, detail="Data de nascimento não encontrada para o gato com esse raça")
                
                # Adicionar o gato com sua data de nascimento
                gatos_encontrados.append({
                    'id': gato.id,
                    'nome': gato.nome,
                    'raca': gato.raca,
                    'idade': gato.idade,
                    'data_nascimento': data_nascimento
                })   
        if not gatos_encontrados: # erro se o array estiver vazio
            raise HTTPException(status_code=404, detail="Nenhum gato dessa raça foi encontrado")
        return {'gatos_encontrados': gatos_encontrados}
    except HTTPException as er:
        raise er
    except Exception as e: # erro de qualquer outra coisa
        raise HTTPException(status_code=500, detail="Erro interno do servidor")
