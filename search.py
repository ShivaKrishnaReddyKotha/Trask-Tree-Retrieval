import pickle
import json
from FOON_class import Object

# -----------------------------------------------------------------------------------------------------------------------------#

# Checks an ingredient exists in kitchen


def check_if_exist_in_kitchen(kitchen_items, ingredient):
    """
        parameters: a list of all kitchen items,
                    an ingredient to be searched in the kitchen
        returns: True if ingredient exists in the kitchen
    """

    for item in kitchen_items:
        if item["label"] == ingredient.label \
                and sorted(item["states"]) == sorted(ingredient.states) \
                and sorted(item["ingredients"]) == sorted(ingredient.ingredients) \
                and item["container"] == ingredient.container:
            return True

    return False


# -----------------------------------------------------------------------------------------------------------------------------#

# Iterative Deepening Search

def IDS_search(kitchen_items, goal_node):
    max_depth = 0
    while True:
        task_tree_units = depth_limited_search(kitchen_items, goal_node, max_depth)
        if task_tree_units:
            return task_tree_units
        else:
            if max_depth>1000:
                return task_tree_units
        max_depth += 1

def depth_limited_search(kitchen_items, goal_node, depth_limit):
    items_already_searched = []
    items_to_search = []
    items_to_search.append(goal_node)
    reference_task_tree = []

    while len(items_to_search) > 0:
        current_item = items_to_search.pop(0)
        if current_item in items_already_searched:
            continue

        else:
            items_already_searched.append(current_item)


        if not check_if_exist_in_kitchen(kitchen_items, current_item):
            candidate_units = foon_object_to_FU_map[current_item.id]

            for selected_candidate in candidate_units:
                    if selected_candidate in reference_task_tree:
                        continue
                    
                    fu = foon_functional_units[selected_candidate]

            if selected_candidate in reference_task_tree:
                continue

            reference_task_tree.append(selected_candidate)

            for node in foon_functional_units[
                    selected_candidate].input_nodes:
                node_index = node.id
                if node_index not in items_to_search:
                    flag = True
                    if node.label in utensils and len(node.ingredients) == 1:
                        for node2 in foon_functional_units[
                                selected_candidate].input_nodes:
                            if node2.label == node.ingredients[0] and node2.container == node.label:
                                flag = False
                                break

                if node not in items_to_search and node not in items_already_searched:
                            items_to_search.append(node)

    reference_task_tree.reverse()

    result = []
    for i in reference_task_tree:
        result.append(foon_functional_units[i])

    return result

# -----------------------------------------------------------------------------------------------------------------------------#

# BFS search with heuristic-1 success rate of the motion

def search_BFS_heuristic1(kitchen_items=[], goal_node=None):
    items_already_searched = []
    items_to_search = []
    items_to_search.append(goal_node)
    reference_task_tree = []

    while len(items_to_search) > 0:
        current_item = items_to_search.pop(0)
        if current_item in items_already_searched:
            continue

        else:
            items_already_searched.append(current_item)

        if isinstance(current_item, Object):
            if not check_if_exist_in_kitchen(kitchen_items, current_item):
                candidate_units = foon_object_to_FU_map[current_item.id]

                best_path = None
                best_success_rate = 0

                for selected_candidate_index in candidate_units:
                    if selected_candidate_index in reference_task_tree:
                        continue
                    
                    fu = foon_functional_units[selected_candidate_index]
                    
                    motion_name = fu.motion_node

                    success_rate = 1.0
                    if motion_name:
                        with open('motion.txt', 'r') as motion_file:
                            for line in motion_file:
                                motion_file_data = line.split("\t")
                                if motion_file_data[0] == motion_name:
                                    success_rate = float(motion_file_data[1])
                                    break

                    if success_rate > best_success_rate:
                        best_success_rate = success_rate
                        best_path = selected_candidate_index

                if best_path is not None:
                    reference_task_tree.append(best_path)

                    for i in foon_functional_units[best_path].input_nodes:
                        if i not in items_to_search and i not in items_already_searched:
                            items_to_search.append(i)


    reference_task_tree.reverse()

    task_tree_units = []
    for i in reference_task_tree:
        task_tree_units.append(foon_functional_units[i])

    return task_tree_units



# -----------------------------------------------------------------------------------------------------------------------------#

# BFS search with heuristic-2 number of input objects in the functional unit

def search_BFS_heuristic2(kitchen_items=[], goal_node=None):

    items_already_searched = []
    reference_task_tree = []
    items_to_search = []
    items_to_search.append(goal_node)

    while len(items_to_search) > 0:
        current_item = items_to_search.pop(0)
        if current_item in items_already_searched:
            continue

        else:
            items_already_searched.append(current_item)

        if isinstance(current_item, Object):
            if not check_if_exist_in_kitchen(kitchen_items, current_item):
                candidate_units = foon_object_to_FU_map[current_item.id]

                best_path = None
                min_input_count = float('inf')

                for selected_candidate_index in candidate_units:
                    if selected_candidate_index in reference_task_tree:
                        continue

                    fu = foon_functional_units[selected_candidate_index]

                    input_count = len(fu.input_nodes)

                    if input_count < min_input_count:
                        min_input_count = input_count
                        best_path = selected_candidate_index

                if best_path is not None:
                    reference_task_tree.append(best_path)

                    for i in foon_functional_units[best_path].input_nodes:
                        if i not in items_to_search and i not in items_already_searched:
                            items_to_search.append(i)


    reference_task_tree.reverse()

    task_tree_units = []
    for i in reference_task_tree:
        task_tree_units.append(foon_functional_units[i])

    return task_tree_units



# -----------------------------------------------------------------------------------------------------------------------------#

# creates the graph using adjacency list
# each object has a list of functional list where it is an output

def save_paths_to_file(task_tree, path):
    print('writing generated task tree to ', path)
    with open(path, 'w') as _file:
        _file.write('//\n')
        for FU in task_tree:
            _file.write(FU.get_FU_as_text() + "\n")
            
def read_universal_foon(filepath='FOON.pkl'):
    """
        parameters: path of universal foon (pickle file)
        returns: a map. key = object, value = list of functional units
    """
    pickle_data = pickle.load(open(filepath, 'rb'))
    functional_units = pickle_data["functional_units"]
    object_nodes = pickle_data["object_nodes"]
    object_to_FU_map = pickle_data["object_to_FU_map"]

    return functional_units, object_nodes, object_to_FU_map


# -----------------------------------------------------------------------------------------------------------------------------#

if __name__ == '__main__':
    foon_functional_units, foon_object_nodes, foon_object_to_FU_map = read_universal_foon(
    )

    utensils = []
    with open('utensils.txt', 'r') as f:
        for line in f:
            utensils.append(line.rstrip())

    kitchen_items = json.load(open('kitchen.json'))

    goal_nodes = json.load(open("goal_nodes.json"))

    for node in goal_nodes:
        node_object = Object(node["label"])
        node_object.states = node["states"]
        node_object.ingredients = node["ingredients"]
        node_object.container = node["container"]
        
 
        for object in foon_object_nodes:
            if object.check_object_equal(node_object):
                output_task_tree = search_BFS_heuristic1(kitchen_items, object)
                if(output_task_tree is not None):
                    save_paths_to_file(output_task_tree,'output_BFS_h1_{}.txt'.format(node["label"]))
                else:
                    print("The goal node does not exist")
                break

        for object in foon_object_nodes:
            if object.check_object_equal(node_object):
                output_task_tree = search_BFS_heuristic2(kitchen_items, object)
                if(output_task_tree is not None):
                    save_paths_to_file(output_task_tree,'output_BFS_h2_{}.txt'.format(node["label"]))
                else:
                    print("The goal node does not exist")
                break
        
        for object in foon_object_nodes:
            if object.check_object_equal(node_object):
                output_task_tree = IDS_search(kitchen_items, object)
                if(output_task_tree is not None):
                    save_paths_to_file(output_task_tree,'output_IDS_{}.txt'.format(node["label"]))
                else:
                    print("The goal node does not exist")
                break

        
        
       
