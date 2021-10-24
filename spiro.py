import sys, random, argparse
import numpy
import math
import turtle
import random
from PIL import Image
from datetime import datetime
from fractions import gcd

# draws the Spirograph
class Spiro:
    # constructor
    def __init__(self, xc, yc, col, R, r, l):
        # create turtle object
        self.t = turtle.Turtle()
        # set the cursor shape
        self.t.shape('turtle')
        # set the step in degrees
        self.step = 5
        # set the drawing complete flag
        self.drawingComplete = False

        # set the parameters
        self.setparameters(xc, yc, col, R, r, l)

        # initialize drawing
        self.restart()
    
    # set the parameters
    def setparameters(self, xc, yc, col, R, r, l):
        # set Spirograph Parameters
        self.xc = xc
        self.yc = yc
        self.R = int(R)
        self.r = int(r)
        self.l = l
        self.col = col

        # Reduce r/R to its smallest form by dividing with the GCD(greatest common denom)
        gcdVal = gcd(self.r, self.R)
        self.nRot = self.r//gcdVal
        # get ratio of radii
        self.k = r/float(R)
        # set colour
        self.t.color(*col)
        # save angle
        self.a = 0

    # restart the drawing
    def restart(self):
        # set the flag
        self.drawingComplete = False
        # show turtle
        self.t.showturtle()
        # go to first point
        self.t.up()
        R, k, l = self.R, self.k, self.l
        a = 0.0
        x = R * ((1 - k) * math.cos(a) + l * k * math.cos((1-k) * a / k))
        y = R * ((1 - k) * math.sin(a) - l * k * math.sin((1-k) * a / k))
        self.t.setpos(self.xc + x, self.yc + y)
        self.t.down()

    # Draw the Spirograph
    def draw(self):
        # Draw the outstanding points
        R, k, l = self.R, self.k, self.l
        for i in range(0, 360 * self.nRot + 1, self.step):
            a = math.radians(i)
            x = R * ((1-k) * math.cos(a) + l * k * math.cos((1-k) * a / k))
            y = R * ((1-k) * math.sin(a) - l * k * math.sin((1-k) * a / k))
            self.t.setpos(self.xc + x, self.yc + y)
        
        # Hide turtle when drawing is done
        self.t.hideturtle()

    # Update by a single step
    def update(self):
        # skip the other steps if drawing is complete
        if self.drawingComplete:
            return
        # increment the angle
        self.a += self.step
        # draw the step
        R, k, l = self.R, self.k, self.l
        # set the angle
        a = math.radians(self.a)
        x = R * ((1-k) * math.cos(a) + l * k * math.cos((1-k) * a / k))
        y = R * ((1-k) * math.sin(a) - l * k * math.sin((1-k) * a / k))
        self.t.setpos(self.xc + x, self.yc + y)
        # if drawing is complete set flag for it
        if self.a >= 360 * self.nRot:
            self.drawingComplete = True
            # drawing is now done so hide turtle
            self.t.hideturtle()

    # clear everything
    def clear(self):
        self.t.clear()


# Animates the Spirograph
class SpiroAnimator:
    # constructor
    def __init__(self, N):
        # set time value (MS)
        self.deltaT = 10
        # get the window dimensions
        self.width = turtle.window_width()
        self.height = turtle.window_height()
        #create the spiro objects
        self.spiros = []
        for i in range(N):
            # generate random params
            rparams = self.genRandomParameters()
            # set the params for the Spiro
            spiro = Spiro(*rparams)
            self.spiros.append(spiro)
        # call timer
        turtle.ontimer(self.update, self.deltaT)

    # restart spiro drawing
    def restart(self):
        for spiro in self.spiros:
            # clear
            spiro.clear()
            # generate random parameters
            rparams = self.genRandomParameters()
            # set the spiro parameters
            spiro.setparameters(*rparams)
            # restart drawing
            spiro.restart()

    # generate random parameters
    def genRandomParameters(self):
        width, height = self.width, self.height
        R = random.randint(50, min(width, height) // 2)
        r = random.randint(10, 9*R//10)
        l = random.uniform(0.1, 0.9)
        xc = random.randint(-width//2, width//2)
        yc = random.randint(-height//2, height//2)
        col = (random.random(), random.random(), random.random())
        return (xc, yc, col, R, r, l)

    def update(self):
        # update all spiros
        nComplete = 0
        for spiro in self.spiros:
            # update
            spiro.update()
            # count number of completed spiros
            if spiro.drawingComplete:
                nComplete += 1
        
        # restart if all spiros are complete
        if nComplete == len(self.spiros):
            self.restart()
        # call the timer
        turtle.ontimer(self.update, self.deltaT)

    # toggle turtle cursor on and off
    def toggleTurtles(self):
        for spiro in self.spiros:
            if spiro.t.isvisible():
                spiro.t.hideturtle()
            else:
                spiro.t.showturtle()

# save drawings as PNG files
def saveDrawing():
    # hide turtle
    turtle.hideturtle()
    # gen filename
    dateStr = (datetime.now()).strftime("%d%b%Y - %H%M%S")
    fileName = 'spiro-' + dateStr
    print("Saving drawing to %s.eps/png" % fileName)
    # Get the tkinter canvas
    canvas = turtle.getcanvas()
    # save the drawing as a postscript image
    canvas.postscript(file = fileName + ".eps")
    # Use pillow module to convert to PNG
    img = Image.open(fileName + ".eps")
    img.save(fileName + ".png", "png")
    # show the turtle cursor
    turtle.turtle.showturtle()

def main():
    print("Generating Spirograph...")
    # argument parser
    descriptionString = """This program draws Spirographs. When run with no arguments, this program draws random Spirographs.
    
    Terminology:

    R: radius of outer circle
    r: radius of inner circle
    l: ratio of hole distance to r
    """

    parser = argparse.ArgumentParser(description=descriptionString)

    # expected arguments
    parser.add_argument("--sparams", nargs=3, dest="sparams", required=False, help="Arguments in sparams: R, r, l")
    # parse the arguments
    args = parser.parse_args()

    # set with of drawing window to 80% of screen width
    turtle.setup(width=0.8)

    turtle.shape("turtle")

    # set window title
    turtle.title("Spirographs!")
    # add key handler to save drawwings
    turtle.onkey(saveDrawing, "s")
    # start listening
    turtle.listen()

    turtle.hideturtle()

    # check for any args and then draw the Spirogrph
    if args.sparams:
        params = [float(x) for x in args.sparams]
        # draw the spirograph with the set parameters
        col = (0.0, 0.0, 0.0)
        spiro = Spiro(0, 0, col, *params)
        spiro.draw()
    else:
        # create animator object
        spiroAnim = SpiroAnimator(4)
        # Add key handler to toggle turtle
        turtle.onkey(spiroAnim.toggleTurtles, "t")
        # Add key handler to restart animation
        turtle.onkey(spiroAnim.restart, "space")

    # Start the main turtle loop
    turtle.mainloop()

if __name__ == "__main__":
    main()
