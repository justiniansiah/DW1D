#Libraries
import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 27
GPIO_ECHO = 22
GPIO_Red = 20      #Red LED
GPIO_Green = 21     #Green LED
GPIO_SERVO = 16     #dispenser motor

 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_Red, GPIO.OUT)
GPIO.setup(GPIO_Green, GPIO.OUT)
GPIO.setup(GPIO_SERVO, GPIO.OUT)
GPIO.setwarnings(False)
pwm = GPIO.PWM(GPIO_SERVO, 1000)

 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
#    start=time.time()
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
#        if time.time()-start>0.01:
#            StartTime = time.time()
#            break
 
    # save time of arrival
#    start=time.time()
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
#        if time.time()-start>0.01:
#            StopTime = StartTime + 0.005
#            break

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    return distance
 
def dispense():        #Distance = distance read from sonar, inp = dispense command
    GPIO.output(GPIO_Red, GPIO.LOW)     #Red LED Turns off
    pwm.start(99)     #complete revolutions at fixed speed for 3 secs
    GPIO.output(GPIO_Green, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(GPIO_Green, GPIO.LOW)
    pwm.stop()

def clearLEDs():    #Cleans up the pins if exits prematurely
    GPIO.output(GPIO_Red, GPIO.LOW)
    GPIO.output(GPIO_Green, GPIO.LOW)
    pwm.stop()


#if __name__ == '__main__':
#    try:
#        while True:
#            dist = distance()
#            print ("Measured Distance = %.1f cm" % dist)
#            Dispenser(dist)
#            time.sleep(1)
# 
#        # Reset by pressing CTRL + C
#    except KeyboardInterrupt:
#        print("Measurement stopped by User")
#        GPIO.cleanup()