import polars as pl
import os
from utility import timer

#DEFINE CONSTANT
LINE = '<div class="line" style="width: {}px; margin-left: {}px;"></div>'

@timer
def read_html(fname: str|os.PathLike="./template.html")->str:
    with open (fname,'r') as template:
        text = template.read()
    return text

@timer
def read_data(file: str|os.PathLike,
              folder: str|os.PathLike= "./data/human_HG38/NPC",
              )->pl.DataFrame:
    return pl.read_csv(os.path.join(folder,file))

@timer
def down_scale(chr: pl.DataFrame,max_size:int=20_000)->pl.DataFrame:
    """Reduces the size of chr (chromosome) dataframe for testing"""
    return chr.filter(pl.col("End")<max_size)

@timer
def new_line(start:int,width:int)->str:
    line =  LINE.format(width,start)+"\n"
    return line

def draw_chr(chr:pl.DataFrame)->None:
    

@timer
def main()->None:
    chr1 = read_data("chr1.csv")
    chr1 = down_scale(chr1)
    # print(len(chr1))
    return

if __name__ == "__main__":
    main()



