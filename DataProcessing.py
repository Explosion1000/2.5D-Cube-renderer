import numpy as np

#TODO: 
# Implement in main Code which is STILL called Test for some reason.
# Delete that useless vertex_ammount variable.

def getVerticesFromFile():
    file = open("testcube.obj", "r")                 #opens file

    vertices = ([])                                  #Creates the array that stores the vertices as split arrays

    for Line in file:

        if Line[0] == "v" and Line[1] == " ":        #checks if the line stores a vertex
            vertices.append(str.split(Line)[1:])         #adds the data from each line as an array and removes the "v"

    vertex_ammount = len(vertices)                   #placeholder which I thought I would need (Could still prove useful (maybe?))

    vertex = np.array(vertices)                      #Turns the array into a multidimensional array.
    file.close                                       #Do I have to comment everything?
    return (vertex)

def getFacesFromFile():                              #Same as the vertices but without the unnecessary values for textures
    file = open("testcube.obj", "r")

    faces = ([])

    for Line in file:

        if Line[0] == "f":
            faces.append([s[0] for s in Line.split()][1:])
    
    quads = np.array(faces)
    file.close
    return (quads)

coords = getVerticesFromFile()                       #stors the Result
faces = getFacesFromFile()
        
print(coords)
print(faces)

