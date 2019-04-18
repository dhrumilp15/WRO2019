#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_C, OUTPUT_B, OUTPUT_D, OUTPUT_A, SpeedDPS, MoveTank, MoveSteering, SpeedPercent, SpeedDPS
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import LightSensor, ColorSensor
from ev3dev2.button import Button
from time import sleep
import sys, os

"""
CHANGE
- Light sensor bounds
- Tune PID
- Tune Turning
"""
class run2019:
    def __init__(self):
        self.btn=Button()
        self.LLight = LightSensor(INPUT_1)
        self.RLight = LightSensor(INPUT_4)
        self.cs = ColorSensor()

        self.drive = MoveTank(OUTPUT_A,OUTPUT_D)
        self.steer = MoveSteering(OUTPUT_A,OUTPUT_D)
        self.heightmotor = LargeMotor(OUTPUT_B)
        self.clawactuator = MediumMotor(OUTPUT_C)

        os.system('setfont Lat15-TerminusBold14')

        self.speed = 40
        self.sectionCache = 0
        self.orient = {'N': "1",
                'E': "1",
                'S': "1",
                'W': "1"}

    def sensordata(self):
            print("Left Light Sensor: ", end = "", file = sys.stderr)
            print(self.LLight.reflected_light_intensity, end = " ", file = sys.stderr)
            print("Right Light Sensor: ", end = "", file = sys.stderr)
            print(self.RLight.reflected_light_intensity, file = sys.stderr)

    def turn(self, direc): # Half - works
        self.drive.on_for_degrees(SpeedDPS(225),SpeedDPS(225),223)
        if direc == "L" or direc == "l":
            self.steer.on_for_degrees(steering=-100, speed=SpeedDPS(720), degrees=400)
        elif direc == "R" or direc == "r":
            self.steer.on_for_degrees(steering=100, speed=SpeedDPS(720), degrees=720)
        self.steer.off()

    def dti(self, speed, n, startCounting=False, sectionCache=0): # Drive to nth intersection
        kp = 1.1
        ki = 0
        kd = 0
        integral = 0
        perror = error = 0
        inters = 0
        piderror = 0
        while not self.btn.any(): # Remember to try stuff twice, this is a keyboard interrupt
            lv = self.LLight.reflected_light_intensity
            rv = self.RLight.reflected_light_intensity
            error = rv - lv
            integral += integral + error
            derivative = lv - perror

            piderror = (error * kp) + (integral * ki) + (derivative * kd)
            if speed + abs(piderror) > 100:
                if piderror >= 0:
                    piderror = 100 - speed
                else:
                    piderror = speed - 100
            self.drive.on(left_speed = speed - piderror, right_speed= speed + piderror)
            sleep(0.01)
            perror = error

            # Drive up to nth intersection
            # These values are subject to change depending on outside factors, CHANGE ON COMPETITION DAY
            if (lv <= 50 and rv <= 55) or (lv <= 50 and rv >= 55) or (lv >= 50 and rv <= 55): # Currently at an intersection
                inters += 1
                if (startCounting == True):
                    sectionCache += 1
                if inters == n: # Currently at nth intersection
                    self.drive.off()
                    return
                self.drive.off()
                self.drive.on_for_seconds(SpeedDPS(115), SpeedDPS(115), 1)

            print("Left Value: {}, Right Value: {}, P error: {}, Inters: {}".format(lv, rv, piderror, inters), file=sys.stderr)

    def assigncolours(self, speed): # Does beginning, up to first intersection
        kp = 1
        ki = 0
        kd = 0
        integral = 0
        perror = error = 0
        piderror = 0
        while not self.btn.any(): # Remember to try stuff twice, this is a keyboard interrupt
            lv = self.LLight.reflected_light_intensity
            rv = self.RLight.reflected_light_intensity
            error = rv - lv
            integral += integral + error
            derivative = lv - perror

            piderror = (error * kp) + (integral * ki) + (derivative * kd)
            if speed + abs(piderror) > 100:
                if piderror >= 0:
                    piderror = 100 - speed
                else:
                    piderror = speed - 100
            self.drive.on(left_speed = speed - piderror, right_speed= speed + piderror)
            sleep(0.01)
            perror = error
            print(self.cs.color, file = sys.stderr)

            if self.cs.color != self.cs.COLOR_NOCOLOR and self.cs.color in [self.cs.COLOR_RED, self.cs.COLOR_GREEN, self.cs.COLOR_YELLOW, self.cs.COLOR_BLUE]:
                if self.orient["E"] == "1":
                    self.orient["E"] = self.cs.color
                    eastcolour = self.cs.color
                    while self.cs.color == eastcolour:
                        self.drive.on(10,10)
                else:
                    if self.orient["S"] == "1":
                        self.orient["S"] = self.cs.color
                        self.drive.on_for_degrees(speed, speed, degrees=40)
                        southcolour = self.cs.color
                        while self.cs.color == southcolour:
                            self.drive.on(10,10)
                    else:
                        if self.orient["W"] == "1":
                            self.orient["W"] = self.cs.color
                            self.drive.on_for_degrees(speed, speed, degrees=40)
                            westcolour = self.cs.color
                            while self.cs.color == westcolour:
                                self.drive.on(10,10)
                        else:
                            if self.orient["N"] == "1":
                                self.orient["N"] = self.cs.color
                                self.drive.on_for_degrees(speed, speed, degrees=40)
                                northcolour = self.cs.color
                                while self.cs.color == northcolour:
                                    self.drive.on(10,10)
            if lv <= 50 and rv >= 55:
                self.drive.off()
                return

    def wirePick(self, speed):
        self.dti(speed, 6)
        self.turn('L')
        self.dti(speed, 1)
        self.turn('R')
        self.drive.on_for_degrees(self.speed, self.speed, degrees = 300)
        self.heightmotor.off()
        self.clawactuator.on()
        self.drive.on_for_degrees(-self.speed, -self.speed, degrees = 360)
        self.turn('R')
        self.dti(speed, 1)
        self.turn("r")
        self.dti(speed,1)
        self.turn('r')
        self.dti(speed,2)
        self.turn('l')
        self.drive.on_for_degrees(self.speed, self.speed, degrees=300)
        self.heighmotor.on()
        self.clawactuator.off()
        self.drive.on_for_degrees(-self.speed, -self.speed, degrees=300)
        self.turn("l")
        self.dti(speed, 2)
        self.turn("r")
        self.dti(speed, 5)
        self.turn("r")
        self.dti(speed, 1)
        self.drive.on_for_degrees(self.speed, self.speed, degrees=300)

    def ballDrop(self, speed):
        self.dti(speed,3)
        self.turn('L')
        self.heightmotor.on_for_degrees(speed=30, degrees=-20)
        self.drive.on_for_degrees(self.speed, self.speed, degrees = 360)
        self.drive.off()
        self.turn('L')
        self.turn('r')
        self.drive.on_for_degrees(-self.speed, -self.speed, degrees = 360)
        self.turn('r')


    def goToDrop (self, color):
        if (self.sectionCache > 1 and self.sectionCache <3 or self.sectionCache>3):
            if(color == 'r' or color == 'R'):
                self.steer.on_for_degrees(steering=-100, speed = SpeedDPS(720), degrees=720) # Figure out 180 turn
                self.dti(self.speed, self.sectionCache - 1)
                self.drive.off()
                self.turn('R')
                self.drive.on_for_degrees(self.speed, self.speed, degrees = 180)
        elif (self.sectionCache == 1 or self.sectionCache == 3):
                self.steer.on_for_degrees(steering=-100, speed = SpeedDPS(720), degrees=720) # Figure out 180 turn
                self.drive.on_for_degrees(self.speed, self.speed, degrees=180)

    def returnToSender (self, speed):
        self.steer.on_for_degrees(steering=-100, speed = SpeedDPS(720), degrees=720) # Figure out 180 turn
        self.drive.on_for_degrees(speed, speed, degrees=180)
        self.dti(self.speed, self.sectionCache - 1)

    def pid(self, speed):
        lv = self.LLight.reflected_light_intensity
        rv = self.RLight.reflected_light_intensity
        kp = 1
        ki = 0
        kd = 0
        integral = 0
        perror = error = 0
        piderror = 0
        while not self.btn.any(): # Remember to try stuff twice, this is a keyboard interrupt
            lv = self.LLight.reflected_light_intensity
            rv = self.RLight.reflected_light_intensity
            error = rv - lv
            integral += integral + error
            derivative = lv - perror

            piderror = (error * kp) + (integral * ki) + (derivative * kd)
            if speed + abs(piderror) > 100:
                if piderror >= 0:
                    piderror = 100 - speed
                else:
                    piderror = speed - 100
            self.drive.on(left_speed = speed - piderror, right_speed= speed + piderror)
            sleep(0.01)
            perror = error

    def firstbnp(self, speed):
        lv = self.LLight.reflected_light_intensity
        rv = self.RLight.reflected_light_intensity
        kp = 1
        ki = 0
        kd = 0
        integral = 0
        perror = error = 0
        piderror = 0
        while not self.btn.any(): # Remember to try stuff twice, this is a keyboard interrupt
            lv = self.LLight.reflected_light_intensity
            rv = self.RLight.reflected_light_intensity
            error = rv - lv
            integral += integral + error
            derivative = lv - perror

            piderror = (error * kp) + (integral * ki) + (derivative * kd)
            if speed + abs(piderror) > 100:
                if piderror >= 0:
                    piderror = 100 - speed
                else:
                    piderror = speed - 100
            self.drive.on(left_speed = speed - piderror, right_speed= speed + piderror)
            sleep(0.01)
            perror = error
            if self.cs.color == self.cs.COLOR_BLACK:
                self.drive.off()
                self.steer.on_for_degrees(steering=100, speed = SpeedDPS(336), degrees=500)
                # self.drive.on_for_degrees(SpeedDPS(360), SpeedDPS(360), 100) # Overshoot
                # self.heightmotor.on_for_degrees(speed=30, degrees=-20)
                # self.drive.on_for_degrees(20,20,-30)
                # self.clawactuator.on(speed=30)
                # self.heightmotor.on_for_degrees(speed=30, degrees = 20)
                # self.steer.on_for_degrees(steering=-100, speed = SpeedDPS(720), degrees=720) # Figure out 180 turn
                # self.dti(speed, 1) # ASSUME: ROBOT IS GOING STRAIGHT
                # self.pidtocolour(speed)
                # self.drive.on_for_degrees(speed, speed, degrees=180)

                # self.goToDrop("r")
                # self.clawactuator.off()
                # self.heightmotor.on_for_degrees(speed,degrees=-50)
                # self.clawactuator.on(-speed)
                # self.clawactuator.wait_until_not_moving()
                # self.returnToSender(30)


    def main(self):
        self.heightmotor.on(speed=self.speed)
        self.heightmotor.wait_until_not_moving()
        # # while not btn.any():
        # #     sensordata()
        # # ## STORING COLOURS
        self.drive.on_for_degrees(left_speed=self.speed, right_speed=self.speed, degrees=50) # To drive past little initial intersection
        self.assigncolours(self.speed)
        print(self.orient, file = sys.stderr) #DEBUG
        self.turn("L")
        # # # GO TO FIRST BNPs
        self.dti(self.speed, 5, startCounting=True)
        self.turn("L")
        self.dti(self.speed, 1)
        self.firstbnp(self.speed)
        # while not self.btn.any():
        #     print(self.cs.color)
        #     print(self.cs.color, file=sys.stderr)

runner = run2019()
runner.main()

"""
Placed directly in front of top front line
dti
Drive by up to first intersection, store coloured bricks into orientation list
turn left
drive to 5th intersection (4 intersections have passed)
turn left
drive up and slightly past first intersection (cs is on half-line of robot)
Is np black?
    Y:
        Back up until at intersection
        Turn right
        Drive forward and overshoot position
        Pick up bnp
        Full 180
        Drive past intersection to red zone to place
        Orient claw in red position
        Drop bnp
        Back up
        Reorient Claw to accept a new bnp
Similar process for blue part
.
. Place first two BNP in position (with center point at mid of np)
.
Full 180
Drive to intersection
turn left
drive to intersection
turn right
dti
turn right
drive to "second" intersection
.
. Place last two BNP in positions (with center point at mid of np)
.
full 180
dti
turn left
drive up to 4th intersection
turn left
dti
turn right
Reset claw to forward-facing
Overshoot and pick up FIBER OPTIC CABLE
full 180
dti
turn left
dti
turn right
dti
turn right
drive to second intersection
turn left
drive up to when can't see balck / hardcode
hardcode distance to position to deposit FIBER OPTIC CABLE
reverse
get back on line (rotating until sees line, etc.)
dti
turn left
drive to 2nd intersection ( 1 intersection passed)
turn right
dti
turn right
dti
turn left
reset claw to forward facing
overshoot and pick up FIBER OPTIC CABLE
full 180
dti
turn right
dti
turn left
drive to 5th intersection ( 4 intersections passed)
turn left
drive to second intersection (1 intersection passed)
turn left
drive up to when can't see balck / hardcode
hardcode distance to position to deposit FIBER OPTIC CABLE
reverse
get back on line (rotating until sees line, etc.)
dti
turn right
drive to second intersection (1 intersection passed)
turn left
drive hardcode to finish
"""
