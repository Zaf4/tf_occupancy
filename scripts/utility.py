from time import perf_counter_ns as pns

def timer(func):
    def wrapper(*args,**kwargs):
        start = pns()
        whatever = func(*args,**kwargs) 
        time_diff = pns()-start
        if time_diff < 1e9: # less than a second
				  # prints the function name and its runtime
          print(f'{func.__name__}:\t{(time_diff*1e-6):.2f}ms')
        else:
           print(f'{func.__name__}:\t{(time_diff*1e-9):.2f}s')
        return whatever # returns whatever the 'func' returns
    return wrapper # returns the inner/wrapper function