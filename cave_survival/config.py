import pydantic


class Config(pydantic.BaseModel):
    screen_width: int = 800
    screen_height: int = 600

    BLACK: tuple[int] = (0, 0, 0)
    WHITE: tuple[int] = (255, 255, 255)
    GREY: tuple[int] = (128, 128, 128)
    RED: tuple[int] = (255, 128, 128)


config = Config()
