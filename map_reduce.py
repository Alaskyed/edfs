import pandas as pd
import uuid


import edfs_core as ec
import edfs_operation as eo


from maps import ValueSearchMap, RangeSearchMap
from reduces import Reduce


# Value Research
def value_search(file_path, field_name, value):
    # get partition paths
    partitions = ec.get_partition_info(file_path)
    colum_names = pd.read_csv(partitions[0]['real_path'], low_memory=False).columns
    # geenrate job id
    job_id = str(uuid.uuid1())

    # map
    map_out_path = []
    for partition in partitions:
        vsm = ValueSearchMap(job_id, colum_names, partition, field_name)
        temp_path = vsm.mapPartition(value=value)
        map_out_path.append(temp_path)

    # reduce
    reduce = Reduce(job_id, partition, colum_names, map_out_path)
    result_file_path = reduce.reduce()
    
    print("Done! The result saved in: " + result_file_path)


## Range Search
def range_search(file_path, field_name, min=None, max=None):
    # get partition paths
    partitions = ec.get_partition_info(file_path)
    colum_names = pd.read_csv(partitions[0]['real_path'], low_memory=False).columns
    # geenrate job id
    job_id = str(uuid.uuid1())

    # map
    map_out_path = []
    for partition in partitions:
        rsm = RangeSearchMap(job_id, colum_names, partition, field_name)
        temp_path = rsm.mapPartition(min=min, max=max)
        map_out_path.append(temp_path)

    # reduce
    reduce = Reduce(job_id, partition, colum_names, map_out_path)
    result_file_path = reduce.reduce()
    
    print("Done! The result saved in: " + result_file_path)





if __name__ == '__main__':  
    # value_search("/data/covid/2021/owid-covid-data.csv", "iso_code", "AFG")
    pass