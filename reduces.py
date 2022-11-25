import pandas as pd
import os
import shutil


class Reduce():
    def __init__(self, job_id, partition, columns, map_outs):
        self.job_id = job_id
        self.partition = partition
        self.colum_names = columns
        self.map_outs = map_outs

        self.df = pd.DataFrame(columns=self.colum_names)
        self.result_dir = os.path.dirname(self.partition['real_path']) + "\\result\\" + job_id
        if not os.path.exists(self.result_dir):
            os.makedirs(self.result_dir)

    def reduce(self):
        for map_out in self.map_outs:
            partition_df = pd.read_csv(map_out)
            self.df = pd.concat([self.df, partition_df], axis=0)

        result_path = self.result_dir + "\\result.csv"
        self.df.to_csv(result_path, index=None)

        # Delete the intermediate files (map outputs)
        dir_path = os.path.dirname(self.map_outs[0])
        shutil.rmtree(dir_path)
            

        print("\tReduce execution completed! Output to: " + result_path)
        print()

        return result_path


















if __name__ == '__main__':  
    pass