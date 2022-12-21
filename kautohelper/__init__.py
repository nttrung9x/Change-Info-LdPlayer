import subprocess
import cv2
import numpy as np
import time
import pyotp
from . import configuration
import re
import random
import itertools
class AutoADB():
    
    def __init__(self):
        self.config = configuration.Configure()

    def ExecuteCMD(self, cmd):
        return subprocess.run(cmd, shell=True)

    def GetDevices(self):

        cmd = subprocess.Popen(self.config.LIST_DEVICES,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)

        de = str(cmd.stdout.read())
        device_list = []
        array = [de.replace("List of devices attached", "").replace("b'","").replace("\\r","")
                     .replace("\\t"," ").strip("").split("\\n")]

        array = list(itertools.chain.from_iterable(array))
        try:
            array.remove("")
            array.remove("'")
            array.remove('')
        except ValueError:
            pass
        for i in range(len(array)):
            if "offline" not in array[i] and "device" in array[i]:
                device_list.append(array[i].replace("device","").strip())
        return device_list

    def Tap(self, deviceID, x, y):
        return self.ExecuteCMD((self.config.TAP_DEVICES).format(deviceID,x,y))

    def InputText(self, deviceID, text):

        for i in text:
            self.ExecuteCMD((self.config.INPUT_TEXT_DEVICES).format(deviceID,i))
            time.sleep(0.1)

    def ClearPackage(self, deviceID, package):
        return self.ExecuteCMD((self.config.CLEAR_PACKAGE).format(deviceID,package))

    def Swipe(self, deviceID, x1, y1, x2, y2):
        return self.ExecuteCMD((self.config.SWIPE_DEVICES).format(deviceID, x1, y1, x2, y2))

    def Install(self, deviceID, apk):
        return self.ExecuteCMD((self.config.INSTALL_APP).format(deviceID,apk))

    def Uninstall(self, deviceID, apk):
        return self.ExecuteCMD((self.config.UNINSTALL_APP).format(deviceID,apk))

    def Push(self, deviceID, file, location):
        return self.ExecuteCMD((self.config.PUSH_FILE_FROM_DEVICES).format(deviceID, file, location))

    def Pull(self, deviceID, file, location):
        return self.ExecuteCMD((self.config.PULL_FILE_FROM_DEVICES).format(deviceID,file, location))

    def Keyevent(self, deviceID, key):
        return self.ExecuteCMD((self.config.KEY_DEVICES).format(deviceID,key))

    def ScreenShoot(self, deviceID):
        return self.ExecuteCMD("adb -s {0} exec-out screencap -p > screen.png".format(deviceID))

    def FindImage(self, deviceID, image):

        self.ScreenShoot(deviceID)
        img = cv2.imread(image)

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        template = cv2.imread("screen.png", 0)

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        THRESHOLD = 0.9
        loc = np.where(res >= THRESHOLD)

        for y, x in zip(loc[0], loc[1]):
            if x or y:
                return True
        return False

    def ClickImage(self,deviceID,image):

        while True:
            if self.FindImage(deviceID, image) == True:
                img = cv2.imread(image)

                img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                template = cv2.imread("screen.png", 0)
                res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
                THRESHOLD = 0.9
                loc = np.where(res >= THRESHOLD)

                for y,x in zip(loc[0], loc[1]):
                    self.Tap(deviceID,x,y)
                break

    def Get2FA(self, code_2fa):
        to_otp =pyotp.TOTP(code_2fa)
        return to_otp.now()

    def EnableWifi(self, deviceID):
        return self.ExecuteCMD("adb -s {0} shell su -c 'svc wifi enable'".format(deviceID))

    def DisableWifi(self, deviceID):
        return self.ExecuteCMD("adb -s {0} shell su -c 'svc wifi disable'".format(deviceID))

    def Grant(self, deviceID, package, permission):
        return self.ExecuteCMD((self.config.GRANT).format(deviceID, package, permission))

    def OpenPackage(self, deviceD ,package):
        return self.ExecuteCMD((self.config.OPEN_PACKAGE).format(deviceD, package))

    def ChangeProxy(self, deviceID, proxy):
        return self.ExecuteCMD("adb -s {0} shell settings put global http_proxy {1}".format(deviceID,proxy))

    def CheckPackage(self, deviceID, package):
        check = subprocess.check_output("adb -s {0} shell pm list packages".format(deviceID), shell=True)
        pck = re.findall(package, str(check))
        if pck:
            return True
        else:
            return False

    def ClearInput(self, deviceID, n):

        self.Tap(deviceID,83,190)

        self.Keyevent(deviceID, "KEYCODE_MOVE_END")
        for i in range(n):
            time.sleep(0.1)
            self.Keyevent(deviceID,67)