import edfs_operation as eo
import map_reduce as mp

command_list = ["exit", "help", "mkdir", "ls", "cat", "rm", "put", "getpartitionlocations", "readpartition", "searchvalue", "searchrange"]

def judge_command(command_list, command):
    command_type = command.split(" ")[0].lower()
    return command_type in command_list

def execute_command(command):
    command_type = command.split(" ")[0].lower()
    parameters = command.split(" ")[1:]

    if command_type == "help":
        print("mkdir <dir path>")
        print("ls <dir path>")
        print("cat <file path>")
        print("rm <file path>")
        print("put <local file path> <file path>")
        print("getPartitionLocations <file path> <partition>")
        print("readPartition <file path> <partition>")
        print("searchValue <file path> <target fields> <constraint fileds> <value>")
        print("searchRange <file path> <target fields> <constraint fileds> <min> <max>")
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
    elif command_type == "getpartitionlocations":
        eo.get_partition_locations(parameters[0])
    elif command_type == "readpartition":
        print(eo.read_partition(parameters[0], parameters[1]), "\n")
    elif command_type == "searchvalue":
        mp.value_search(parameters[0], parameters[1], parameters[2], parameters[3])
    elif command_type == "searchrange":
        # min
        mp.range_search(parameters[0], parameters[1], parameters[2], float(parameters[3]), float(parameters[4]))
    


if __name__ == '__main__':  
    command = ""
    while not command == "exit":
        print()
        command = input("Please input your command (input help for details): \n")
        is_exist = judge_command(command_list, command)
        if is_exist:
            # execute_command(command)
            try:
                execute_command(command)
            except IndexError:
                print("Parameter Error!")
            except:
                print("Unknow error! Please re-enter the command.")
        else:
            print("Command dose not exist!")
    print("Bye bye ~")