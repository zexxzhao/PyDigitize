import sys
from pynput.mouse import Listener, Button
import numpy as np

def get_range(x, y, button, pressed):
    pass

class MouseTracker:
    def __init__(self, x, y, fname):
        self.data_x = x
        self.data_y = y
        self.fname = fname

        self.window_x = []
        self.window_y = []
        self.info = []
        self.counter = 0

    def setup(self, x, y, button, pressed):
        if button == Button.left and pressed:
            self.window_x.append(x)
            self.window_y.append(y)
            self.counter += 1
        if self.counter == 2:
            self.counter = 0
            return False
            
    def extract_position(self, x, y, button, pressed):
        if button == Button.right:
            np.savetxt(self.fname, self.info)
            return False
        if pressed:
            xi = (x - self.window_x[0]) / (self.window_x[1] - self.window_x[0])
            eta = (y - self.window_y[0]) / (self.window_y[1] - self.window_y[0])
            xi = xi * (self.data_x[1] - self.data_x[0]) + self.data_x[0]
            eta = eta * (self.data_y[1] - self.data_y[0]) + self.data_y[0]
            print(f'{self.counter}: [{xi}, {eta}]')
            self.counter += 1
            self.info.append([xi, eta])



def parse_argv(argv):
    argv = argv[1:]
    argc = len(argv)
    if argc != 4  and argc != 6:
        raise RuntimeError(f'Invalid arguments: {argv}')
    pos = [float(argv[0]), float(argv[1]), float(argv[2]), float(argv[3])]
    fname = 'position.dat'
    if argc == 6:
        if argv[4] != '-o':
            raise ValueError(f'Invalid option: {argv[4]}')
        fname = argv[5]
    return pos, fname

def main(argv):
    
    argc = len(argv)
    if any(argv[i].find('help') != -1 for i in range(1, argc)):
        print("""
USAGE:
    click X1 Y1 X2 Y2 [-o FILENAME]

    e.g.
    click 0 0 2.0 1.0 -o data.txt

    [-o FILENAME] is optional. Specify the dst file
""")

    xp, fname = parse_argv(argv)
    tracker = MouseTracker([xp[0], xp[2]], [xp[1], xp[3]], fname)

    # Collect reference point coordinates
    print('Click the reference points', flush=True)
    with Listener(on_click=tracker.setup) as listener:
        listener.join()

    # Collect events until released
    print('Extracting data. Stop by right-clicking.', flush=True)
    with Listener(on_click=tracker.extract_position) as listener:
        listener.join()

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
