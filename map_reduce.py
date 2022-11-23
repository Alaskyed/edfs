import pandas as pd
import uuid

import edfs_core as ec
import edfs_operation as eo

import map.value_search_map as vsp
import reduce.value_search_reduce as vsr
import map.range_search_map as rsp
import reduce.range_search_reduce as rsr


# Value Research
def value_search(file_path, field_name, value):
    # get partition paths
    partitions = ec.get_partition_info(file_path)
    colum_names = pd.read_csv(partitions[0]['real_path']).columns
    # geenrate job id
    job_id = str(uuid.uuid1())

    # map
    map_out_path = []
    for partition in partitions:
        temp_path = vsp.value_search_map(job_id, colum_names, partition, field_name, value)
        map_out_path.append(temp_path)

    # reduce
    result_file_path = vsr.value_search_reduce(job_id, partition, map_out_path, colum_names)
    
    print("Done! The result saved in: " + result_file_path)


## Range Search
def range_search(file_path, field_name, min=None, max=None):
    # get partition paths
    partitions = ec.get_partition_info(file_path)
    colum_names = pd.read_csv(partitions[0]['real_path']).columns
    # geenrate job id
    job_id = str(uuid.uuid1())

    # map
    map_out_path = []
    for partition in partitions:
        temp_path = rsp.range_search_map(job_id, colum_names, partition, field_name, min, max)
        map_out_path.append(temp_path)

    # reduce
    result_file_path = rsr.range_search_reduce(job_id, partition, map_out_path, colum_names)
    
    print("Done! The result saved in: " + result_file_path)





if __name__ == '__main__':  
    # value_search("/data/covid/2021/owid-covid-data.csv", "iso_code", "AFG")
    pass