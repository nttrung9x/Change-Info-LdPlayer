from kautohelper import AutoADB
from ldhelper import LdHelper
from otphelper import OTPHelper, ProxyHelper
import time
import random

dir = "data/"
ho = dir + "name/ho.txt"
ten = dir + "name/ten.txt"

def name():
    name, mid = '',''
    file_1 = open(ho, "r", encoding="utf8").readlines()
    file_1 = file_1[random.randint(0,1375)]
    for i in range(len(file_1)):
        if file_1[i] == ' ':
            name = file_1[:i]
            mid = file_1[i+1:]
    return name,mid

def RegClone(deviceID,i,api):

    file_2 = open(ten, "r", encoding="utf8").readlines()

    auto_helper = AutoADB()
    ld_helper = LdHelper(r'C:\LDPlayer\LDPlayer4.0')
    otp_helper = OTPHelper
    proxy_helper = ProxyHelper()

    #Open LDPlayer
    print("Đang mở LdPlayer")
    ld_helper.StartNewLD("LDPlayer-{0}".format(i))

    #Connect to LdPlayer
    print("Đang kết nối LD")
    while True:
        time.sleep(5)
        if ld_helper.CheckLD(deviceID) == True:
            print("Đã kết nối thành công")
            break
        continue

    #Change proxy
    print("Đang thay đổi proxy")
    proxy = proxy_helper.GetNewProxyTM(api)
    if not proxy:
        proxy = proxy_helper.GetCurrentProxyTM(api)

    auto_helper.ChangeProxy(deviceID,proxy)

    #Uninstall/Install Facebooklite
    print("Đang xóa Facebooklite")
    auto_helper.Uninstall(deviceID,"com.facebook.lite")
    print("Đang cài Facebooklite")
    auto_helper.Install(deviceID,'apps/facebook.apk')

    #Delete Facebooklite Cache
    print("Đang xóa dữ liệu")
    auto_helper.ClearPackage(deviceID,"com.facebook.lite")

    #Allow some privacy
    print("Đang cho phép các quyền")
    auto_helper.Grant(deviceID,"com.facebook.lite", "android.permission.READ_CONTACTS")
    auto_helper.Grant(deviceID,"com.facebook.lite", "android.permission.CALL_PHONE")
    auto_helper.Grant(deviceID,"com.facebook.lite", "android.permission.CAMERA")
    auto_helper.Grant(deviceID,"com.facebook.lite", "android.permission.ACCESS_FINE_LOCATION")
    auto_helper.Grant(deviceID,"com.facebook.lite", "android.permission.READ_EXTERNAL_STORAGE")

    #Open Facebook
    print("Đang mở Facebooklite")
    auto_helper.OpenPackage(deviceID, "com.facebook.lite")

    #Press create
    if auto_helper.FindImage(deviceID,"image/create.PNG"):
        time.sleep(random.randint(0,2))
        auto_helper.ClickImage(deviceID,"image/create.PNG")

    #Press next
    if auto_helper.FindImage(deviceID,"image/next.PNG"):
        time.sleep(random.randint(0,2))
        auto_helper.ClickImage(deviceID,"image/next.PNG")

    #Write name
    sir,mid = name()
    print("Đang nhập họ và tên")
    time.sleep(random.randint(0,2))
    auto_helper.InputText(deviceID,sir)

    time.sleep(1)
    auto_helper.Keyevent(deviceID, 61)
    time.sleep(0.5)
    auto_helper.InputText(deviceID,mid)
    auto_helper.Keyevent(deviceID,62)
    time.sleep(0.5)
    last_n = file_2[random.randint(0,212)]
    auto_helper.InputText(deviceID,last_n)
    time.sleep(random.randint(0,2))
    auto_helper.ClickImage(deviceID, "image/next.PNG")

    #Write birth
    time.sleep(random.randint(0,2))


    #Write gender
    time.sleep(random.randint(0,2))


RegClone("127.0.0.1:5557",1, "")

