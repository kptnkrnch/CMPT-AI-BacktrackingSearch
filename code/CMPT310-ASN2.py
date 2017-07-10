import sys
import timeit

# Project: CMPT310-ASN2
# Author: Joshua Campbell
# Student Number: 301266191
# Date: October 31, 2016

class ColourVertex: # vertex on the graph
    def __init__(self, name):
        self.name = name # the numerical name for the vertex
        self.edges = list() # edge list for vertex, unused.
        self.colour = -1 # colour number for the vertex
        self.degree = 0 # the number of adjacent vertices
        self.adjacentVertices = list() # list of vertices adjacent to this vertex
        self.legalColoursRemaining = [] # list of legal colours remaining (based on the colours of adjacent vertices
        self.numLegalColoursRemaining = 0 # number of legal colours remaining (shortcut for length of list)
    def __str__(self):
        return self.name

class ColourEdge: # edge between two ColourVertex
    def __init__(self, vertex1, vertex2):
        self.vertex1 = vertex1
        self.vertex2 = vertex2
    def __str__(self):
        return "[" + self.vertex1 + ", " + self.vertex2 + "]"

class ColourGraph: # graph containing ColourVertices and ColourEdges
    def __init__(self, vertices, edges, numColours):
        self.vertices = vertices
        self.edges = edges
        self.numColours = numColours # number of available colours
    def __str__(self):
        return "Edges: " + self.edges

# parseLine is used to parse a standard graph file. It returns a ColourGraph with its vertices, edges, and number of colours
def parseLine(line):
    foundStart = False
    foundEnd = False
    vertexCount = -1
    colourCount = -1
    number = ""
    vertices = []
    edges = []
    edgeFinding = False
    mainVertex = -1
    secondaryVertex = -1
    for i in range(len(line)):
        if i == 0 and line[i] == '(':
            foundStart = True
        elif foundStart and vertexCount == -1:
            if line[i].isdigit():
                number += line[i]
            elif len(number) > 0:
                print "num vertices", number
                vertexCount = int(number)
                number = ""
                for n in range(vertexCount):
                    vertex = ColourVertex(n)
                    vertices.append(vertex)
        elif foundStart and vertexCount != -1 and colourCount == -1:
            if line[i].isdigit():
                number += line[i]
            elif len(number) > 0:
                print "num colours", number
                colourCount = int(number)
                number = ""
        if foundStart and vertexCount != -1 and colourCount != -1:
            if not edgeFinding and line[i] == '(':
                edgeFinding = True
            elif edgeFinding: # generating edges from the graph file
                if line[i].isdigit():
                    number += line[i]
                elif line[i] == ')':
                    if len(number) > 0:
                        secondaryVertex = int(number)
                        edge = ColourEdge(vertices[mainVertex - 1], vertices[secondaryVertex - 1])
                        vertices[mainVertex - 1].degree += 1 # incrementing the degree for the vertex
                        vertices[mainVertex - 1].adjacentVertices.append(vertices[secondaryVertex - 1]) # appending an adjacent vertex
                        edges.append(edge)
                    number = ""
                    mainVertex = -1
                    secondaryVertex = -1
                    edgeFinding = False
                elif mainVertex == -1 and len(number) > 0:
                    mainVertex = int(number)
                    number = ""
                elif len(number) > 0:
                    secondaryVertex = int(number)
                    number = ""
                    edge = ColourEdge(vertices[mainVertex - 1], vertices[secondaryVertex - 1])
                    vertices[mainVertex - 1].degree += 1 # incrementing the degree for the vertex
                    vertices[mainVertex - 1].adjacentVertices.append(vertices[secondaryVertex - 1]) # appending an adjacent vertex
                    edges.append(edge)
    for vertex in vertices: # loop to give all vertices their initial legal remaining colours
        for i in range(colourCount):
            vertex.legalColoursRemaining.append(i)
        vertex.numLegalColoursRemaining = colourCount
    return ColourGraph(vertices, edges, colourCount)

# main backtracking search for colouring the graph
def BacktrackingSearch(graph, useMRVandDegreeHeuristics=False, useLeastConstrainingValueHeuristic=False):
    assignedColours = []
    return RecursiveBacktrack(graph, assignedColours, useMRVandDegreeHeuristics, useLeastConstrainingValueHeuristic)

# recursive portion of the backtracking search
# useMRVandDegreeHeuristics is a flag for enabling the Minimum Remaining Value and Degree hueristics
# useLeastConstrainingValueHeuristic is a flag for enabling the Least Constraining Colour hueristic
def RecursiveBacktrack(graph, assignedColours, useMRVandDegreeHeuristics=False, useLeastConstrainingValueHeuristic=False):
    validColouring = True
    if len(assignedColours) == len(graph.vertices): # checking if the graph is complete
        for vertex in assignedColours:
            for adjacentVertex in vertex.adjacentVertices:
                if adjacentVertex.colour == vertex.colour:
                    validColouring = False
    else:
        validColouring = False

    if validColouring: # if the graph is complete, return the assignments
        return assignedColours
    else: # otherwise, continue searching for a complete graph
        colours = []
        for colour in range(graph.numColours): # generating a list of available colours
            colours.append(colour)

        if useMRVandDegreeHeuristics: # the MinimumRemainingValue heuristic
            unAssignedVertices = getUnassignedVariables(graph, assignedColours) # finding all unassigned vertices
            vertex = findMinimumRemainingValues(colours, unAssignedVertices) # finding the minimum remaining value (vertex)
        else:
            vertex = getUnassignedVariable(graph, assignedColours) # finding the first unassigned variable, fallback if no MRV heuristic
        if vertex is not None:
            if useLeastConstrainingValueHeuristic: # finding the least constraining value (colour)
                leastConstrainingColours = findLeastConstrainingValues(vertex, colours) # returns a list of colours ordered from least constraining to most constraining
                for colour in leastConstrainingColours: # looping through the least constraining colours
                    unusedColour = True
                    for adjacentVertex in vertex.adjacentVertices: # verifying that the colour can be used
                        if colour == adjacentVertex.colour:
                            unusedColour = False
                    if unusedColour:
                        vertex.colour = colour
                        for tempVertex in vertex.adjacentVertices: # updating the legalColoursRemaining for adjacent vertices
                            if colour in tempVertex.legalColoursRemaining:
                                tempVertex.legalColoursRemaining.remove(colour)
                                tempVertex.numLegalColoursRemaining -= 1
                        assignedColours.append(vertex) # adding the vertex to the assigned colours list
                        result = RecursiveBacktrack(graph, assignedColours, useMRVandDegreeHeuristics, useLeastConstrainingValueHeuristic) # start searching again with the newly assigned vertex on the graph
                        if result is not None: # if the result is a complete graph, return the graph
                            return result
                        else: # if the graph is not complete, remove the current vertex from the assigned colours and add the current colour back into the legal
                            # colours remaining list for the adjacent vertices
                            assignedColours.remove(vertex)
                            for tempVertex in vertex.adjacentVertices:
                                if colour not in tempVertex.legalColoursRemaining:
                                    tempVertex.legalColoursRemaining.append(colour)
                                    tempVertex.numLegalColoursRemaining += 1
                            vertex.colour = -1

            else: # fall back if not using least constraining colour heuristic
                for colour in colours: # exhaustive search on all colours
                    unusedColour = True
                    for adjacentVertex in vertex.adjacentVertices: # testing if the colour can be used
                        if colour == adjacentVertex.colour:
                            unusedColour = False
                    if unusedColour:
                        vertex.colour = colour
                        assignedColours.append(vertex)
                        result = RecursiveBacktrack(graph, assignedColours, useMRVandDegreeHeuristics, useLeastConstrainingValueHeuristic) # start searching again with the newly assigned vertex on the graph
                        if result is not None:
                            return result
                        else:
                            assignedColours.remove(vertex)
                            vertex.colour = -1
    return None # returns None if there are no more colours left for the current vertex (ie, the graph is inconsistent)

# used to find the Minimum Remaining Value
# uses the Degree heuristic as a tie breaker
def findMinimumRemainingValues(colours, unAssignedVertices):
    minVertex = None
    minVertexColours = len(colours)
    minVertexDegree = 0
    for vertex in unAssignedVertices: # loops through all unassigned vertices
        if minVertex is None: # setting up the initial minimum vertex
            minVertex = vertex
            adjacentColours = []
            for adjacentVertex in vertex.adjacentVertices:
                if adjacentVertex.colour not in adjacentColours and adjacentVertex.colour != -1:
                    adjacentColours.append(adjacentVertex.colour)
            minVertexColours = len(colours) - len(adjacentColours)
            minVertexDegree = minVertex.degree
        else:
            adjacentColours = []
            for adjacentVertex in vertex.adjacentVertices:
                if adjacentVertex.colour not in adjacentColours and adjacentVertex.colour != -1:
                    adjacentColours.append(adjacentVertex.colour)
            tempVertexColours = len(colours) - len(adjacentColours)
            tempVertexDegree = minVertex.degree
            if tempVertexColours < minVertexColours: # finds the vertex with the least colours remaining
                minVertexColours = tempVertexColours
                minVertex = vertex
                minVertexDegree = tempVertexDegree
            elif tempVertexColours == minVertexColours and tempVertexDegree > minVertexDegree: # Degree heuristic as a tie breaker
                minVertexColours = tempVertexColours
                minVertex = vertex
                minVertexDegree = tempVertexDegree

    return minVertex

# used to find the least constraining values
# returns a list ordered from the least constraining to the most constraining colour
def findLeastConstrainingValues(vertex, colours):
    bestColours = [0 for colour in colours]

    for colour in vertex.legalColoursRemaining: # looping through all legal remaining colours for the vertex
        for adjacentVertex in vertex.adjacentVertices: # looping through the adjacent vertices
            if adjacentVertex.colour == -1: # check to see if the adjacent vertex is not coloured
                if colour in adjacentVertex.legalColoursRemaining: # if the adjacent vertex has the current colour in its legal remaining values
                    bestColours[colour] += (adjacentVertex.numLegalColoursRemaining - 1) # append the number of legal remaining colours - 1 to the colour list
                else:
                    bestColours[colour] += adjacentVertex.numLegalColoursRemaining # otherwise, append the number of legal remaining colours to the colour list

    leastConstrainingColours = []
    consumedColours = []
    while len(consumedColours) < vertex.numLegalColoursRemaining: # loop to order the colours from least constraining to most contraining
        leastConstrainingColourSum = -1
        leastConstrainingColour = -1
        for colour in vertex.legalColoursRemaining:
            if colour not in consumedColours and bestColours[colour] > leastConstrainingColourSum:
                leastConstrainingColourSum = bestColours[colour]
                leastConstrainingColour = colour
        if leastConstrainingColour != -1:
            leastConstrainingColours.append(leastConstrainingColour)
            consumedColours.append(leastConstrainingColour)
    return leastConstrainingColours

def getUnassignedVariable(graph, assignedColours): # finds an unassigned variable
    for vertex in graph.vertices:
        found = False
        for assignment in assignedColours:
            if assignment.name == vertex.name:
                found = True
        if not found:
            return vertex

def getUnassignedVariables(graph, assignedColours): # finds all unassigned variables
    vertices = []
    for vertex in graph.vertices:
        found = False
        for assignment in assignedColours:
            if assignment.name == vertex.name:
                found = True
        if not found:
            vertices.append(vertex)
    return vertices

def mainArgs(): # main program
    fileName = None
    if len(sys.argv) >= 2:
        fileName = sys.argv[1]
    else:
        print "Usage:"
        print "python CMPT310-ASN2.py <graph fileName> <optional: use MRV heuristic; \'true\'/\'false\'> <optional: use LCV heuristic; \'true\'/\'false\'>"

    if len(sys.argv) == 3:
        useMRV = sys.argv[2] == 'true'
        useLCV = True
    elif len(sys.argv) == 4:
        useMRV = sys.argv[2] == 'true'
        useLCV = sys.argv[3] == 'true'
    else:
        useMRV = True
        useLCV = True

    if fileName is not None:
        with open(fileName) as f:
            content = f.readlines()
        if len(content) > 0:
            for line in content:
                graph = parseLine(line) # reading the graph file
                startTime = timeit.default_timer() # start time
                result = BacktrackingSearch(graph, useMRV, useLCV) # search for colouring for the graphs
                endTime = timeit.default_timer() # end time
                sResult = sorted(result, key=lambda x: x.name) # sorting the results by vertex name
                print "Execution Time:", (endTime - startTime)
                if result is None:
                    print "Failed"
                else:
                    for vertex in sResult: # printing the results
                        print "Vertex: %d Colour: %d" % (vertex.name + 1, vertex.colour)

mainArgs()