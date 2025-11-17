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
    objetivo: Literal[
        "emagrecimento", "ganho de massa", "recomposicao", "condicionamento", "saude"
    ] = Field(..., description="Objetivo principal")
    nivel: Literal["iniciante", "intermediario", "avancado"] = Field(..., description="Nível de experiência")
    idade: Optional[int] = Field(None, ge=10, le=100)
    sexo: Optional[Literal["masculino", "feminino", "outro"]] = None
    peso_kg: Optional[float] = Field(None, ge=30, le=300)
    altura_cm: Optional[int] = Field(None, ge=120, le=230)

    lesoes: List[str] = Field(default_factory=list, description="Lesões e limitações relevantes")
    dores: List[str] = Field(default_factory=list, description="Dores atuais a considerar")

    tempo_por_sessao_min: int = Field(..., ge=15, le=120)
    sessoes_semana: int = Field(..., ge=2, le=7)
    rotina: Optional[str] = Field(None, description="Janelas de treino, agenda, turnos")

    estilo_preferido: Optional[Literal[
        "full body", "abc", "upper/lower", "circuito", "funcional", "cross", "maquinas"
    ]] = None

    equipamentos: List[str] = Field(default_factory=list, description="Equipamentos disponíveis")
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
