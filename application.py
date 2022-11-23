import edfs_operation as eo
import map_reduce as mp

command_list = ["exit", "help", "mkdir", "ls", "cat", "rm", "put", "getPartitionLocations", "readPartition", "searchValue", "searchRange"]

def judge_command(command_list, command):
    command_type = command.split(" ")[0]
    return command_type in command_list

def execute_command(command):
    command_type = command.split(" ")[0]
    parameters = command.split(" ")[1:]

    if command_type == "help":
        print("mkdir <dir path>")
        print("ls <dir path>")
        print("cat <file path>")
        print("rm <file path>")
        print("put <local file path> <file path>")
        print("getPartitionLocations <file path> <partition>")
        print("readPartition <file path> <partition>")
        print()
    elif command_type == "mkdir":
        eo.mkdir(parameters[0])
    elif command_type == "ls":
        eo.ls(parameters[0])
    elif command_type == "cat":
        eo.cat(parameters[0])
    elif command_type == "rm":
        eo.rm(parameters[0])
    elif command_type == "put":
        eo.put(parameters[0], parameters[1])
    elif command_type == "getPartitionLocations":
        eo.get_partition_locations(parameters[0])
    elif command_type == "readPartition":
        eo.read_partition(parameters[0], parameters[1])
    elif command_type == "searchValue":
        mp.value_search(parameters[0], parameters[1], parameters[2])
    elif command_type == "searchRange":
        # min
        mp.range_search(parameters[0], parameters[1], float(parameters[2]), float(parameters[3]))
    


if __name__ == '__main__':  
    command = ""
    while not command == "exit":
        print()
        command = input("Please input your command (input help for details): \n")
        is_exist = judge_command(command_list, command)
        if is_exist:
            try:
                execute_command(command)
            except IndexError:
                print("Parameter Error!")
            except:
                print("Unknow error! Please re-enter the command.")
        else:
            print("Command dose not exist!")
    print("Bye bye ~")



        
