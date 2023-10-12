import polars as pl
import os
from utility import timer

#DEFINE globals
LINE = '<div class="line" style="width: {}px; margin-left: {}px;"></div>'
CHROMOSOME = '<div class="chr" style="width: {}px;"></div>'

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


def new_line(start:int,width:int)->str:
    line = "\t"+LINE.format(width,start)+"\n"
    return line

@timer
def draw_lines(chr:pl.DataFrame,template:str)->str:
    lines = ""
    for start,width in zip(chr.select("Start").iter_rows(),chr.select("Range").iter_rows()):
        lines+=new_line(start[0],width[0])
    
    return template.replace("{line}",lines)

@timer
def draw_chr(chr:pl.DataFrame,template:str)->None:
    width = chr.select("End").max()[0,0]
    chr_line = "\t"+CHROMOSOME.format(width)+"\n"

    return template.replace("{chr}",chr_line)

@timer
def main()->None:
    template = read_html() #template html file

    chr1 = read_data("chr1.csv")
    chr1 = down_scale(chr1,200_000)
    
    new_html = draw_lines(chr1,template)
    new_html = draw_chr(chr1,new_html)

    with open ("CHR1.html","w",encoding="utf-8") as final:
        final.write(new_html)

    return

if __name__ == "__main__":
    main()



