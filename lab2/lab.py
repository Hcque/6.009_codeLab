# NO IMPORTS ALLOWED!

import json

def did_x_and_y_act_together(data, actor_id_1, actor_id_2):
    for i in data:
        if (i[0] == actor_id_1 and i[1] == actor_id_2) or\
        (i[0] == actor_id_2 and i[1] == actor_id_1):
            return True
    return False
          
def get_actors_with_bacon_number(data, n):
    # revise data to dictionary
    data_dict = {}
    for item in data:
        if item[0] not in data_dict:
            data_dict[item[0]] = {item[1]}
        else:
            data_dict[item[0]].add(item[1])
        if item[1] not in data_dict:
            data_dict[item[1]] = {item[0]}
        else:
            data_dict[item[1]].add(item[0])
            
    frontier = {4724}
    parents = {4724:None}
    for i in range(n):
        new_set = set()
        for actorId in frontier: 
            for item in data_dict[actorId]:
                if item not in parents:
                    new_set.add(item)
                    parents[item] = actorId  
        if len(new_set) == 0:
            return None
        frontier = new_set 
    return frontier 

def get_bacon_path(data, actor_id):
    # revise data to dictionary
    data_dict = {}
    for item in data:
        if item[0] not in data_dict:
            data_dict[item[0]] = {item[1]}
        else:
            data_dict[item[0]].add(item[1])
        if item[1] not in data_dict:
            data_dict[item[1]] = {item[0]}
        else:
            data_dict[item[1]].add(item[0])
            
    frontier = {4724}
    parents = {4724:None}
    has_find = False
    while not has_find:
        new_set = set()
        for actorId in frontier: 
            for item in data_dict[actorId]:
                if item not in parents:
                    new_set.add(item)
                    parents[item] = actorId  
        if actor_id in new_set:
            has_find = True
        if len(new_set) == 0:
            return None
        frontier = new_set
    # get path
    path = [actor_id]
    while path[-1] != 4724:
        path.append(parents[path[-1]])
    path.reverse()
    return path        
        
def get_path(data, actor_id_1, actor_id_2):
    # revise data to dictionary
    data_dict = {}
    for item in data:
        if item[0] not in data_dict:
            data_dict[item[0]] = {item[1]}
        else:
            data_dict[item[0]].add(item[1])
        if item[1] not in data_dict:
            data_dict[item[1]] = {item[0]}
        else:
            data_dict[item[1]].add(item[0])
            
    frontier = {actor_id_1}
    parents = {actor_id_1:None}
    has_find = False
    while not has_find:
        new_set = set()
        for actorId in frontier: 
            for item in data_dict[actorId]:
                    if item not in parents:
                        new_set.add(item)
                        parents[item] = actorId  
        if actor_id_2 in new_set:
            has_find = True
        if len(new_set) == 0:
            return None
        frontier = new_set
    # get path
    path = [actor_id_2]
    while path[-1] != actor_id_1:
        path.append(parents[path[-1]])
    path.reverse()
    return path      

def get_movie_path(data, actor_id_1, actor_id_2):
    path = get_path(data, actor_id_1, actor_id_2)
    # revise data to handle movies
    search_movies = {}
    for i in data:
        search_movies[(i[0],i[1])] = i[2]
        search_movies[(i[1],i[0])] = i[2]
    # get movie names
    with open('resources/movies.json', 'r') as f:
        movies = json.load(f)
    movie_data = {movies[i]:i for i in movies}
    movie_path = []
    for i in range(len(path)-1):
        m_id = search_movies[(path[i], path[i+1])]
        m_name = movie_data[m_id]
        movie_path.append(m_name)
    return movie_path

# helper function
def to_id(name):
    filename = 'resources/names.json'
    with open(filename, 'r') as f:
        name_data = json.load(f)
    return name_data[name]

def to_name(id):
    filename = 'resources/names.json'
    with open(filename, 'r') as f:
        name_data = json.load(f)
    name_data = {name_data[item]:item for item in name_data}
    return name_data[id]
# end helper function

# answer questions
def answer_act_together(data):
    name1 = ['Craig Bierko', 'Beatrice Winde', 'Kevin Bacon', 'Eduardo Yanez']
    name2 = ['Tom Amandes', 'Melanie Laurent', 'David Stevens', 'Jason Robards']
    for i in range(4):
        ans = did_x_and_y_act_together(data, to_id(name1[i]), to_id(name2[i]))
        print(name1[i] + ' and ' + name2[i] + 'act together: ')
        print(ans)

def answer_path(data):
    names = ['Gregg Henry', 'Lloyd Hamilton', 'Sven Batinic']
    for i in range(3):    
        path = get_path(data, to_id('Kevin Bacon'), to_id(names[i]))
    return [to_name(n) for n in path]
        
    
if __name__ == '__main__':
    with open('resources/small.json') as f:
        smalldb = json.load(f)
    with open('resources/large.json') as f:
        db_large = json.load(f)
    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    
    # answer_act_together(smalldb)
    
#    for i in range(3,5): 
#        ans = get_actors_with_bacon_number(smalldb, i)
#        print('Set of actors with Bacon number ', i, ' is : ')
#        if ans is not None:
#            names = set()
#            for id in ans:
#                names.add(to_name(id))
#            print(names)
#        else:
#            print(None)
#    
#    for i in range(5,7): 
#        ans = get_actors_with_bacon_number(db_large, i)
#        print('Set of actors with Bacon number ', i, ' is : ')
#        if ans is not None:
#            names = set()
#            for id in ans:
#                names.add(to_name(id))
#            print(names)
#        else:
#            print(None)
    
#    print(answer_path(db_large))
#    def get_path_names(data, n1, n2):
#        path = get_path(data, to_id(n1), to_id(n2))
#        print([to_name(i) for i in path])
#        return [to_name(i) for i in path]
#    get_path_names(db_large, 'Tom Hanks', 'Vjeran Tin Turk')
#    get_path_names(db_large, 'Roland Freitag', 'Curtis Hanson')

#    print(get_movie_path(db_large, to_id('Anton Radacic'), to_id('Hayden Christensen')))
#    print(get_movie_path(db_large, to_id('Ronn Carroll'), to_id('Kai-tai Di')))
    
#    actor_id = 1345462
#    len_expected = 6
#    result = get_bacon_path(db_large, actor_id)
#    print(result)
    
#    movie_path = get_movie_path(db_large, 1345462, 4724)
#    print(movie_path)
    