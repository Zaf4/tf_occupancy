import polars as pl
import os
import numpy as np
from utility import timer

#DEFINE globals
LINE = '<div class="line" style="width: {}px; margin-left: {}px; margin-top: {}px; title="This is a line tooltip."></div>'
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
    """Reduces the size of chr (chromosome) dataframe for testing
    Returns full scale dataframe if max_size == 0"""
    if max_size == 0:
        return chr
    else:
        return chr.filter(pl.col("End")<max_size)

def new_line(start:int,width:int,margin_top:int=0)->str:
    line = "\t"+LINE.format(width,start,margin_top)+"\n"
    return line

@timer
def draw_lines(chr:pl.DataFrame,template:str)->str:
    lines = ""
    previous_start = 0
    previous_end = 0
    line_count = 0

    for (start,),(width,) in zip(chr.select("Start").iter_rows(),chr.select("Range").iter_rows()):
        end = start+width
        #if no overlap, if -> (completely on left) and (completely on right)
        if (start < previous_end) and (end>previous_start):
            line = new_line(start,width,margin_top=2) # 2px spacing between lines
            line_count += 1 #count the number of lines on top of each other
        else:
            #6 comes from 4 (line height) + 2 (margin spacing) and 4 to remove single line spacing
            # ... update start here ...
            line = new_line(start,width,margin_top=line_count*-6-4) # subtracted to reset to top
            line_count=0  # reset if the new line is non-overlapping
        
        lines+=line
        previous_end=end
    
    return template.replace("{line}",lines)

def chr_slices(chr:pl.DataFrame)->np.ndarray:
    previous_start = 0
    previous_end = 0
    ranges_list = []

    overlap_range = [np.inf,np.ninf] #min,max

    for (start,),(width,) in zip(chr.select("Start").iter_rows(),chr.select("Range").iter_rows()):
        
        end = start+width
        #if no overlap, if -> (completely on left) and (completely on right)
        if (start < previous_end) and (end>previous_start):
            if start<overlap_range[0]:
                overlap_range[0] = start
            if end>overlap_range[1]:
                overlap_range[1] = end
        else:
            ranges_list.append(overlap_range)
            overlap_range = [np.inf,np.ninf] # reset overlap_range

        previous_end=end
    
    slices  = np.array(ranges_list)
    # ... update slices to reduce the spacing between neigboring slices 10px here...
    return slices


@timer
def draw_chr(chr:pl.DataFrame,template:str)->None:
    # ... update this function to draw multiple slices with same Y value ...
    width = chr.select("End").max()[0,0]
    chr_line = "\t"+CHROMOSOME.format(width)+"\n"
    return template.replace("{chr}",chr_line)

def main()->None:
    # ... this function also should be updated with new callings ...
    html = read_html() #template html file

    chr1 = read_data("chr1.csv")
    chr1 = down_scale(chr1,0)
    
    html = draw_chr(chr1,html)
    html = draw_lines(chr1,html)
    

    with open ("CHR1.html","w",encoding="utf-8") as final:
        final.write(html)

    return

if __name__ == "__main__":
    main()



