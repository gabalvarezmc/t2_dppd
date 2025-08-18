from pydantic import BaseModel, Field

class SuggestionResponse(BaseModel):
    suggestion: str = Field(..., description="Técnica sugerida para resolver el Sudoku")
    status: str = Field(..., description="Status de la predicción")
    sudoku_digitalized: str = Field(..., min_length=81, max_length=81, description="Cadena con los 81 dígitos del Sudoku")
