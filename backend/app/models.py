from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from .database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), unique=True, nullable=False, index=True)
    eh_basico = Column(Boolean, default=False, nullable=False)

    produzidos = relationship("Receita", back_populates="resultado_item", cascade="all, delete")


class Receita(Base):
    __tablename__ = "receitas"

    id = Column(Integer, primary_key=True, index=True)
    resultado_id = Column(Integer, ForeignKey("items.id", ondelete="CASCADE"), nullable=False)
    quantidade_resultado = Column(Integer, default=1, nullable=False)

    resultado_item = relationship("Item", back_populates="produzidos")
    ingredientes = relationship("IngredienteReceita", back_populates="receita", cascade="all, delete")


class IngredienteReceita(Base):
    __tablename__ = "ingredientes_receita"
    __table_args__ = (
        UniqueConstraint("receita_id", "item_id", name="uq_receita_item"),
    )

    id = Column(Integer, primary_key=True, index=True)
    receita_id = Column(Integer, ForeignKey("receitas.id", ondelete="CASCADE"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id", ondelete="CASCADE"), nullable=False)
    quantidade = Column(Integer, default=1, nullable=False)

    receita = relationship("Receita", back_populates="ingredientes")
    item = relationship("Item")


