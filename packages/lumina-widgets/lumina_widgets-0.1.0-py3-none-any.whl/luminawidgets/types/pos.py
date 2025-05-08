from pydantic import BaseModel, Field



class Point(BaseModel):
    """Point in 2D space.
    
    Args:
        x (int): X coordinate of the point.
        y (int): Y coordinate of the point.
    """
    
    x: int = Field(0, description="X coordinate of the point.")
    y: int = Field(0, description="Y coordinate of the point.")