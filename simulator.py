import numpy as np
import random as rd
import threading
import math


class SingSrc:
    def __init__(self, pos, wgt):
        self.pos = pos
        self.wgt = wgt


class Mode:
    def __init__(self, num_ptc=1000, num_tl=50, num_ac=30, no_absorb=False):
        self.num_ptc = num_ptc
        self.num_tl = num_tl
        self.num_ac = num_ac
        self.no_absorb = no_absorb


class Bin:
    def __init__(self, name):
        self.name = name


def get_drt():
    drt = [rd.random() - 0.5 for i in range(3)]
    length = np.sqrt(sum([drt[i] ** 2 for i in range(3)]))
    drt = [drt[i] / length for i in range(3)]
    return drt


class Simulate:
    def __init__(self, geometry, mat_list, mode=Mode()):
        self.model = geometry
        self.mat_list = mat_list
        self.mode = mode
        self.src_bank = []
        self.src_store = []
        self.k_track = 0
        self.k_absorb = 0
        self.total_wgt = 0

    def run(self):
        self.init_source()
        for i in range(self.mode.num_tl - self.mode.num_ac):
            self.start_batch()
            print(f'the {i + 1} inactive-gen K-track is {self.k_track}, K-absorb is {self.k_absorb}')

        for i in range(self.mode.num_ac):
            self.start_count()
            print(f'the {i + 1} active-gen K-track is {self.k_track}, K-absorb is {self.k_absorb}')

    def init_source(self):
        if self.src_bank:
            length = len(self.src_bank)
            src_select = []
            for i in range(self.mode.num_ptc):
                selected = False
                rd1 = rd.randint(1, length)
                while not selected:
                    rd1 = rd.randint(1, length)
                    rd2 = rd.random()
                    if rd2 < self.src_bank[rd1 - 1].wgt:
                        selected = True
                src_select.append(self.src_bank[rd1 - 1])
            self.src_bank = src_select
            self.total_wgt = sum([self.src_bank[i].wgt for i in range(len(self.src_bank))])
        else:
            '''
            初始源分布在 1 1 1 点
            '''
            pos = [1, 1, 1]
            wgt = 1
            for i in range(self.mode.num_ptc):
                self.src_bank.append(SingSrc(pos, wgt))
            self.total_wgt = sum([self.src_bank[i].wgt for i in range(len(self.src_bank))])

    def ray_tracking(self, i):
        src = self.src_bank[i]
        pos = src.pos
        wgt = src.wgt
        drt = get_drt()
        cell = self.model.locate(pos, drt)
        if not cell:
            raise ValueError()
        killed = False
        while not killed:
            dist_bound = cell.distance(pos, drt)
            if dist_bound < 0:
                raise ValueError()
            mat = self.mat_list[cell.mat - 1]
            [co_type, dist_fly] = mat.fly()
            track_length = min(dist_bound, dist_fly)
            pos = [pos[i] + (track_length + 1e-8) * drt[i] for i in range(len(pos))]
            if dist_fly < dist_bound:
                [killed, pos, drt, wgt] = self.proc_cl(co_type, mat, pos, wgt)
            elif dist_bound < dist_fly:
                cell = self.model.neighbor(pos, drt)
                if not cell:
                    killed = True
            self.k_track += track_length * mat.xs_f * wgt
            if wgt < 0.5:
                rd1 = rd.random()
                if rd1 < 0.5:
                    wgt = 1
                else:
                    killed = True

    def proc_cl(self, ct, mat, pos, wgt):
        if not self.mode.no_absorb:
            if ct == 1:
                # 裂变
                self.src_store.append(SingSrc(pos, wgt))
                self.k_absorb = self.k_absorb + 2 * wgt
                return [True, pos, [0, 0, 0], wgt]
            elif ct == 2:
                return [True, pos, [0, 0, 0], wgt]
            elif ct == 3:
                drt = get_drt()
                return [False, pos, drt, wgt]
        else:
            if ct == 1:
                self.src_store.append(SingSrc(pos, wgt))
                self.k_absorb = self.k_absorb + wgt * mat.xs_f / mat.xs_a
                drt = get_drt()
                wgt1 = wgt * mat.xs_s / (mat.xs_a + mat.xs_s)
                return [False, pos, drt, wgt1]
            elif ct == 2:
                drt = get_drt()
                self.k_absorb = self.k_absorb + wgt * mat.xs_f / mat.xs_a
                wgt1 = wgt * mat.xs_s / (mat.xs_a + mat.xs_s)
                return [False, pos, drt, wgt1]
            elif ct == 3:
                drt = get_drt()
                return [False, pos, drt, wgt]

    def start_batch(self):
        self.k_track = 0
        self.k_absorb = 0
        threads = []
        for i in range(10):
            lst1 = []
            for j in range(i*100, (i+1)*100):
                lst1.append(j)
            t = threading.Thread(target=self.para_track, args=(lst1,))
            threads.append(t)

        for i in range(10):
            threads[i].start()
        for i in range(10):
            threads[i].join()

        self.k_track = self.k_track / self.mode.num_ptc
        if not self.mode.no_absorb:
            self.k_absorb = self.k_absorb / self.mode.num_ptc
        else:
            self.k_absorb = self.k_absorb / self.total_wgt
        self.src_bank = self.src_store
        self.src_store = []
        self.init_source()

    def start_count(self):
        self.start_batch()

    def para_track(self, lst):
        for i in lst:
            self.ray_tracking(i)
