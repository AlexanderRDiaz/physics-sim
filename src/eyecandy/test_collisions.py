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

        for x in range(25, 400, 25):
            for y in range(25, 400, 25):
                world.CreateBoxBody(
                    20,
                    20,
                    Vector(x, y),
                    1.0,
                    0.5,
                    False,
                )

        def Prerender(world) -> None:
            for body in world.Bodies:
                body.Color = (0, 0, 0)
                body.Rotate(1)

        def OnCollide(b1, b2) -> None:
            b1.Color = (255, 0, 0)
            b2.Color = (255, 0, 0)

        world.OnCollide = OnCollide
        world.Prerender = Prerender

        for idx in range(220):
            drawlib.StoreFrame(world.GenerateFrame(), testlib.FRAMES_PATH, idx)
            world.StepTime(0.0416)

        movie = JES.makeMovieFromInitialFile(f'{testlib.FRAMES_PATH}/frame000.jpg')
        JES.writeAnimatedGif(movie, f'{testlib.BIN_PATH}/{testlib.GIFName(__file__)}.gif')


if __name__ == '__main__':
    testlib.SoloRunOutput(__file__)
    unittest.main()
