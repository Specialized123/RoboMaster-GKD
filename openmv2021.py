# Hello World Example
#
# Welcome to the OpenMV IDE! Click on the green run arrow button below to run the script!
from pyb import UART
import sensor, image, time, pyb
uart = UART(3, 115200)

sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.VGA)   # Set frame size to QVGA (320x240)
sensor.set_windowing([320, 240])
sensor.set_auto_exposure(False, 800)
sensor.set_auto_whitebal(False, (-5.75, -6, -4.75))  # 若使用滤镜片，则需锁定白平衡增益值
sensor.set_auto_gain(False, 1)
sensor.skip_frames(time = 2000)     # Wait for settings take effect.
clock = time.clock()                # Create a clock object to track the FPS.
led1 = pyb.LED(1)       #red
led2 = pyb.LED(2)       #green
led3 = pyb.LED(3)       #blue

while(True):
    clock.tick()                    # Update the FPS clock.
    img = sensor.snapshot()         # Take a picture and return the image.


    # ---------调试---------------
    #(24, 91, -74, -35, -4, 49)     #test
    #(0, 100, -88, -28, 7, 66)      #real 1
    for blob in img.find_blobs([(24, 91, -74, -35, -4, 49)], pixels_threshold=2, area_threshold=3, merge=True, margin=20):
        led3.on()
        led2.on()       #如果视觉工作，则亮青灯
        img.draw_rectangle(blob.rect())
        output="%03d%03d" % (blob.cx(),blob.cy())
        uart.write("!"+output)
        print(output)
    # ----------------------------
    #print(clock.fps())              # Note: OpenMV Cam runs about half as fast when connected
                                    # to the IDE. The FPS should increase once disconnected.
