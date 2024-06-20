def servosetup(pwm):
	pwm.set_pwm(0, 0, 300)
	pwm.set_pwm(1, 0, 330)
	pwm.set_pwm(2, 0, 250)
#	pwm.set_pwm(3, 0, 350)
#	pwm.set_pwm(4, 0, 350)


def destra(arduino): # nella nuova versione manda comando sinistra su seriale
    arduino.write(bytes("right\n", "utf-8"))

def sinistra(arduino):
    arduino.write(bytes("left\n", "utf-8"))
