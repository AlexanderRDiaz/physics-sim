import drawlib
import JES

from container import Container
from matrix import Vector


world = Container()


def PrerenderWork(container: Container) -> None:
    for body in container.Bodies:
        body.Rotate(3)


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

world.Attach(PrerenderWork)

for idx in range(120):
    drawlib.StoreFrame(world.StepTime(), 'frames', idx)
movie = JES.makeMovieFromInitialFile('frames/frame000.jpg')
JES.writeAnimatedGif(movie, 'test.gif')
