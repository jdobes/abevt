#!/usr/bin/env python3

import csv
import matplotlib.pyplot as plt
import numpy as np
from os import listdir
from os.path import isfile, join


def init_graph(title):
    plt.xlabel("FES")
    plt.ylabel("cost function")
    plt.grid(True)
    #plt.axis(GRAPH_BOUNDS[f"{fun_name}_{dimensions}"])
    plt.title(title)


def main():
    mypath = "output/"
    csv_files = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f)) and f.endswith(".csv")]

    for csv_file in csv_files:
        with open(csv_file, newline='') as f:
            run_averages = []
            reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)
            for row in reader:
                run_average = np.mean(np.array(row[1:]).astype(np.float))
                run_averages.append(run_average)
            init_graph(f"{csv_file[:-4]}, average best run")
            plt.plot(range(1, len(run_averages)+1), run_averages, linewidth=1)
            plt.savefig(f"{csv_file[:-4]}.png")
            plt.clf()
            plt.cla()
            plt.close()

if __name__ == "__main__":
    main()
