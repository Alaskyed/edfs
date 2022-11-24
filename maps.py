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


    def mapPartition(self, value=None, max=None, min=None):
        result = None
        # Adjust the type of search function
        # result = self.map(field_name=self.field_name, value=value)
        if value is not None:
            result = self.map(field_name=self.field_name, value=value)
        else:
            result = self.map(field_name=self.field_name, max=max, min=min)

        # Output the map result
        temp_file_path = self.temp_dir + "\\" + str(self.partition['block_no']) + ".part"
        result.to_csv(temp_file_path)
        print("\tmap " + str(self.partition['block_no']) + " execution completed!" + "Output to: " + temp_file_path)
        
        # return the temp file path (to reduce)
        return temp_file_path

    def map(self):
        '''
        When re-write the function, 
        the parameters must include value, max and min
        '''
        pass



class ValueSearchMap(Map):
    def map(self, field_name, value):
        result = self.df.loc[self.df[field_name] == value]

        return result

class RangeSearchMap(Map):
    def map(self, field_name, max, min):
        # map
        if min is None and max is None:
            result = self.df.loc[ : , field_name]
        elif min is not None and max is None:
            result = self.df.loc[self.df[field_name] > min]
        elif min is None and max is not None:
            result = self.df.loc[self.df[field_name] < max]
        else:
            result = self.df.loc[(self.df[field_name] > min) & (self.df[field_name] < max)]
        return result

