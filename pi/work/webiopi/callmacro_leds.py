import webiopi
import datetime
 
GPIO = webiopi.GPIO
 
LIGHT = 4    # GPIO4
HOUR_ON = datetime.time(8,0)     # 自動消灯時間 8:00
HOUR_OFF = datetime.time(18,0)     # 自動消灯時間 8:00
 
def setup():
    # GPIO4をOUTに設定
    GPIO.setFunction(LIGHT, GPIO.OUT)
    # 現在時刻を取得
    now = datetime.time(datetime.datetime.now().hour, datetime.datetime.now().minute)
 
    # 現在時刻と自動点灯・消灯時間の比較
    if ((now >= HOUR_ON ) and (now <= HOUR_OFF)):
        GPIO.digitalWrite(LIGHT, GPIO.HIGH)
 
def loop():
    # 現在時刻を取得
    now = datetime.time(datetime.datetime.now().hour, datetime.datetime.now().minute)
 
    # 自動点灯
    if ((now.hour == HOUR_ON.hour) and (now.minute == HOUR_ON.minute) and (now.second == 0)):
        if (GPIO.digitalRead(LIGHT) == GPIO.LOW):
            GPIO.digitalWrite(LIGHT, GPIO.HIGH)
 
    # 自動消灯
    if ((now.hour == HOUR_OFF.hour) and (now.minute == HOUR_OFF.minute) and (now.second == 0)):
        if (GPIO.digitalRead(LIGHT) == GPIO.HIGH):
            GPIO.digitalWrite(LIGHT, GPIO.LOW)
 
    # 1秒間隔で繰り返し
    webiopi.sleep(1)
 
def destroy():
    # 消灯
    GPIO.digitalWrite(LIGHT, GPIO.LOW)
 
@webiopi.macro
def getLightHours():
    return "%s;%s" % (HOUR_ON.strftime("%H:%M"),HOUR_OFF.strftime("%H:%M"))
 
@webiopi.macro
def setLightHours(on, off):
    global HOUR_ON, HOUR_OFF
    # 引数を分割
    array_on  = on.split(":")
    array_off = off.split(":")
    # 値の設定
    HOUR_ON  = datetime.time(int(array_on[0]),int(array_on[1]))
    HOUR_OFF = datetime.time(int(array_off[0]),int(array_off[1]))
    return getLightHours()
