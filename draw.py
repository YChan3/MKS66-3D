from display import *
from matrix import *

  # ====================
  # add the points for a rectagular prism whose
  # upper-left corner is (x, y, z) with width,
  # height and depth dimensions.
  # ====================
def add_box( points, x, y, z, width, height, depth ):
    add_edge(points, x, y, z, x+width, y, z)
    add_edge(points, x, y, z, x, y+height, z)
    add_edge(points, x, y, z, x, y, z+depth)
    add_edge(points, x+width, y, z, x+width, y+height, z)
    add_edge(points, x, y+height, z, x+width, y+height, z)
    add_edge(points, x, y, z+depth, x+width, y, z+depth)
    add_edge(points, x+width, y, z, x+width, y, z+depth)
    add_edge(points, x, y+height, z, x, y+height, z+depth)
    add_edge(points, x, y+height, z+depth, x+width, y+height, z+depth)
    add_edge(points, x+width, y+height, z, x+width, y+height, z+depth)
    add_edge(points, x, y, z+depth, x, y+height, z+depth)
    add_edge(points, x+width, y, z+depth, x+width, y+height, z+depth)

  # ====================
  # Generates all the points along the surface
  # of a sphere with center (cx, cy, cz) and
  # radius r.
  # Returns a matrix of those points
  # ====================
def generate_sphere( points, cx, cy, cz, r, step ):
    a = step
    matrix = []
    while a <= 1+step:
        t = step
        x0 = r + cx
        y0 = cy
        z0 = cz
        while t <= (1+step)/2:
            x0 = r*math.cos(2*math.pi*t)+cx
            y0 = r*math.sin(2*math.pi*t)*math.cos(2*math.pi*a)+cy
            z0 = r*math.sin(2*math.pi*t)*math.sin(2*math.pi*a)+cz
            matrix.append([x0,y0,z0])
            t = t + step
        a = a + step
    return matrix

  # ====================
  # adds all the points for a sphere with center
  # (cx, cy, cz) and radius r to points
  # should call generate_sphere to create the
  # necessary points
  # ====================
def add_sphere( points, cx, cy, cz, r, step ):
    matrix = generate_sphere(points,cx,cy,cz,r,step)
    for coords in matrix:
        add_edge(points, coords[0],coords[1],coords[2], coords[0],coords[1],coords[2])


  # ====================
  # Generates all the points along the surface
  # of a torus with center (cx, cy, cz) and
  # radii r0 and r1.
  # Returns a matrix of those points
  # ====================
# def generate_torus( points, cx, cy, cz, r0, r1, step ):
#     a = 0
#     matrix = []
#     while a <= 1:
#         t = 0
#         x0 = r0 + cx
#         y0 = cy
#         z0 = cz
#         while t <= 1:
#             x0 = math.cos(2*math.pi*a)*(r0*math.cos(2*math.pi*t)+r1)+cx
#             y0 = r0*math.sin(2*math.pi*t)+cy
#             z0 = 0-math.sin(2*math.pi*a)*(r0*math.cos(2*math.pi*t)+r1)+cz
#             matrix.append([x0,y0,z0,0])
#             t = t + step
#         a = a + step
#     return matrix

def generate_torus( points, cx, cy, cz, r0, r1, step ):
    matrix = []
    phi = 0
    while phi<=1:
        theta = 0
        x = r0 + cx
        y = cy
        z = cz
        while theta<=1:
            #print("theta: " + str(theta) + ", phi: " + str(phi))
            x = math.cos(2 * math.pi * phi)*(r0*math.cos(2 * math.pi * theta)+r1) + cx
            y = r0*math.sin(2 * math.pi * theta) + cy
            z = 0-math.sin(2 * math.pi * phi)*(r0*math.cos(2 * math.pi * theta)+r1) + cz
            matrix.append([x,y,z,0])
            theta+=step
        phi+=step
    return matrix

  # ====================
  # adds all the points for a torus with center
  # (cx, cy, cz) and radii r0, r1 to points
  # should call generate_torus to create the
  # necessary points
  # ====================
def add_torus( points, cx, cy, cz, r0, r1, step ):
    matrix = generate_torus(points,cx,cy,cz,r0,r1,step)
    for coords in matrix:
        add_edge(points, coords[0],coords[1],coords[2], coords[0],coords[1],coords[2])



def add_circle( points, cx, cy, cz, r, step ):
    x0 = r + cx
    y0 = cy

    i = 1
    while i <= step:
        t = float(i)/step
        x1 = r * math.cos(2*math.pi * t) + cx;
        y1 = r * math.sin(2*math.pi * t) + cy;

        add_edge(points, x0, y0, cz, x1, y1, cz)
        x0 = x1
        y0 = y1
        t+= step

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):

    xcoefs = generate_curve_coefs(x0, x1, x2, x3, curve_type)[0]
    ycoefs = generate_curve_coefs(y0, y1, y2, y3, curve_type)[0]

    i = 1
    while i <= step:
        t = float(i)/step
        x = t * (t * (xcoefs[0] * t + xcoefs[1]) + xcoefs[2]) + xcoefs[3]
        y = t * (t * (ycoefs[0] * t + ycoefs[1]) + ycoefs[2]) + ycoefs[3]
        #x = xcoefs[0] * t*t*t + xcoefs[1] * t*t + xcoefs[2] * t + xcoefs[3]
        #y = ycoefs[0] * t*t*t + ycoefs[1] * t*t + ycoefs[2] * t + ycoefs[3]

        add_edge(points, x0, y0, 0, x, y, 0)
        x0 = x
        y0 = y
        t+= step


def draw_lines( matrix, screen, color ):
    if len(matrix) < 2:
        print ('Need at least 2 points to draw')
        return

    point = 0
    while point < len(matrix) - 1:
        draw_line( int(matrix[point][0]),
                   int(matrix[point][1]),
                   int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   screen, color)
        point+= 2

def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)

def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )




def draw_line( x0, y0, x1, y1, screen, color ):

    #swap points if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
        x0 = x1
        y0 = y1
        x1 = xt
        y1 = yt

    x = x0
    y = y0
    A = 2 * (y1 - y0)
    B = -2 * (x1 - x0)

    #octants 1 and 8
    if ( abs(x1-x0) >= abs(y1 - y0) ):

        #octant 1
        if A > 0:
            d = A + B/2

            while x < x1:
                plot(screen, color, x, y)
                if d > 0:
                    y+= 1
                    d+= B
                x+= 1
                d+= A
            #end octant 1 while
            plot(screen, color, x1, y1)
        #end octant 1

        #octant 8
        else:
            d = A - B/2

            while x < x1:
                plot(screen, color, x, y)
                if d < 0:
                    y-= 1
                    d-= B
                x+= 1
                d+= A
            #end octant 8 while
            plot(screen, color, x1, y1)
        #end octant 8
    #end octants 1 and 8

    #octants 2 and 7
    else:
        #octant 2
        if A > 0:
            d = A/2 + B

            while y < y1:
                plot(screen, color, x, y)
                if d < 0:
                    x+= 1
                    d+= A
                y+= 1
                d+= B
            #end octant 2 while
            plot(screen, color, x1, y1)
        #end octant 2

        #octant 7
        else:
            d = A/2 - B;

            while y > y1:
                plot(screen, color, x, y)
                if d > 0:
                    x+= 1
                    d+= A
                y-= 1
                d-= B
            #end octant 7 while
            plot(screen, color, x1, y1)
        #end octant 7
    #end octants 2 and 7
#end draw_line
