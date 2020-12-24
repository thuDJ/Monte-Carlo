import geometry as gm
import simulator as simu
import material as mt
import time


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


if __name__ == '__main__':
    cell1 = gm.Cell(1, -80, 50, 1000, -1000, 1000, -1000)
    cell2 = gm.Cell(2, 50, 80, 1000, -1000, 1000, -1000)
    mat1 = mt.Material(1, 0.7, 0.0092, 0.010)
    mat2 = mt.Material(2, 0.9, 0.002, 0)
    cell_list = [cell1, cell2]
    geo = gm.Geometry(cell_list)
    mat_list = [mat1, mat2]
    mode1 = simu.Mode(10000, 50, 30, False)
    runner = simu.Simulate(geo, mat_list, mode1)

    t1 = time.time()
    runner.run()
    t2 = time.time() - t1
    print_hi(f'succeed, run in {t2} seconds')
