from __future__ import annotations

from collections.abc import Callable

from PIL import Image, ImageDraw

from body import BoxBody, CircleBody


class Container:
    __slots__ = [
        'Width',
        'Height',
        'Bodies',
        'Work',
    ]

    Width: int
    Height: int
    Bodies: list[BoxBody | CircleBody]
    Work: list[Callable[[Container], None]]

    def __init__(self: Container) -> None:
        self.Width, self.Height = 400, 400
        self.Bodies = []
        self.Work = []

    def Attach(self: Container, work: Callable[[Container], None]) -> None:
        self.Work.append(work)

    def StepTime(self: Container) -> Image.Image:
        img = Image.new('RGB', (self.Width, self.Height), (255, 255, 255))
        draw = ImageDraw.Draw(img)

        for func in self.Work:
            func(self)

        for body in self.Bodies:
            body.Draw(draw)

        return img

    # Arguments for this function are the same as the constructor for CircleBody class.
    def CreateCircleBody(self: Container, *args) -> None:
        self.Bodies.append(CircleBody(*args))

    # Arguments for this function are the same as the constructor for BoxBody class.
    def CreateBoxBody(self: Container, *args) -> None:
        self.Bodies.append(BoxBody(*args))
