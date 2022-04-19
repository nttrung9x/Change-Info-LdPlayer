from ppadb.client import Client as AdbClient
import cv2
import numpy as np
import time

class KautoHelper:
    def __init__(self, host="127.0.0.1", port=5037):

        self.host = host
        self.port = port

    def GetDeviceServer(self, device_num):
        # Default is "127.0.0.1" and 5037

        client = AdbClient(host=self.host, port=self.port)
        devices = client.devices()

        return devices[device_num]

    def GetAdbDevice(self, device_name):

        client = AdbClient(host=self.host, port=self.port)
        device = client.device(device_name)

        return device

    def ListAllDevices(self):

        client = AdbClient(host=self.host, port=self.port)
        devices = client.devices()

        return devices

    def ExecuteCommand(self,device,cmd):
        return device.shell(cmd)

    def ScreenCap(self, device, name):

        result = device.screencap()
        with open(name, "wb") as fp:
            fp.write(result)

    def InstallApp(self,device,apk):
        return device.install(apk)

    def UninstallApp(self,device,package):
        return device.uninstall(package)

    def CheckInstalled(self,device,package):
        return device.is_installed(package)

    def Push(self, device,file, path):
        return device.push(file, path)

    def Pull(self, device, file, path):
        return device.pull(file,path)

    def InputTap(self, device, x, y):
        return device.input_tap(x,y)

    def ClickImage(self, device, index, image):

        self.ScreenCap(device, "screen_{}.png".format(index))
        img = cv2.imread(image)

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        template = cv2.imread("image/screen.png", 0)

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        THRESHOLD = 0.9
        loc = np.where(res >= THRESHOLD)

        for y, x in zip(loc[0], loc[1]):
            return self.InputTap(device,x+6, y+6)

    def ClearPackage(self, device, package):
        cmd = "pm clear " + package
        return self.ExecuteCommand(device,cmd)

    def Grant(self, device, package, permission):
        cmd = "pm grant " + package + permission
        return self.ExecuteCommand(device,cmd)

    def OpenPackage(self, device, package):
        cmd = "monkey -p " + package + " -c android.intent.category.LAUNCHER 1"
        return self.ExecuteCommand(device,cmd)

    def WriteInput(self, device, text, time_write=0.05):

        for i in range(len(text)):
            time.sleep(time_write)
            device.input_text(text[i])

    def ClearInput(self, device, time_to_delete):

        device.shell("input keyevent KEYCODE_MOVE_END")
        for i in range(time_to_delete):
            time.sleep(0.1)
            device.input_keyevent(67)

    def ChangeProxy(self, device, proxy):
        return self.ExecuteCommand(device,"settings put global http_proxy {}".format(proxy))

    def RemoveProxy(self, device):
        return self.ExecuteCommand(device,"settings put global http_proxy :0")

    

