"""Value Change Dump to Data Frame (Pandas)"""

__version__ = "1.0"

import pandas as pd

def get_vars(fptr):
    line = fptr.readline()
    vars = {} # insertion order >= 3.7
    while "$enddefinitions" not in line:
        if "var" in line:
            parts = line.split()
            if parts[4] not in vars.values():
                vars[parts[3]] = parts[4]
        line = fptr.readline()
    return vars

def vcd2df(f_name):
    fptr = open(f_name, "r")
    vars = get_vars(fptr)
    names = vars.copy()
    vars = {var:-1 for var in vars.keys()}
    df = {}
    while "$dumpvars" not in fptr.readline():
        pass
    time = "#0"
    while (line := fptr.readline()):
        if "#" in line[0]: # Check for tick
            df[time] = pd.Series(vars.values())
            time = line.strip()
        else: # Else two cases, words and bits
            if " " in line: # word
                val, var = line[1:].strip().split()
            else: # bit
                val, var = line[0], line[1:].strip()
            if var in vars:
                vars[var] = int(val, 2) if val.isdigit() else -1
    df = pd.DataFrame(df, dtype=int)
    df.index = names.values()
    return df
