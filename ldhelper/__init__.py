import subprocess
import random
import json


class LdHelper:

    def __init__(self, pathLd):
        self.pathLD = pathLd + "\ldconsole.exe "

    def CreateRandomNumber(self, index):

        random_num = ''
        for i in range(index):
            random_num += str(random.randint(0,9))
        return random_num

    def ExecuteCMD(self, cmd):
        return subprocess.call(cmd, shell=True)

    def CheckLD(self, deviceID):

        output = self.ExecuteCMD("adb -s {0} shell input tap 1 1".format(deviceID))
        if output:
            return False
        return True

    def CloseAllLD(self):
        return subprocess.call(self.pathLD + 'quitall', shell=True)

    def OpenLD(self, index=None, name=None):
        if index:
            subprocess.call(self.pathLD +  "launch --index {0}".format(index),shell=True)
        if name:
            subprocess.call(self.pathLD +  "launch --name {0}".format(name),shell=True)

    def KillPackage(self, index, package):
        return subprocess.call(self.pathLD + "killapp --index {0} --packagename {1}".format(index,package), shell=True)

    def CreateLD(self,name):
        return subprocess.call(self.pathLD + ('add --name {0}').format(name), shell=True)

    def Modify(self, setting, index):
        return subprocess.call(self.pathLD + "modify --index {0} {1}".format(index,setting), shell=True)

    def RemoveLD(self,name):
        return subprocess.call(self.pathLD + ('remove --name {}').format(name), shell=True)

    def Copy(self, name, index):
        return subprocess.call("copy --name {0} --from {1}".format(name, index), shell=True)

    def ChangeInfoLD(self, name):

        text2 = "86516602" + self.CreateRandomNumber(7)
        text3 = "46000" + self.CreateRandomNumber(10)
        text4 = "898600" + self.CreateRandomNumber(14)

        jtoken = json.load(open("deviceinfo.json","r"))
        device_manu = random.randint(0,3)
        jtoken2 = jtoken[device_manu]
        device_model = random.randint(0, len(jtoken2['models'])-1)
        manufactures = jtoken2['manufacturer']
        models = jtoken2['models'][device_model]
        pnum =  '09' + self.CreateRandomNumber(8)

        subprocess.call(self.pathLD + ('modify --name {0} --resolution 320,480,120 --cpu 1 --memory 1024').format(name))
        subprocess.call(self.pathLD + ('modify --name {0} --pnumber {1} --manufacturer {2} --model "{3}"').format(name, pnum, manufactures, models))
        subprocess.call(self.pathLD + ("modify --name {0} --imei {1} --imsi {2} --simserial {3}").format(name,text2,text3,text4))


    def StartNewLD(self, name):

        self.CreateLD(name)
        self.ChangeInfoLD(name)
        self.OpenLD(name=name)

ldhelper = LdHelper(r'C:\LDPlayer\LDPlayer4.0')
ldhelper.StartNewLD('ld0')
