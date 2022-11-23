import pandas as pd
import os 



def value_search_map(job_id, colum_names, partition, field_name, value):
    df = pd.read_csv(partition['real_path'])
    df.columns = colum_names

    temp_dir = os.path.dirname(partition['real_path']) + "\\temp\\" + job_id
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    result = df.loc[df[field_name] == value]
    temp_file_path = temp_dir + "\\" + str(partition['block_no']) + ".part"
    
    result.to_csv(temp_file_path)

    print("map " + str(partition['block_no']) + "execution completed!" + "Output to: " + temp_file_path)

    return temp_file_path















if __name__ == '__main__':  
    pass