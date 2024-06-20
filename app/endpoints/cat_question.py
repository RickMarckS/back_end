from fastapi import APIRouter, Body, HTTPException
from app.models.cat_question import lista_gatos_tratada, datas_nascimento
from pydantic import BaseModel

router = APIRouter()

class GatoNome(BaseModel):
    nome: str

class GatoRaca(BaseModel):
    raca: str

# Método que recebe um ID e retorna os dados do gato e sua data de nascimento
@router.get("/gato/{id}")
def get_gato_por_id(id: int):
    try:
        gato = next((g for g in lista_gatos_tratada if g.id == id), None)
        if not gato:
            raise HTTPException(status_code=404, detail="O gato não foi encontrado")
        
        data_nascimento = next((d['data_nascimento'] for d in datas_nascimento if d['id'] == id), None)
        if data_nascimento is None:
            raise HTTPException(status_code=422, detail="Data de nascimento não encontrada para o gato")
        
        return {
            'id': gato.id,
            'nome': gato.nome,
            'raca': gato.raca,
            'idade': gato.idade,
            'data_nascimento': data_nascimento
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

# Método que retorna a lista de gatos sem data de nascimento e sem idade
@router.get("/gato")
def get_gatos():
    try:
        gatos_sem_data_nascimento = []
        for gato in lista_gatos_tratada:
            if not any(d['id'] == gato.id for d in datas_nascimento):
                gatos_sem_data_nascimento.append({
                    'id': gato.id,
                    'nome': gato.nome,
                    'raca': gato.raca
                })
        return gatos_sem_data_nascimento
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

# Método que retorna uma lista de todos os gatos mais velhos com a mesma idade
@router.get("/gatos-mais-velhos")
def get_gatos_mais_velhos():
    try:
        idade_maxima = max(gato.idade for gato in lista_gatos_tratada)
        gatos_mais_velhos = []
        for gato in lista_gatos_tratada:
            if gato.idade == idade_maxima:
                data_nascimento = next((d['data_nascimento'] for d in datas_nascimento if d['id'] == gato.id), None)
                if data_nascimento is None:
                    raise HTTPException(status_code=422, detail="Data de nascimento não encontrada para o gato")
                
                gatos_mais_velhos.append({
                    'id': gato.id,
                    'nome': gato.nome,
                    'raca': gato.raca,
                    'idade': gato.idade,
                    'data_nascimento': data_nascimento
                })
        return gatos_mais_velhos
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

# Método que busca gatos por um termo de busca no nome
@router.post("/buscar-gatos")
def buscar_gatos_por_nome(termo_busca: GatoNome = Body(...)):
    try:
        gatos_encontrados = []
        for gato in lista_gatos_tratada:
            if gato.nome.lower() == termo_busca.nome.lower():
                data_nascimento = next((d['data_nascimento'] for d in datas_nascimento if d['id'] == gato.id), None)
                if data_nascimento is None:
                    raise HTTPException(status_code=422, detail="Data de nascimento não encontrada para o gato com esse nome")
                
                gatos_encontrados.append({
                    'id': gato.id,
                    'nome': gato.nome,
                    'raca': gato.raca,
                    'idade': gato.idade,
                    'data_nascimento': data_nascimento
                })
        if not gatos_encontrados:
            raise HTTPException(status_code=404, detail="Nenhum gato com esse nome foi encontrado")
        return {'gatos_encontrados': gatos_encontrados}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

# Método que busca gatos por raça
@router.post("/buscar-raca")
def buscar_gatos_por_raca(termo_busca: GatoRaca = Body(...)):
    try:
        gatos_encontrados = []
        for gato in lista_gatos_tratada:
            if gato.raca.lower() == termo_busca.raca.lower():
                data_nascimento = next((d['data_nascimento'] for d in datas_nascimento if d['id'] == gato.id), None)
                if data_nascimento is None:
                    raise HTTPException(status_code=422, detail="Data de nascimento não encontrada para o gato com essa raça")
                
                gatos_encontrados.append({
                    'id': gato.id,
                    'nome': gato.nome,
                    'raca': gato.raca,
                    'idade': gato.idade,
                    'data_nascimento': data_nascimento
                })
        if not gatos_encontrados:
            raise HTTPException(status_code=404, detail="Nenhum gato dessa raça foi encontrado")
        return {'gatos_encontrados': gatos_encontrados}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno do servidor")
