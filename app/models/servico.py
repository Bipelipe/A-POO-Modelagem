from dataclasses import dataclass


@dataclass(frozen=True)
class Servico:
    id: int
    nome: str
    tipo: str
