import json
import os
import uuid
import pandas as pd

import edfs_core as ec


config_root="F:\\EDFS\\configs\\"


def get_root_path():
    return ec.get_root_path()

def set_root_path(new_path):
    ec.set_root_path(new_path=new_path)



# ====================================================
def mkdir(dir_path):
    path_list = dir_path.strip('/').split("/")
    directory_dict = ec.get_directory_meta()

    dir = directory_dict
    if ec.is_exist(path_list):
        print("Directory or file already exist!")
        return False
    else:
        for d in path_list:
            if d in dir.keys():
                dir = dir[d]
            else:
                dir[d] = {}
                dir = dir[d]   
        ec.reset_json(config_root+"directory.json", directory_dict)
        print("Create successfully!")
        return True


def ls(path):
    path_list = path.strip('/').split("/")
    directory_dict = ec.get_directory_meta()
    dir = directory_dict
    for d in path_list:
        if d in dir.keys():
            dir = dir[d]
        else:
            print("No such a path like this.")
            break
    for file in list(dir.keys()):
        print(file)



def rm(file_path):
    path_list = file_path.strip('/').split("/")
    file_name = path_list[-1]
    file_id = ""
    
    if not ec.is_exist(path_list):
        print("File is not existed!")
        return False
    
    directory_dict = ec.get_directory_meta()
    dir = directory_dict
    for d in path_list[:-1]:
        dir = dir[d]
    file_id = dir[file_name]
    dir.pop(file_name)
    ec.reset_json(config_root+"directory.json", directory_dict)

    if isinstance(file_id, str):
        files_meta_dict = ec.get_files_meta()
        files_meta_dict.pop(file_id)
        ec.reset_json(config_root+"files_meta.json", files_meta_dict)

    # ============= to do: delet file from real file system
    print("Delete successfully!")


def put(file_path, store_path, block_lines=100000):
    dir_list = store_path.strip('/').split("/")
    file_name = file_path.strip('\\').split("\\")[-1]

    if not ec.is_exist(dir_list):
        print("directory is not exist! Please create it as first!")
        return False

    total_lines = ec.count_lines(file_path=file_path)
    block_num = int(total_lines/block_lines) + 1
    block_size = (os.path.getsize(file_path)/1024**2)/(block_num - 1) # MB

    # Set the files meta
    file_id = str(uuid.uuid1())
    with open(config_root+"files_meta.json", 'r+') as f:
        file_meta_json = f.read()
        file_meta_dict = json.loads(file_meta_json)
        ## file
        file_meta_dict[file_id] = {"file_name": file_name, "file_blocks":[]}

        ## blocks
        nodes_dict = ec.get_nodes()
        for block_no in range(block_num):
            for node_id, node_info in nodes_dict.items():
                if block_size < node_info['storage']:
                    block_info = {}
                    block_id = str(uuid.uuid1())
                    start_line = block_no*block_lines

                    block_info["block_no"] = block_no
                    block_info["block_id"] = block_id
                    block_info["start"] = start_line
                    block_info['node']=node_id
                    block_info['location']="/"

                    save_block(file_path=file_path, start_line=start_line, line_num=block_lines, save_path=node_info['address'], block_name=block_id)

                    file_meta_dict[file_id]["file_blocks"].append(block_info)
                    # block_no = block_no + 1
                    break
            ec.reset_json(config_root+"files_meta.json", file_meta_dict)
    # Set the directory meta
    ec.add_file_meta(dir_list, file_name, file_id)
    # =========== to do: execute the real process of adding file block on file system ==========

def save_block(file_path, start_line, line_num, save_path, block_name):
    block_file = pd.read_csv(file_path, skiprows=start_line, nrows=line_num)
    if start_line == 0:
        block_file.to_csv(save_path+"\\"+block_name, index=0)
    else:
        block_file.to_csv(save_path+"\\"+block_name, header=0, index=0)



def get_partition_locations(file_path):
    partition_info = ec.get_partition_info(file_path)
    for partition in partition_info:
        print(partition['block_no'], partition['real_path'])


def read_partition(file_path, partition_no):
    path_list = file_path.strip('/').split("/")

    if not ec.is_exist(path_list):
        print("File is not existed!")
        return False
        
    dir = ec.get_directory_meta()
    for d in path_list[:-1]:
        dir = dir[d]
    file_id = dir[path_list[-1]]

    files_meta_dict = ec.get_files_meta()
    first_block = files_meta_dict[file_id]["file_blocks"][int(partition_no)]
        
    nodes_dict = ec.get_nodes()
    node_addr = nodes_dict[first_block['node']]['address']

    real_path = node_addr + first_block['location'] + first_block['block_id']
    real_path = real_path.replace("/", "\\")

    f = open(real_path)

    return f


def cat(file_path):
    f = read_partition(file_path, 0)

    for i in range(5):
        print(f.readline().strip())




if __name__ == '__main__':  
    print("=============Start===============")
    # set_root_path("F:\\EDFS\\DFS\\")
    # print(get_root_path())

    # mkdir("user/John/works/first_work/test")
    # ls("user/John")
    
    # rm("/data/covid/2021/owid-covid-data.csv")
    # put("F:\\EDFS\\dataset\\owid-covid-data.csv", "/data/covid/2021/")
    # put("F:\\EDFS\\dataset\\OxCGRT_latest.csv", "/data/covid/2021/")
    # get_partition_locations("/data/covid/2021/owid-covid-data.csv")
    # cat("/data/covid/2021/owid-covid-data.csv")



