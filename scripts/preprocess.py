def print_lines(data:str,n_lines:int=3)->None:
    lines = data.split('\n')
    print("\n".join(lines[0:n_lines]))
    return

def run(path:str = "./data/human_HG38/NPC/Oth.Neu.05.AllAg.Neural_progenitor_cells.bed",
        target_path:str = "./data/human_HG38/NPC/NPC_pp.csv"):

    with open(path) as f:
        data = f.read()

    #removing the first column 
    index_new_line = data.find("\n")
    data = data[index_new_line+1:]
    #replacing js characters
    data = data.replace("%3B",";")
    data = data.replace(";","\t")
    data = data.replace("%20"," ")
    data = data.replace(",","\t")
    #removing unnecassary prefixes
    data = data.replace("ID=","")
    data = data.replace("Tile=","")
    data = data.replace("Name=","")
    data = data.replace("(@ Neural progenitor cells)","")

    with open(target_path,"w") as pp:
        pp.write(data)

    return

if __name__ == "__main__":
    run()
 


 



