import subprocess
import cv2
import numpy as np
import time
import pyotp
from pyzbar.pyzbar import decode
from PIL import Image

class AutoADB():

    def __init__(self, pathLd):

        self.pathLD = pathLd

    def ExecuteLD_Result(self, cmd):
        pathLd = self.pathLD
        text = subprocess.run(pathLd + cmd).returncode
        return text

    def ExecuteCMD(self,index,cmd):
        return self.ExecuteLD_Result(("adb --{0} --command \'{1}\'").format(index,cmd))

