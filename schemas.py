"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Literal, Dict, Any

# Example schemas (retain for reference)
class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Fitness-specific schemas used by this app

class Questionnaire(BaseModel):
    # Objetivo e nível (mantidos para compatibilidade com o gerador atual)
    objetivo: Literal[
        "emagrecimento", "ganho de massa", "recomposicao", "condicionamento", "saude"
    ] = Field(..., description="Objetivo principal")
    nivel: Literal["iniciante", "intermediario", "avancado"] = Field(..., description="Nível de experiência")

    # 1. Identidade física e rotina de vida
    idade: Optional[int] = Field(None, ge=10, le=100)
    altura_cm: Optional[int] = Field(None, ge=120, le=230)
    peso_kg: Optional[float] = Field(None, ge=30, le=300)
    peso_max_adulto: Optional[float] = Field(None, ge=30, le=400)
    peso_min_adulto: Optional[float] = Field(None, ge=30, le=400)
    corpo_descr: Optional[str] = Field(None, description="Descrição do corpo hoje")
    energia_nivel: Optional[str] = None
    rotina_prof: Optional[Literal["sentado", "em_pe", "alternancia"]] = None
    horas_tela_dia: Optional[int] = Field(None, ge=0, le=18)
    estresse_nivel: Optional[str] = None

    # 2. Objetivo claro
    objetivo_quilos: Optional[float] = None
    objetivo_tempo: Optional[str] = None
    motivo_emocional: Optional[str] = None
    sentimento_desejado: Optional[str] = None
    comprometimento_nota: Optional[int] = Field(None, ge=0, le=10)
    comprometimento_motivo: Optional[str] = None

    # 3. Histórico de treinos
    treinou_com_personal: Optional[bool] = None
    metodos_feitos: List[str] = Field(default_factory=list)
    funcionou: Optional[str] = None
    nao_funcionou: Optional[str] = None
    treino_consistente_descricao: Optional[str] = None
    treino_consistente_tempo: Optional[str] = None
    dificuldade_aprender_movimentos: Optional[bool] = None

    # 4. Saúde geral
    lesoes: List[str] = Field(default_factory=list, description="Lesões e limitações relevantes")
    dores: List[str] = Field(default_factory=list, description="Dores atuais a considerar")
    estado_articulacoes: Optional[str] = None
    cirurgias: Optional[str] = None
    limitacao_medica: Optional[str] = None
    dor_partes: Optional[str] = None
    sono_rotina_qualidade: Optional[str] = None
    nutricionista_acompanhamento: Optional[bool] = None
    historico_condicoes: Optional[str] = None

    # 5. Alimentação e hábitos
    dia_alimentar: Optional[str] = None
    cozinha: Optional[bool] = None
    dificuldade_proteina: Optional[bool] = None
    cafe_da_manha: Optional[Literal["toma", "pula"]] = None
    alcool_frequencia: Optional[str] = None
    hidratacao: Optional[str] = None
    aversoes_restricoes: Optional[str] = None

    # 6. Equipamentos disponíveis
    local_treino: Optional[Literal["academia", "casa", "ambos"]] = None
    equipamentos: List[str] = Field(default_factory=list, description="Equipamentos disponíveis")
    disposto_comprar_equip: Optional[bool] = None

    # 7. Tempo real disponível
    sessoes_semana: int = Field(..., ge=2, le=7)
    tempo_por_sessao_min: int = Field(..., ge=15, le=120)
    preferencia_horario: Optional[Literal["manha", "tarde", "noite"]] = None

    # 8. Estilo de treino preferido
    estilo_preferido: Optional[Literal[
        "tecnico_lento", "rapido_intenso", "mistura", "full body", "abc", "upper/lower", "circuito", "funcional", "maquinas"
    ]] = None
    treinos_longos_desanima: Optional[bool] = None
    estrutura_fixa_ou_variedade: Optional[Literal["fixa", "variedade"]] = None
    foco_preferido: Optional[Literal["forca", "cardio", "estetica", "performance"]] = None

    # 9. Sensação corporal
    dificuldade_sentir_gluteos: Optional[bool] = None
    ativar_abdomen_facilidade: Optional[str] = None
    onde_acumula_gordura: Optional[str] = None
    musculos_dificeis_responder: Optional[str] = None
    desconfortos_movimentos: List[str] = Field(default_factory=list)

    # 10. Psicológico do treino
    desistir_motivos: Optional[str] = None
    coach_estilo: Optional[Literal["motivador", "tecnico", "firme", "suave"]] = None
    empolga: Optional[str] = None
    vergonha_motivo: Optional[str] = None
    paciencia_aprender_nota: Optional[int] = Field(None, ge=0, le=10)

    # 11. Vida social e impacto
    fim_de_semana: Optional[str] = None
    sono_fds_pior: Optional[bool] = None
    viagens_programadas: Optional[str] = None
    apoio_rotina: Optional[str] = None

    # 12. Emagrecimento específico
    facilidade_perder_peso: Optional[Literal["facil", "medio", "dificil"]] = None
    facilidade_ganhar_musculo: Optional[Literal["facil", "medio", "dificil"]] = None
    protocolos_extremos: Optional[str] = None
    gatilho_comer_alem: Optional[str] = None

    # 13. Massa muscular específica
    grupamentos_prioridade: Optional[str] = None
    nao_gosta_treinar: Optional[str] = None
    objetivos_esteticos: Optional[str] = None
    suplementos_usados: Optional[str] = None

    # 14. Zona de risco e motivação
    evento_motivador: Optional[str] = None
    barreiras_reais: Optional[str] = None
    mudaria_estilo_vida: Optional[str] = None

    # 15. O mais importante
    obra_prima_precisa_ver: Optional[str] = None
    como_quer_se_ver_3m: Optional[str] = None
    motivo_secreto: Optional[str] = None

    # Extras mantidos
    sexo: Optional[Literal["masculino", "feminino", "outro"]] = None
    rotina: Optional[str] = Field(None, description="Janelas de treino, agenda, turnos")
    cardio_preferido: Optional[Literal["esteira", "bike", "eliptico", "pular corda", "caminhada", "nenhum"]] = "caminhada"
    historico: Optional[str] = Field(None, description="Histórico de treinos e pausas")
    personalidade: Optional[str] = Field(None, description="O que motiva, preferências de treino")
    restricoes: Optional[str] = Field(None, description="Restrições médicas ou alimentares")


class Assessment(BaseModel):
    """Documento salvo com questionário e plano gerado"""
    questionnaire: Questionnaire
    plan: Dict[str, Any]

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
