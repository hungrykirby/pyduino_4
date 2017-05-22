import numpy as np
from scipy import signal
from pylab import *
import os

class Arrange:
    past_c = "xx"
    bwn_a = False
    ax = None
    n = np.arange(-0.5, 0.5, 0.01)
    plots_numbers = []
    count = 0
    pattern = {"train": 100, "test":30, "raw": 1000}

    count_calibration = 0
    FRAMES_CALIBRATION = 5
    array_calibration = []
    calibration_numbers = np.array([0, 0, 0]).astype(np.int64)

    def __init__(self, serial, MODE):
        self.ser = serial
        self.MODE = MODE

    def plots(self, x, y, z):
        #figure(figsize=(8, 8))
        #subplot(511)
        clf()
        axis([-1500, 1500, -0.5, 5.5])
        subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.2, hspace=0.5)
        plot(x, 1, 'o')
        plot(y, 3, '*')
        plot(z, 5, 'd')
        pause(0.00001)

    def write_ceps(self, ceps, fn_):
        if MODE == "test" or MODE == "train":
            fn = os.path.join(os.getcwd(), self.MODE, fn_)
            if not os.path.exists(fn):
                os.makedirs(fn)
            #base_fn,ext = os.path.splitext(fn)
            count_str = "00"
            if self.count < 10:
                count_str = "0" + str(self.count)
            else:
                count_str = str(self.count)
            data_fn = os.path.join(self.MODE, fn_, count_str + ".ceps")
            np.save(data_fn,ceps)
            self.count += 1

    def fetch_three_numbers(self, matched_group, is_calibration, c):
        if self.past_c != c:
            self.past_c = c
            self.count = 0
        try:
            if matched_group == "a":
                self.bwn_a = True
                self.plots_numbers = []
            elif self.bwn_a:
                self.plots_numbers.append(int(matched_group))

            if len(self.plots_numbers) == 3:
                pl = self.plots_numbers
                #self.plots(pl[0], pl[1], pl[2])
                self.bwn_a = False
                self.ser.flushInput()
                #print(c, pl)
                if is_calibration:
                    #print("Now Calibration Mode")
                    is_calibration = self.start_calibration(is_calibration, np.array(pl).astype(np.int64))

                if self.count < self.pattern[self.MODE] and c.isdigit():
                    input_array = np.array(pl).astype(np.int64) - self.calibration_numbers
                    if c != "1025":
                        self.write_ceps(input_array, c)
                    print("Calibration Mode is ", is_calibration, ":input array = ", input_array, ":MODE = ", self.MODE)


        except KeyboardInterrupt:
            ser.close()
        return is_calibration

    def start_calibration(self, is_calibration, input_array):
        if self.count_calibration < self.FRAMES_CALIBRATION:
            if is_calibration:
                self.count_calibration += 1
                self.array_calibration.append(input_array)
                #print("count_calibration", self.count_calibration)
        else:
            self.calibration_numbers = np.mean(np.array(self.array_calibration), axis=0)
            is_calibration = False
            self.count_calibration = 0
            self.array_calibration = []
            print("Calibration Finished")
        return is_calibration
