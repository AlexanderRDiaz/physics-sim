from __future__ import annotations

import unittest

from src import JES, drawlib, testlib
from src.matrix import Vector
from src.world import World


class Main(unittest.TestCase):
    setUp = testlib.GIFSetup
    tearDown = testlib.GIFCleanup

    def test_GIF(self: Main) -> None:
        world = World()
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

        def Prerender(world: World) -> None:
            for body in world.Bodies:
                body.Rotate(1)

        world.Attach(Prerender)

        for idx in range(361):
            drawlib.StoreFrame(world.GenerateFrame(), testlib.FRAMES_PATH, idx)
            world.StepTime()

        movie = JES.makeMovieFromInitialFile(f'{testlib.FRAMES_PATH}/frame000.jpg')
        JES.writeAnimatedGif(movie, f'{testlib.BIN_PATH}/{testlib.GIFName(__file__)}.gif')


if __name__ == '__main__':
    testlib.SoloRunOutput(__file__)
    unittest.main()
