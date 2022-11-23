import json
import uuid

config_root="F:\\EDFS\\configs\\"

def get_config():
    root_path = ""
    with open(config_root+"config.json", 'r') as f:
        configs_json = f.read()
        config_dict = json.loads(configs_json)

    return config_dict


def get_root_path():
    root_path = ""
    with open(config_root+"config.json", 'r') as f:
        configs_json = f.read()
        config_dict = json.loads(configs_json)
        root_path = config_dict['root_path']

    return root_path


def set_root_path(new_path):
    f = open(config_root+"config.json", 'r+')
    configs_json = f.read()
    config_dict = json.loads(configs_json)

    config_dict['root_path'] = new_path
    new_configs_json = json.dumps(config_dict)

    f.seek(0)
    f.truncate()
    f.write(new_configs_json)
    f.close()

    print("Done!")



def get_nodes():
    nodes_dict = {}
    with open(config_root+"config.json", 'r') as f:
        configs_json = f.read()
        config_dict = json.loads(configs_json)
        nodes_dict = config_dict['nodes']

    return nodes_dict

def add_node(node_addr):
    nodes_dict = {}
    with open(config_root+"config.json", 'r+') as f:
        configs_json = f.read()
        config_dict = json.loads(configs_json)
        nodes_dict = config_dict['nodes']
        nodes_dict[str(uuid.uuid1())] = {"address": node_addr, "storage": 1024}

        f.seek(0)
        f.truncate()
        f.write(json.dumps(config_dict))
        f.close()

    print("Done!")


def get_directory_meta():
    dictioanry_dict = "/"
    with open(config_root+"directory.json", 'r') as f:
        dictioanry_json = f.read()
        dictioanry_dict = json.loads(dictioanry_json)
    return dictioanry_dict


def get_files_meta():
    dictioanry_dict = "/"
    with open(config_root+"files_meta.json", 'r') as f:
        files_meta_json = f.read()
        files_meta_dict = json.loads(files_meta_json)
    return files_meta_dict


def reset_json(file_name, dict):
     with open(file_name, 'r+') as f:
        json_str = json.dumps(dict)
        f.seek(0)
        f.truncate()
        f.write(json_str)

def is_exist(path_list):
    directory_dict = get_directory_meta()
    for d in path_list:
        if d in directory_dict.keys():
            directory_dict = directory_dict[d]
        else:
            return False
    return True

def add_file_meta(dir_path_list, file_name, file_id):
    path_list = dir_path_list
    directory_dict = get_directory_meta()

    dir = directory_dict
    if is_exist(path_list):
        for d in path_list:
            dir = dir[d]
        dir[file_name] = file_id
        reset_json(config_root+"directory.json", directory_dict)
        print("Add file successfully!")


def count_lines(file_path):
    count = -1
    for count, line in enumerate(open(file_path, 'r')):
        pass
    count += 1
    return count


def get_partition_info(file_path):
    path_list = file_path.strip('/').split("/")

    dir = get_directory_meta()
    for d in path_list[:-1]:
        dir = dir[d]
    file_id = dir[path_list[-1]]

    files_meta_dict = get_files_meta()
    partition_dict = files_meta_dict[file_id]["file_blocks"]

    for partition in partition_dict:
        real_path = get_nodes()[partition['node']]['address'] + partition["location"].replace('/', '\\') + partition['block_id']
        partition['real_path'] = real_path    
    return partition_dict
# ================================================






# ============================================










if __name__ == '__main__':  
    # add_node("F:\\EDFS\\DFS\\2")
    # print(get_config())
    # print(get_directory_meta())
    # print(count_lines("F:\\EDFS\\dataset\\owid-covid-data.csv"))
    # get_nodes()
    pass