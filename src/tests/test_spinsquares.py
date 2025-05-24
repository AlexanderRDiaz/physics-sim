from __future__ import annotations

import os
import shutil
import unittest

from src import JES, drawlib
from src.container import Container
from src.matrix import Vector


FRAMES_PATH = 'src/test/bin/frames'


class Main(unittest.TestCase):
    def setUp(self: Main):
        if os.path.exists(FRAMES_PATH):
            shutil.rmtree(FRAMES_PATH)

        os.makedirs(FRAMES_PATH)

    def tearDown(self: Main):
        if os.path.exists(FRAMES_PATH):
            shutil.rmtree(FRAMES_PATH)

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

        for idx in range(120):
            drawlib.StoreFrame(world.StepTime(), FRAMES_PATH, idx)

        movie = JES.makeMovieFromInitialFile(f'{FRAMES_PATH}/frame000.jpg')
        JES.writeAnimatedGif(movie, f'src/bin/{__name__}.gif')


if __name__ == '__main__':
    unittest.main()
