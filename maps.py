import pandas as pd
import os

class Map():
    def __init__(self, job_id, colum_names, partition, field_name):
        self.job_id = job_id
        self.field_name = field_name
        self.colum_names = colum_names
        self.partition = partition

        self.df = pd.read_csv(self.partition['real_path'], low_memory=False)
        self.df.columns = colum_names
        self.temp_dir = os.path.dirname(self.partition['real_path']) + "\\temp\\" + job_id
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)


    def mapPartition(self, target_filed='*', value=None, max=None, min=None):
        result = None
        # Adjust the type of search function
        # result = self.map(field_name=self.field_name, value=value)
        if value is not None:
            result = self.map(target_filed=target_filed, field_name=self.field_name, value=value)
        else:
            result = self.map(target_filed=target_filed, field_name=self.field_name, max=max, min=min)

        # Output the map result
        temp_file_path = self.temp_dir + "\\" + str(self.partition['block_no']) + ".part"
        result.to_csv(temp_file_path, index=None)
        print("\tmap " + str(self.partition['block_no']) + " execution completed!" + "Output to: " + temp_file_path)
        
        # return the temp file path (to reduce)
        return temp_file_path, result.columns

    def map(self):
        '''
        When re-write the function, 
        the parameters must include value, max and min
        '''
        pass



class ValueSearchMap(Map):
    def map(self, target_filed, field_name, value):
        if target_filed == "*":
            result = self.df.loc[self.df[field_name] == value]
        else:
            result = self.df.loc[self.df[field_name] == value][target_filed]

        return pd.DataFrame(result)

class RangeSearchMap(Map):
    def map(self, target_filed, field_name, max, min):
        # map
        if target_filed == "*":
            if min is None and max is None:
                result = self.df.loc[ : , field_name]
            elif min is not None and max is None:
                result = self.df.loc[self.df[field_name] > min]
            elif min is None and max is not None:
                result = self.df.loc[self.df[field_name] < max]
            else:
                result = self.df.loc[(self.df[field_name] > min) & (self.df[field_name] < max)]
        else:
            if min is None and max is None:
                result = self.df.loc[ : , field_name][target_filed]
            elif min is not None and max is None:
                result = self.df.loc[self.df[field_name] > min][target_filed]
            elif min is None and max is not None:
                result = self.df.loc[self.df[field_name] < max][target_filed]
            else:
                result = self.df.loc[(self.df[field_name] > min) & (self.df[field_name] < max)][target_filed]            

        return pd.DataFrame(result)

