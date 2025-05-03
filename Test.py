import sys, pygame
from pygame.locals import*
import numpy as np
from decimal import Decimal

#TODO:
# Clean this mess up
# Do not forget to update the screen before ending up in a mental breakdown because stuff won't show up on screen

#WAS MACHT DER CODE:
# 1. Grafik-fenster wird erstellt
# 2. Im np array coords_str werden die Koordinaten von den Eckpunkten als Dimensionen gespeichert
# 3. Das selbe passiert auch mit den Daten für die Oberflächen(faces)
# 4. Die Daten aus coords_str und faces_str werden in float und intiger umgewandelt, damit die Mathematik damit funktioniert
# 5. Ein graues Raster mit der größe cell_size wird dargestellt
# 6. Der 3D-Effekt wird auf die Koordinaten der Eckpunkte angewendet, indem sie um 0.3536 mal die z koordinate auf x und y verschoben werden
#    *0.3536 damit es genau die hälfte im Diagonalen ist und besser aussieht*
# 7. die Koordinaten werden in drawdata als intiger gespeichert, weil das anzeigen auf dem Bildschirm nicht mit komma Zahlen funktioniert
# 8. Drawdata und faces werden von arrays in Listen konvertiert, weil man Listen leichter sortiern kann
# 9. Die z Koordinate der Oberflächen wird durch den Durchschnitt zwischen zwei Eckpunkten ermittelt und zu der facelist hinzugefügt
# 10. Die facelist wird nach der z Koordinate sortiert, damit Objekte verdeckt werden.
# 11. Durch den Richtungsvektor, welcher durch die Reihenfolge der Eckpunkte berechnet wird lässt sich feststellen, ob die Oberfläche
#     "mit dem Rücken" zur Kamera zeigt und nicht gezeichnet werden soll
# 12. Die Flächen werden erst mit schwarz gefüllt um die dahinterliegenden Flächen zu verdecken und dann als Umrandung dargestellt

# Ab hier sind alle kommentare auf Englisch, weil ich es nicht mag, wenn deutsche kommentare in englischem code sind.

width = 2560
height = 1440
screen_color = (0, 0, 0)
line_color = (255, 255, 255)
offset_x = width // 2
offset_y = height // 2
zoom = 10
cell_size = 10

pygame.display.set_caption("OBJ Viewer")

def getVerticesFromFile():
    file = open("opera.obj", "r")                 #opens file

    vertices = ([])                                  #Creates the array that stores the vertices as split arrays

    for Line in file:

        if Line[0] == "v" and Line[1] == " ":        #checks if the line stores a vertex
            vertices.append([s for s in Line.split()][1:])         #adds the data from each line as an array and removes the "v"

    vertex_ammount = len(vertices)                   #placeholder which I thought I would need (Could still prove useful (maybe?))

    vertex = np.array(vertices)                      #Turns the array into a multidimensional array.
    file.close()                                     #Do I have to comment everything?
    return (vertex)

def getFacesFromFile():                              #Same as the vertices but without the unnecessary values for textures
    file = open("opera.obj", "r")

    faces = ([])

    for Line in file:

        if Line[0] == "f":
            faces.append([s.split("/")[0] for s in Line.strip().split()[1:]])
    
    quads = np.array(faces)
    file.close()
    return (quads)

coords_str = np.array(getVerticesFromFile())                       #stores the Result
faces_str = np.array(getFacesFromFile())

coords = coords_str.astype(float)                                  #python doesn't like strings in math
faces = faces_str.astype(int)

def ConvertCoords():                                               #applies the 3d effect to the coords

    for i in range(len(coords)):
        coords[i, 0] = coords[i, 0] * zoom + offset_x + -(coords[i, 2] * 0.3536 * zoom)
        coords[i, 1] = -coords[i, 1] * zoom + offset_y + coords[i, 2] * 0.3536 * zoom
        coords[i, 2] = coords[i, 2] * zoom

def main():
    screen=pygame.display.set_mode((width,height))
    screen.fill(screen_color)

    def drawGrid():                                                # draws the grid
        for x in range(0, width, cell_size):
            pygame.draw.line(screen, (50, 50, 50), (x, 0), (x, height))

        for x in range(0, height, cell_size):
            pygame.draw.line(screen, (50, 50, 50), (0, x), (width, x))

    drawGrid()

    ConvertCoords()
    drawdata = coords.astype(int)                                  # converts drwadata to int

    drawlist = drawdata.tolist()                                   # converts np arrays to lists
    facelist = faces.tolist()

    #print(drawlist)
    #print(facelist)

    def getZValue():
        
        for i in range(len(facelist)):
            x = drawlist[(facelist[i][1])-1]                        # gets the coordinates of 2 vertices of a face
            y = drawlist[(facelist[i][3])-1]
            division = [2, 2, 2]
            z = [l1 + l2 for l1, l2 in zip(x, y)]                   # adds the coordinates
            result = [l1 / l2 for l1, l2 in zip(z, division)]       # divides the coordinates by 2
            facelist[i].append(result[2])                           # adds the faces z value to the facelist
            facelist[i].append(result[1])        

        #print(*facelist)
        facelist_z = sorted(facelist, key=lambda v: (v[4], -v[5]))         # sorts the facelist by the z value

        return(facelist_z)
    
    def is_backface(face, coords):
            v0 = coords[(facelist_z[face][0]-1)]                    # gets 3 vertex coordinates of the face
            v1 = coords[(facelist_z[face][1]-1)]
            v2 = coords[(facelist_z[face][2]-1)]

            # Calculate two edges
            edge1 = v1 - v0
            edge2 = v2 - v0

            # Compute normal with cross product
            normal = np.cross(edge1, edge2)

            # View vector (camera is at z = -∞ looking toward +z)
            view_dir = np.array([0, 0, -1])

            # If dot product < 0, the face is visible
            return np.dot(normal, view_dir) >= 0  # True = backface
    
    facelist_z = getZValue()
        
    getZValue()

    def drawMesh(zoomlevel = 1):
        #Draws stuff
        screen.fill(screen_color)

        for i in range(len(facelist_z)):

            if not is_backface(i, coords):                              # checks if the face is backfacing
                continue

            #draws the faces
            pygame.draw.polygon(screen,(0, 0, 0), (((drawlist[((facelist_z[i][0])-1)][0] * zoomlevel), (drawlist[((facelist_z[i][0])-1)][1] * zoomlevel)), 
                                                    ((drawlist[((facelist_z[i][1])-1)][0] * zoomlevel), (drawlist[((facelist_z[i][1])-1)][1] * zoomlevel)), 
                                                    ((drawlist[((facelist_z[i][2])-1)][0] * zoomlevel), (drawlist[((facelist_z[i][2])-1)][1] * zoomlevel)), 
                                                    ((drawlist[((facelist_z[i][3])-1)][0] * zoomlevel), (drawlist[((facelist_z[i][3])-1)][1] * zoomlevel))))
            
            pygame.draw.polygon(screen,line_color, (((drawlist[((facelist_z[i][0])-1)][0] * zoomlevel), (drawlist[((facelist_z[i][0])-1)][1] * zoomlevel)), 
                                                    ((drawlist[((facelist_z[i][1])-1)][0] * zoomlevel), (drawlist[((facelist_z[i][1])-1)][1] * zoomlevel)), 
                                                    ((drawlist[((facelist_z[i][2])-1)][0] * zoomlevel), (drawlist[((facelist_z[i][2])-1)][1] * zoomlevel)), 
                                                    ((drawlist[((facelist_z[i][3])-1)][0] * zoomlevel), (drawlist[((facelist_z[i][3])-1)][1] * zoomlevel))), 1)
        
        pygame.display.flip()
        
    drawMesh()

    zom = 1

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == MOUSEWHEEL:
                zom += event.y
                print(zom)
                drawMesh(zom)
main()

