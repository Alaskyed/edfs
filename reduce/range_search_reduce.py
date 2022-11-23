import pandas as pd
import os



def range_search_reduce(job_id, partition, map_outs, columns):
    df = pd.DataFrame(columns=columns)

    result_dir = os.path.dirname(partition['real_path']) + "\\result\\" + job_id

    for map_out in map_outs:
        partition_df = pd.read_csv(map_out)
        df = pd.concat([df, partition_df], axis=0)
    
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    
    result_path = result_dir + "\\result.csv"
    df.to_csv(result_path)

    # Delete the intermediate files (map outputs)
    for map_out in map_outs:
        os.remove(map_out)

    print("Reduce execution completed! Output to: " + result_path)
    print()

    return result_path


















if __name__ == '__main__':  
    pass