class Border:
    def __init__(self, x, y, z, n):
        self.type = 1
        self.var = [x, y, z, n]


class Cell:
    def __init__(self, mat, x1, x2, y1, y2, z1, z2):
        self.mat = mat
        self.x_left = x1
        self.x_right = x2
        self.y_fr = y1
        self.y_back = y2
        self.z_up = z1
        self.z_bt = z2

    def in_cell(self, pos):
        x = pos[0]
        y = pos[1]
        z = pos[2]
        if self.x_right > x > self.x_left and self.y_fr > y > self.y_back and self.z_up > z > self.z_bt:
            return True
        else:
            return False

    def distance(self, pos, drt):
        if drt[0] > 0:
            dst1 = (self.x_right - pos[0])/abs(drt[0])
        else:
            dst1 = -(self.x_left - pos[0])/abs(drt[0])
        if drt[1] > 0:
            dst2 = (self.y_fr - pos[1])/abs(drt[1])
        else:
            dst2 = -(self.y_back - pos[1])/abs(drt[1])
        if drt[2] > 0:
            dst3 = (self.z_up - pos[2])/abs(drt[2])
        else:
            dst3 = -(self.z_bt - pos[2])/abs(drt[2])

        return min(dst1, dst2, dst3)


class Geometry:
    def __init__(self, cell_list):
        self.cells = cell_list

    def locate(self, pos, drt):
        pos = [pos[i] + 1e-8 * drt[i] for i in range(len(pos))]
        for cell in self.cells:
            if cell.in_cell(pos):
                return cell
        return False

    def distance(self, pos, drt, cell_id):
        return self.cells[cell_id].distance(pos, drt)

    def neighbor(self, pos, drt):
        pos = [pos[i] + 1e-8 * drt[i] for i in range(len(pos))]
        return self.locate(pos, drt)
