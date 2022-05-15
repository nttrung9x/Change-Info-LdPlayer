import subprocess
import cv2
import numpy as np
import time
import pyotp
from pyzbar.pyzbar import decode
from PIL import Image
import configuration
import re
class AutoADB():
    
    def __init__(self, ADB_PATH):
        self.config = configuration.Configure(ADB_PATH)


    def ExecuteCMD(self, cmd):

        output = subprocess.run(cmd, shell=True).returncode
        if output:
            return output

    def GetDevices(self):

        de = str(subprocess.check_output(self.config.LIST_DEVICES, shell=True))
        matchCollection = re.findall("emulator-\d\d\d\d", de)
        return matchCollection

    def Tap(self, deviceID, x, y):
        return self.ExecuteCMD((self.config.TAP_DEVICES).format(deviceID,x,y))

    def Key(self, deviceID, key):
        return self.ExecuteCMD((self.config.KEY_DEVICES).format(deviceID, key))

    def InputText(self, deviceID, text):

        for i in text:
            self.ExecuteCMD((self.config.INPUT_TEXT_DEVICES).format(deviceID,i))
            time.sleep(0.2)

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

    def ScreenShoot(self, deviceID, file="/sdcard/screenShoot.png"):

        self.ExecuteCMD((self.config.CAPTURE_SCREEN_TO_DEVICES).format(deviceID))
        self.Pull(deviceID,file,"")

    def FindImage(self, deviceID, image):

        self.ScreenShoot(deviceID)
        img = cv2.imread(image)

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        template = cv2.imread("screenShoot.png", 0)

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        THRESHOLD = 0.9
        loc = np.where(res >= THRESHOLD)

        for y, x in zip(loc[0], loc[1]):
            if x or y:
                return True
        return False

    def ClickImage(self, deviceID, image):

        self.ScreenShoot(deviceID)
        img = cv2.imread(image)

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        template = cv2.imread("screenShoot.png", 0)

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        THRESHOLD = 0.9
        loc = np.where(res >= THRESHOLD)

        for y, x in zip(loc[0], loc[1]):
            return self.Tap(deviceID, x+6, y+6)

    def Get2FA(self, code_2fa=None):
        if code_2fa:
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
