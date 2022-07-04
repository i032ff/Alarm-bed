import sys
import RPi.GPIO as GPIO
import time

# LED制御ピンに、GPIO 23 を使用する
LED_GPIO = 23
# SW制御ピンに、GPIO 24 を使用する
SW_GPIO = 24

# GPIO.BCMを設定することで、GPIO番号で制御出来るようになります。
GPIO.setmode(GPIO.BCM)
# GPIO.OUTを設定することで、出力モードになります。
# 出力モードにすることで電圧を ON/OFF することが出来ます。
GPIO.setup(LED_GPIO, GPIO.OUT)
# GPIO.INを設定することで、入力モードになります。
# pull_up_down=GPIO.PUD_DOWNにすることで、内部プルダウンになります。
GPIO.setup(SW_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
    try:
        # ボタンの値を読み込み
        if GPIO.input(SW_GPIO):
            # LEDを点灯
            GPIO.output(LED_GPIO, GPIO.HIGH)
        else:
            # LEDを消灯
            GPIO.output(LED_GPIO, GPIO.LOW)
        time.sleep(0.5)       # 0.5秒wait
    # Ctrl+Cキーを押すと処理を停止
    except KeyboardInterrupt:
        # ピンの設定を初期化
        # この処理をしないと、次回 プログラムを実行した時に「ピンが使用中」のエラーになります。
        GPIO.cleanup()
        sys.exit()
