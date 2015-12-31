
# some of th1se need to be installed appart from regular python installation. the urls are here:
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# set up the two curves - these can be changed manually
def function_a(x):     #blue curve - rotated
    y = x**3
    return (y)

def function_b(x):     #red curve - rotator
    y = np.cos(x)
    return (y)

# set up original curves
MIN = -1
MAX = 2
NUM = 500
xvals = np.linspace(MIN, MAX, NUM)

a_yvals = function_a(xvals)
b_yvals = function_b(xvals)


# plot what we have so far and set up for the rest
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot(xvals, a_yvals, "b-", alpha=1.0)
ax.plot(xvals, b_yvals, "r-", alpha=1.0)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')


# take each point on curve B, make perpendicular line to it, find point on curve A 
# that it intersects, draw a circle with this point around B:
for i in range(len(xvals)):

    b_x = xvals[i]
    b_y = b_yvals[i]

    # dont make a circle of radius 0...
    if a_yvals[i] == b_y:
        continue
    
    # get perpendicular slope to reflection point on curve B 
    # use approx of slope 
    if i>=1:
        slope = (b_yvals[i]-b_yvals[i-1])/(xvals[i]-xvals[i-1])
    else:
        slope = (b_yvals[i]-b_yvals[i+1])/(xvals[i]-xvals[i+1])
        
    # perpendicular is neg recip
    slope = slope**(-1)
    slope = -slope
        
    # find approx where perp_line and rotating line intersect
    solutions = []
    # manage very steep lines
    if slope > 100:
        solutions.append(function_a(b_x))
    else:
        perp_line = slope*(xvals - b_x) + b_y
        positive = None
        for i in range(len(xvals)):
            diff = perp_line[i]-a_yvals[i]
            old_positive = positive
            if diff>0:
                positive = True
            elif diff==0:
                solutions.append(x_vals[i])
            else:
                positive = False

            if old_positive != None:
                if old_positive != positive:
                    solutions.append(xvals[i])

    # make a circle for every solution instead of just the first one it finds
    for a_x in solutions:
        if a_x < MIN or a_x > MAX:
            continue
        a_y = function_a(a_x)

        # radius of circle is dist btwn point on line A and point on line B
        delta_x = np.abs(float(b_x-a_x))
        delta_y = np.abs(float(b_y-a_y))
        radius = np.sqrt((delta_x)**2 + (delta_y)**2)


        # make a line segment on xy plane that is circle's diameter
        circle_xs = np.linspace(b_x-delta_x, b_x+delta_x, 100) 
        circle_ys = slope*(circle_xs - b_x) + b_y

        # z points are a function of x and y, make a circle
        circle_zs = []
        for i in range(len(circle_xs)):
            # new magnitude calculation is faster: solve for z in distance formula
            magnitude = np.sqrt(radius**2 - (circle_xs[i]-b_x)**2 - (circle_ys[i]-b_y)**2)

            # bottom and top of circle
            circle_zs.append(magnitude)
            circle_zs.append(-magnitude)

        # double all the points on the x and y axes to account for top and bottom of circle
        circle_xs = np.repeat(circle_xs, 2)
        circle_ys = np.repeat(circle_ys, 2)

        # plot this particular circle and do the next one
        ax.plot(circle_xs, circle_ys, circle_zs, c='g', alpha=.1)
        #ax.scatter(circle_xs, circle_ys, circle_zs, c="g")

### make sure it's not distorted
diff = MAX - MIN + 4    # length of one side of cubic graph
diff = diff/2.0         # half so we can start from midpoint
# determine where the middle of the graph is on the y axis 
a_yvalsMIN = min(a_yvals)
a_yvalsMAX = max(a_yvals)
b_yvalsMIN = min(b_yvals)
b_yvalsMAX = max(b_yvals)
YMAX = max(a_yvalsMIN, b_yvalsMIN)
YMIN = min(a_yvalsMAX, b_yvalsMAX)
ymiddle = YMIN + (YMAX - YMIN)/2.0
# set the axis limits to be a nice cube
ax.set_xlim(MIN - 2, MAX + 2)
ax.set_ylim(ymiddle - diff, ymiddle + diff)
ax.set_zlim(-diff, diff)

# finish
plt.show()