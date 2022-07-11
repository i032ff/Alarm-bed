import webiopi

GPIO = webiopi.GPIO

LED1PIN = 23
LED2PIN = 24
LED3PIN = 25

g_led1active = 0
g_led2active = 0
g_led3active = 0
g_speed = 5

def setup():
	GPIO.setFunction( LED1PIN, GPIO.OUT )
	GPIO.setFunction( LED2PIN, GPIO.OUT )
	GPIO.setFunction( LED3PIN, GPIO.OUT )

def loop():
	# speed          |   1    10
	# interval[ sec] |   0.5   0.01
	interval = 0.5 + (g_speed - 1) * (0.01 - 0.5) / (10-1)

	if g_led1active:
		GPIO.digitalWrite( LED1PIN, True )
	if g_led2active:
		GPIO.digitalWrite( LED2PIN, True )
	if g_led3active:
		GPIO.digitalWrite( LED3PIN, True )

	webiopi.sleep( interval )

	GPIO.digitalWrite(LED1PIN, False )
	GPIO.digitalWrite(LED2PIN, False )
	GPIO.digitalWrite(LED3PIN, False )

	webiopi.sleep( interval )

@webiopi.macro
def ChangeLedActive( led, active ):
	global g_led1active, g_led2active, g_led3active
	if 1 == int(led):
		g_led1active = int(active)
	if 2 == int(led):
		g_led2active = int(active)
	if 3 == int(led):
		g_led3active = int(active)

@webiopi.macro
def ChangeSpeed( speed ):
	global g_speed
	g_speed = int(speed)
