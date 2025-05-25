from __future__ import annotations

import unittest

import utils

from src import JES, drawlib
from src.container import Container
from src.matrix import Vector


class Main(unittest.TestCase):
    setUp = utils.setup
    tearDown = utils.cleanup

    def test_CreateGIF(self: Main) -> None:
        world = Container()
        for x in range(40, 400, 40):
            for y in range(40, 400, 40):
                world.CreateBoxBody(
                    20,
                    20,
                    Vector(x, y),
                    1.0,
                    0.5,
                    False,
                )

        def Prerender(container: Container) -> None:
            for body in container.Bodies:
                body.Rotate(3)

        world.Attach(Prerender)

        for idx in range(121):
            drawlib.StoreFrame(world.GenerateFrame(), utils.FRAMES_PATH, idx)
            world.StepTime()

        movie = JES.makeMovieFromInitialFile(f'{utils.FRAMES_PATH}/frame000.jpg')
        JES.writeAnimatedGif(movie, f'{utils.BIN_PATH}/{__name__[5:]}.gif')


if __name__ == '__main__':
    unittest.main()
