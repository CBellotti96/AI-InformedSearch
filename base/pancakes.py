#Chris Bellotti

from Queue import PriorityQueue

class Graph(object):
    
    def __init__(self, graph_dict=None):
        if graph_dict == None:
            graph_dict = {}
        self.graph_dict = graph_dict
    
    #find_neighbors returns the 3 neighbors from the dictionary based on current vertex
    def find_neighbors(self, vertex):
        my_neighbors = []
        for neighbor in self.graph_dict[vertex]:
            if neighbor not in my_neighbors:
                my_neighbors.append(neighbor)
        return my_neighbors
    
    #get_cost calculates the cost between a vertex and a neighbor and adds that to the total of the path so far
    def get_cost(self, curr_vertex, next_vertex, total):
        my_cost = 0
        curr_vertex = str(curr_vertex)
        next_vertex = str(next_vertex)
        #find location of flip
        for char in range(len(curr_vertex)):
            if curr_vertex[char] != next_vertex[char]:
                my_cost = int(char)
                break
        #add 4-flip location to total
        total = total + (4 - my_cost)
        return total   
    
    #get_heuristic returns the h value of the provided vertex, based on largest pancake out of place
    def get_heuristic(self, curr_vertex):
        if curr_vertex[0] != '4':
            my_heuristic = 4
        elif curr_vertex[1] != '3':
            my_heuristic = 3
        elif curr_vertex[2] != '2':
            my_heuristic = 2
        else:
            my_heuristic = 0
        return my_heuristic
    
#encode_decode is used to handle ties. We must encode the number when placing in the fringe because python priority queue returns the minimum value
#this is called again once we pull a value from the fringe in order to get the original value
def encode_decode_num(value):
    new_value = ""
    char_array = []
    for char in value:
        if char == '1':
            new_value = new_value + '4'
        elif char == '2':
            new_value = new_value + '3'
        elif char == '3':
            new_value = new_value + '2'
        else:
            new_value = new_value + '1'
    
    return new_value

#needed insert_to_fringe so i could order values in case of ties
#only necessary for dfs because i used a list as a lifo queue instead of using the imported PriorityQueue library
def insert_to_fringe_dfs(fringe, vertices):
    vertices = sorted(vertices, key=int)
    for vertex in vertices:
        fringe.append(vertex)
    return fringe

#prints out the path while showing flip locations at each step    
def report_path_dfs(path):
    index = 0
    while index < len(path)-1:
        flip = 0
        s1 = str(path[index])
        s2 = str(path[index+1])
        for char in range(len(s1)):
            if s1[char] != s2[char]:
                flip = char
                break
        print s1[:flip] + '|' + s1[flip:]
        index+=1
    print path[-1]
    return path

#depth first search
def depth_first(graph, start, goal, fringe=None, visited=None, path=None):
    #initialize variables
    if fringe == None:
        fringe = []
    if visited == None:
        visited = [start]
    if path == None:
        path = [start]
    if start == goal:
        report_path_dfs(path)
        return
    #create list of potential fringe values and add only those that are necessary
    potential_fringe = graph.find_neighbors(start)
    for vertex in potential_fringe:
        if (vertex in visited) or (vertex in fringe) :
            potential_fringe.remove(vertex)
    insert_to_fringe_dfs(fringe, potential_fringe)
    #recursively remove and check next values from fringe in LIFO style until a valid path to goal is found
    while fringe:
        next_vertex = fringe.pop()
        path.append(next_vertex)
        #note that since we are doing this recursively, start is not always the root, but is the most recent vertex in the path
        return depth_first(graph, next_vertex, goal, fringe, visited, path)

#prints out the path taken for ucs as well as flip locations and cost at each step in the path
def report_path_ucs(path):
    index = 0
    total_cost = 0
    while index < len(path)-1:
        flip = 0
        s1 = str(path[index])
        s2 = str(path[index+1])
        for char in range(len(s1)):
            if s1[char] != s2[char]:
                flip = char #index of where the flip occurs
                break
        print s1[:flip] + '|' + s1[flip:] + " g=" + str(total_cost)
        cost = int(char)
        total_cost = total_cost + (4 - cost)
        index+=1
    print str(path[-1]) + "  g=" + str(total_cost)
    return path

#unifrom cost search
def uniform_cost(graph, start, goal):
    #initializing variables, fringe will be priority queue with tuples that contain the total cost of path, current vertex, and path
    fringe = PriorityQueue()
    visited = [start]
    in_fringe = []
    total_cost = 0
    path = [start]
    root_neighbors = graph.find_neighbors(start)
    if start == goal:
        report_path_ucs(path)
        return
    for neighbor in root_neighbors:
        #create new instances of path for each possibility and add them all to the fringe
        new_path = list(path)
        new_path.append(neighbor)
        in_fringe.append(neighbor)
        fringe.put((graph.get_cost(start, neighbor, total_cost), int(encode_decode_num(str(neighbor))), new_path))
    while not fringe.empty():
        #pull tuple from fringe and assign values
        total_cost, next_vertex, curr_path = fringe.get()
        next_vertex = int(encode_decode_num(str(next_vertex)))
        #check for goal state
        if next_vertex == goal:
            report_path_ucs(curr_path)
            return
        visited.append(next_vertex)
        neighbors = graph.find_neighbors(next_vertex)
        #if not at the goal, add new neighbors to fringe and continue
        for neighbor in neighbors:
            if (neighbor not in visited) and (neighbor not in in_fringe):
                new_path = list(curr_path)
                new_path.append(neighbor)
                in_fringe.append(neighbor)
                fringe.put((graph.get_cost(start, neighbor, total_cost), int(encode_decode_num(str(neighbor))), new_path))
    print "failure"
    return        

#prints out the path taken as well as flip locations, total cost, and heuristic cost at each step
def report_path_greedy(graph, path):
    index = 0
    total_cost = 0
    while index < len(path)-1:
        flip = 0
        s1 = str(path[index])
        s2 = str(path[index+1])
        heuristic = graph.get_heuristic(s1)
        for char in range(len(s1)):
            if s1[char] != s2[char]:
                flip = char
                break
        print s1[:flip] + '|' + s1[flip:] + " g=" + str(total_cost) + " h=" + str(heuristic)
        cost = int(char)
        total_cost = total_cost + (4 - cost)
        index+=1
    print str(path[-1]) + "  g=" + str(total_cost) + " h=0"
    return path    
    
#greedy search
def greedy(graph, start, goal):
    #initialize values, fringe will be a priority queue of tuples that contain the value of the heuristic and the associated vertex
    visited = [start]
    fringe = PriorityQueue()
    path = [start]
    root_neighbors = graph.find_neighbors(start)
    if start == goal:
        report_path_greedy(graph, path)
        return
    for neighbor in root_neighbors:
        #only focus on heuristic, not cost
        fringe.put((graph.get_heuristic(str(neighbor)), int(encode_decode_num(str(neighbor)))))
    while not fringe.empty():
        #pull values from tuple, add to the path
        curr_heuristic, next_vertex = fringe.get()
        next_vertex = int(encode_decode_num(str(next_vertex)))
        path.append(next_vertex)
        #check for goal state
        if next_vertex == goal:
            report_path_greedy(graph, path)
            return
        visited.append(next_vertex)
        #we do not want to backtrack so clear the fringe and check for current neighbors
        fringe = PriorityQueue()
        neighbors = graph.find_neighbors(next_vertex)
        for neighbor in neighbors:
            if neighbor not in visited:
                fringe.put((graph.get_heuristic(str(neighbor)), int(encode_decode_num(str(neighbor)))))

#prints out the path taken as well as flip locations, total cost, and heuristic cost at each step
def report_path_a_star(graph, path):
    index = 0
    total_cost = 0
    while index < len(path)-1:
        flip = 0
        s1 = str(path[index])
        s2 = str(path[index+1])
        heuristic = graph.get_heuristic(s1)
        for char in range(len(s1)):
            if s1[char] != s2[char]:
                flip = char
                break
        print s1[:flip] + '|' + s1[flip:] + " g=" + str(total_cost) + " h=" + str(heuristic)
        cost = int(char)
        total_cost = total_cost + (4 - cost)
        index+=1
    print str(path[-1]) + "  g=" + str(total_cost) + " h=0"
    return path

#A* search
def a_star(graph, start, goal):
    #initialize values, fringe will be a priority queue of tuples that contain the calculated f value, associated vertex, total cost, and path)
    visited = [start]
    fringe = PriorityQueue()
    in_fringe = []
    path = [start]
    root_neighbors = graph.find_neighbors(start)
    if start == goal:
        report_path_a_star(graph, path)
        return
    for neighbor in root_neighbors:
        #initialize costs to 0, create path instances for each neighbor, and calculate cost of path and f value to place in fringe
        total_cost = 0
        new_path = list(path)
        new_path.append(neighbor)
        in_fringe.append(neighbor)
        total_cost = graph.get_cost(start, neighbor, total_cost)
        heuristic = graph.get_heuristic(str(neighbor))
        f_value = total_cost + heuristic
        fringe.put((f_value, int(encode_decode_num(str(neighbor))), total_cost, new_path))
    while not fringe.empty():
        #pull values from tuple
        f_value, next_vertex, total_cost, curr_path = fringe.get()
        next_vertex = int(encode_decode_num(str(next_vertex)))
        #check for goal state
        if next_vertex == goal:
            report_path_a_star(graph, curr_path)
            return
        visited.append(next_vertex)
        #continue searching from pulled state from fringe, add new neighbors and path instances to the fringe
        neighbors = graph.find_neighbors(next_vertex)
        for neighbor in neighbors:
            if (neighbor not in visited) and (neighbor not in in_fringe):
                new_path = list(curr_path)
                new_path.append(neighbor)
                in_fringe.append(neighbor)
                total_cost = graph.get_cost(next_vertex, neighbor, total_cost)
                heuristic = graph.get_heuristic(str(neighbor))
                f_value = total_cost + heuristic
                fringe.put((f_value, int(encode_decode_num(str(neighbor))), total_cost, new_path))
    print "failure"
    return

if __name__ == "__main__":
    
    #creating dictionary of all nodes and neighbors, could also do this during runtime but there aren't that many possibilities
    
    state_space = { 4123 : [4321, 4132, 3214],
                    3214 : [4123, 3412, 3241],
                    3241 : [3214, 3142, 1423],
                    3142 : [2413, 3241, 3124],
                    3124 : [3142, 3421, 4213],
                    4213 : [4312, 4231, 3124],
                    4312 : [4321, 4213, 2134],
                    4321 : [4312, 4123, 1234],
                    1423 : [3241, 1324, 1432],
                    1324 : [4231, 1423, 1342],
                    4231 : [4213, 4132, 1324],
                    4132 : [4231, 4123, 2314],
                    3412 : [2143, 3214, 3421],
                    2413 : [3142, 2314, 2431],
                    3421 : [1243, 3124, 3412],
                    2134 : [4312, 2431, 2143],
                    1234 : [4321, 1432, 1243],
                    1432 : [2341, 1234, 1423],
                    1342 : [2431, 1243, 1324],
                    2314 : [4132, 2413, 2341],
                    2143 : [3412, 2341, 2134],
                    2431 : [1342, 2134, 2413],
                    1243 : [3421, 1342, 1234],
                    2341 : [1432, 2143, 2314],
                  }
    #create graph object
    graph = Graph(state_space)
    
    while True:
        #run search algorithm based on user input       
        start = raw_input("Please provide starting state and search method, or enter 'q' to quit: ")
        if start == "q":
            exit()
        start_vertex = int(start[0:4])
        search_type = start[4]
        if search_type == "d":
            depth_first(graph,start_vertex, 4321)
        elif search_type == "u":
            uniform_cost(graph,start_vertex, 4321)
        elif search_type == "g":
            greedy(graph,start_vertex, 4321)
        elif search_type == "a":
            a_star(graph, start_vertex, 4321)
        else:
            print "invalid search type"

    