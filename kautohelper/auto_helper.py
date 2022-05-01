import subprocess
import cv2
import numpy as np
import time
import pyotp
from pyzbar.pyzbar import decode
from PIL import Image
import re
class AutoADB():

    def GetDevices(self):

        devices = []
        de = str(subprocess.check_output("adb devices"))
        matchCollection = re.findall("\Semulator-\d\d\d\d", de)
        return matchCollection


auto = AutoADB()
print(auto.GetDevices())