from pydantic import BaseModel, Field



class NodeSize(BaseModel):
    """Node sizes in pixels.
    
    Args:
        width (int): Width of the node in pixels.
        height (int): Height of the node in pixels.
        radius (float): Corner radius of the node in pixels.
        title_height (float): Height of the title bar in pixels.
        port_spacing (float): Spacing between ports in pixels.
    """

    width: int = Field(180, description="Width of the node in pixels.")
    height: int = Field(120, description="Height of the node in pixels.")
    radius: float = Field(5.0, description="Corner radius of the node in pixels.")
    title_height: float = Field(24.0, description="Height of the title bar in pixels.")
    port_spacing: float = Field(22.0, description="Spacing between ports in pixels.")



class NodeColor(BaseModel):
    """Node colors.
    
    Args:
        background (str): Background color of the node in hex format.
        title (str): Title bar color of the node in hex format.
    """
    
    background: str = Field("#3D3D3D", description="Background color of the node in hex format.")
    title: str = Field("#2D2D30", description="Title bar color of the node in hex format.")
