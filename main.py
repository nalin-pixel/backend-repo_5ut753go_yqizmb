import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any

from database import db, create_document
from schemas import Questionnaire, Assessment

app = FastAPI(title="Premium Personal Trainer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Trainer API running"}

@app.get("/test")
def test_database():
    """Health check for database connectivity"""
    response = {
        "backend": "running",
        "database": "disconnected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "connected"
            response["collections"] = db.list_collection_names()
    except Exception as e:
        response["database"] = f"error: {str(e)[:80]}"
    return response

class GenerateRequest(BaseModel):
    questionnaire: Questionnaire

@app.post("/generate")
def generate_plan(payload: GenerateRequest) -> Dict[str, Any]:
    q = payload.questionnaire

    # Helper flags
    objetivo = q.objetivo
    nivel = q.nivel
    tem_dor_joelho = any("joelho" in d.lower() for d in (q.lesoes + q.dores))
    tem_dor_coluna = any(x in d.lower() for d in (q.lesoes + q.dores) for x in ["coluna", "lombar", "costas"])
    equipamentos = set(e.lower() for e in q.equipamentos)

    # Define frequência e duração
    freq = q.sessoes_semana
    dur = min(max(q.tempo_por_sessao_min, 25), 75)

    # Estilo base
    if q.estilo_preferido:
        estilo = q.estilo_preferido
    else:
        estilo = "full body" if nivel in ["iniciante", "intermediario"] else "upper/lower"

    # Foco do plano
    if objetivo == "emagrecimento":
        foco = "déficit calórico + alta densidade de treino"
        cardio_final = True
    elif objetivo == "ganho de massa":
        foco = "sobrecarga progressiva com técnica limpa"
        cardio_final = False
    elif objetivo == "recomposicao":
        foco = "mescla de força + cardio moderado"
        cardio_final = True
    else:
        foco = "condicionamento geral com segurança articular"
        cardio_final = True

    # Construção do treino da Semana 1
    def adapt_exec(nome, series_reps, execucao, ajustes=None):
        item = {
            "nome": nome,
            "series_reps": series_reps,
            "execucao": execucao[:300]
        }
        if ajustes:
            item["ajuste"] = ajustes
        return item

    aquecimento = [
        {
            "exercicio": "Mobilidade torácica e quadril",
            "tempo": "2 min",
            "descricao": "círculos de ombro, gato-vaca, abertura de quadril",
            "adaptacao": "sem dor; reduzir amplitude se coluna reclamar" if tem_dor_coluna else ""
        },
        {
            "exercicio": "Ativação glúteo + core",
            "tempo": "2 min",
            "descricao": "ponte de glúteo + pranchas curtas (15–20s)",
            "adaptacao": "apoio de joelho em superfícies macias" if tem_dor_joelho else ""
        }
    ]

    # Escolha de exercícios conforme equipamentos
    def tem(eq):
        return any(eq in e for e in equipamentos)

    principais = []

    # Exercício 1
    if tem("halter") or tem("dumbbell"):
        principais.append(adapt_exec(
            "Agachamento goblet",
            "3 x 8–12",
            "segurar halter ao peito, descer até amplitude confortável, coluna neutra",
            "trocar por cadeira extensora ou agachamento em caixa se joelho doer" if tem_dor_joelho else None
        ))
    elif tem("barra") or tem("smith"):
        principais.append(adapt_exec(
            "Agachamento no smith (box squat)",
            "3 x 8–10",
            "sentar em caixa/banquinho para limitar amplitude e manter controle",
            "altura da caixa reduz dor no joelho" if tem_dor_joelho else None
        ))
    else:
        principais.append(adapt_exec(
            "Agachamento com peso corporal",
            "4 x 12–15",
            "pés estáveis, tronco firme; pausa de 1s no fundo",
            "usar apoio em porta ou cadeira se houver dor no joelho"
        ))

    # Exercício 2
    if tem("maquina") or tem("remada") or tem("cabo"):
        principais.append(adapt_exec(
            "Remada sentada na máquina/cabo",
            "3 x 10–12",
            "peito aberto, puxar cotovelos para trás, segurar 1s",
            "trocar por remada com halteres apoiado no banco se coluna sensível" if tem_dor_coluna else None
        ))
    else:
        principais.append(adapt_exec(
            "Remada curvada com halteres",
            "3 x 8–10",
            "tronco inclinado 30–45°, core ativo, movimentos controlados",
            "apoiar o peito no banco para poupar lombar" if tem_dor_coluna else None
        ))

    # Exercício 3
    if tem("supino") or tem("banco") or tem("halter"):
        principais.append(adapt_exec(
            "Supino com halteres (banco)",
            "3 x 8–12",
            "punhos neutros, linha do peito, pés firmes",
            None
        ))
    else:
        principais.append(adapt_exec(
            "Flexões inclinadas (apoio na mesa/parede)",
            "4 x 8–12",
            "corpo alinhado, amplitude confortável",
            "aumentar inclinação se punho/ombro reclamar"
        ))

    # Exercício 4 (opcional) conforme objetivo
    if objetivo in ["emagrecimento", "recomposicao"]:
        if tem("kettlebell"):
            principais.append(adapt_exec(
                "Kettlebell swing",
                "4 x 15–20",
                "quadril domina o movimento, costas firmes, não elevar além dos ombros",
                "trocar por levantamento terra romeno leve com halteres se lombar sensível" if tem_dor_coluna else None
            ))
        else:
            principais.append(adapt_exec(
                "Levantamento terra romeno (halteres)",
                "3 x 10–12",
                "deslizar halteres nas coxas, quadril para trás, coluna neutra",
                "diminuir amplitude se lombar sinalizar"
            ))

    finalizacao = None
    if cardio_final:
        cardio_tipo = q.cardio_preferido or "caminhada"
        finalizacao = {
            "tipo": cardio_tipo,
            "tempo": 8 if objetivo == "ganho de massa" else 12,
            "intensidade": "RPE 6/10 (respiração acelerada, conversa ainda possível)",
            "observacoes": "mantém gasto calórico sem atrapalhar recuperação" if objetivo != "ganho de massa" else "apenas para condicionamento"
        }

    # Resumo do aluno
    resumo = {
        "objetivo": objetivo,
        "nivel": nivel,
        "lesoes_limitacoes": q.lesoes + q.dores,
        "rotina_tempo": f"{freq}x por semana, {dur} min por sessão",
        "estilo": estilo,
        "equipamentos": list(equipamentos) or ["peso corporal"],
    }

    # Estratégia
    estrategia = {
        "foco": foco,
        "estilo": estilo,
        "intensidade_inicial": "moderada, técnica em primeiro lugar",
        "frequencia": f"{freq}x/semana",
        "duracao": f"{dur} min/sessão",
        "cuidados": [
            "reduzir amplitude em movimentos que irritem joelho" if tem_dor_joelho else "",
            "priorizar estabilidade de core para proteger coluna" if tem_dor_coluna else ""
        ],
        "justificativa": "plano direto e eficiente, alinhado ao objetivo e ao equipamento disponível"
    }

    plano_semana1 = {
        "aquecimento": aquecimento,
        "principais": principais[:4],
        "finalizacao": finalizacao
    }

    recomendacoes = [
        "Proteína: 1.6–2.2 g/kg/dia, dividir em 3–4 refeições",
        "Creatina 3–5 g/dia se não houver contraindicação",
        "Dormir 7–8h; se não for possível, reduzir 1 série por exercício",
        "Intervalos de 60–90s entre séries (até 120s em compostos)",
        "Use gatilhos: horário fixo e check rápido pós-treino para reforço"
    ]

    progresso_4s = [
        "Semana 1: consolidar técnica; ajustar cargas para RPE 7/10 no final",
        "Semana 2: aumentar carga ou reps (+2) mantendo forma",
        "Semana 3: trocar 1 variação por mais desafiadora (ex: banco plano -> inclinado)",
        "Semana 4: incluir 1 sessão com HIIT leve (6x30s) se articulações estiverem bem; reavaliar medidas"
    ]

    avisos = [
        "Dor articular aguda = parar, reduzir amplitude/carga ou trocar a variação",
        "Coluna: sempre neutra; se houver desconforto, use apoios e isometrias",
        "Joelho: não travar; use caixa/apoio para controlar amplitude",
        "Progresso depende de consistência: 3–4x/semana por 4+ semanas",
    ]

    resposta = {
        "resumo": resumo,
        "estrategia": estrategia,
        "semana1": plano_semana1,
        "recomendacoes": recomendacoes,
        "progresso": progresso_4s,
        "avisos": avisos
    }

    # Persistir avaliação
    try:
        doc = Assessment(questionnaire=q, plan=resposta)
        create_document("assessment", doc)
    except Exception:
        pass

    return resposta


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
