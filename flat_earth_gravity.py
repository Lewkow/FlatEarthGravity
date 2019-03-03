import math
import matplotlib.pyplot as plt

grid_N = 100
disc_r = 90

def make_plot(data):
    fig, ax = plt.subplots()
    plt.xlim(0,1)
    plt.ylim(0,1)
    for d in data:
        (r,(x,y)) = d
        plt.plot(x,y,lw=2,label="%d percent thickness ratio"%(int(r*100)))
    plt.ylabel('Force of Gravity Relative to Center of Disc [arbitrary units]')
    plt.xlabel('Distance from Center of Disc [arbitrary units]')
    plt.legend()
    plt.draw()
    plt.savefig("gravity.png")
    plt.clf()
    plt.close(fig)

def get_grid_mass(x,y,z,disk_h):
    if (math.sqrt(x*x+y*y) <= disc_r) and (abs(z) <= disk_h/2):
        return 1
    else:
        return 0

def get_grid(N,disk_h):
    grid_index = list(range(-int(N/2),int(N/2)+1,1))
    grid_matrix = {}
    mass_location = []
    for x in grid_index:
        for y in grid_index:
            for z in grid_index:
                grid_matrix[(x,y,z)] = get_grid_mass(x,y,z,disk_h)
                if grid_matrix[(x,y,z)] == 1:
                    mass_location.append((x,y,z))
    return(grid_matrix,mass_location)

def get_gravity(x,y,z,grid):
    force = 0
    for mass in grid:
        r = math.sqrt(math.pow((x-mass[0]),2)+
                      math.pow((y-mass[1]),2)+
                      math.pow((z-mass[2]),2))
        if r > 0:
            force += 1.0/math.pow(r,2)
    return(force)

def get_disk_force(disk_r,disk_h):
    (grid_matrix,mass_location) = get_grid(grid_N,disk_h)
    gravity = []
    r = range(0,disc_r,1)
    for x in r:
        force = get_gravity(x,0,0,mass_location)
        gravity.append(force)
    relative_gravity = [tmp/max(gravity) for tmp in gravity]
    relative_r = [tmp/max(r) for tmp in r]
    return((relative_r,relative_gravity))

if __name__ == '__main__':
    gravities = []
    for ratio in [0.01,0.05,0.1,0.5]:
        print("doing %f ratio"%(ratio))
        (r,g) = get_disk_force(disc_r, int(ratio*disc_r))
        gravities.append((ratio,(r,g)))
    make_plot(gravities)
