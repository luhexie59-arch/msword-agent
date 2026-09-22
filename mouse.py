import pynput, time
import numpy as np

Button = pynput.mouse.Button
# presets
CURVE_STYLE = [
    [[0., 0.],[-0.1, 0.3],[1., 1.5],[1., 1.]],
    [[0., 0.],[0.2, 1.],[0.8, 1.],[1., 1.]],
    [[0., 0.],[0.2, 0.45],[1.3, 0.95],[1., 1.]],
    [[0., 0.],[0.72, 0.34],[1.18, 0.39],[1., 1.]],
    [[0., 0.],[0.085, 0.24],[0.865, 0.73], [1., 1.]],
    [[0., 0.], [0.4, 0.61], [0.79, 0.97], [1., 1.]]
]

N = 200
T_BASE = np.linspace(0, 1, N).reshape((N, 1))
COEF_MAT = np.hstack((
    np.ones((N, 1)),
    T_BASE,
    T_BASE ** 2,
    T_BASE ** 3
)) @ np.array(
    [[1, 0, 0, 0],
     [-3, 3, 0, 0],
     [3, -6, 3, 0],
     [-1, 3, -3, 1]],
     dtype=np.float64
)


class RealisticMouse(pynput.mouse.Controller):
    def __init__(self, position: tuple[int, int] | None = None):
        super().__init__()
        if position:
            self.position = position


    def real_move(self, dest_x: int, dest_y: int):
        controlPoints = np.array(
            CURVE_STYLE[np.random.randint(len(CURVE_STYLE))],
            dtype=np.float64
        )
        positions = COEF_MAT @ controlPoints

        start_x, start_y = self.position
        dx, dy = dest_x - start_x, dest_y - start_y

        transformed = (np.array([[dx, 0], [0, dy]]) @ positions.T + np.array([[start_x], [start_y]])).T

        for _t, (x, y) in enumerate(transformed.astype(int)):
            self.position = (x, y)
            time.sleep(0.006 * (abs(0.8 / N * _t - 0.4) + 0.8))

    def real_scroll(self, dy: int):
        max_scroll = 8
        duration_each = 0.25
        if dy > 0:
            direction = 1
        else:
            direction = -1
            dy = -dy
        while dy > 0:
            current_scroll = min(dy, max_scroll)
            dy -= current_scroll
            for t in range(current_scroll):
                self.scroll(0, direction)
                time.sleep(duration_each * (abs(0.4 / current_scroll * t - 0.2) + 0.9) / current_scroll)
            time.sleep(0.5)
