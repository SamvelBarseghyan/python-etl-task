from pydantic import BaseModel, Field


class ResponseContent(BaseModel):
    """
    Class/Model that represent structure of the response of the API call
    """
    player_name: str = Field(..., example="YrikGood")
    total_games: int = Field(..., example=20)
    min_kda: float = Field(..., example=2.15)
    avg_kda: float = Field(..., example=3.89)
    max_kda: float = Field(..., example=5.45)
    min_kp: str = Field(..., example="21.23%")
    avg_kp: str = Field(..., example="54.87%")
    max_kp: str = Field(..., example="72.55%")
    game: str = "Dota"
