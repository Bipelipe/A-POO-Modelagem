from dataclasses import dataclass


@dataclass(frozen=True)
class Livro:
    id: int
    titulo: str
    autor: str
