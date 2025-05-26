from __future__ import annotations

import unittest

from src import JES, collisions, drawlib, testlib
from src.body import BoxBody
from src.container import Container
from src.matrix import Vector


class Main(unittest.TestCase):
    setUp = testlib.GIFSetup
    tearDown = testlib.GIFCleanup

    def test_GIF(self: Main) -> None:
        world = Container()

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

        def Prerender(container: Container) -> None:
            for b in container.Bodies:
                b.Color = (0, 0, 0)
                b.Rotate(1)

            resolved = []

            for b1 in container.Bodies:
                if not isinstance(b1, BoxBody):
                    continue

                for b2 in container.Bodies:
                    if (b1 is b2) or (not isinstance(b2, BoxBody)) or (b2 in resolved):
                        continue

                    t = collisions.Polygons(
                        b1.Position,
                        b1.GetTransformedVertices(),
                        b2.Position,
                        b2.GetTransformedVertices(),
                    )

                    if t is not None:
                        b1.Color = (255, 0, 0)
                        b2.Color = (255, 0, 0)

                resolved.append(b1)

        world.Attach(Prerender)

        for idx in range(361):
            drawlib.StoreFrame(world.GenerateFrame(), testlib.FRAMES_PATH, idx)

        movie = JES.makeMovieFromInitialFile(f'{testlib.FRAMES_PATH}/frame000.jpg')
        JES.writeAnimatedGif(movie, f'{testlib.BIN_PATH}/{testlib.GIFName(__file__)}.gif')


if __name__ == '__main__':
    testlib.SoloRunOutput(__file__)
    unittest.main()
