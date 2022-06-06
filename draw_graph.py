import numpy as np
import matplotlib.pyplot as plt
import sys
from os import walk
from matplotlib_venn import venn2, venn3, venn3_circles
import random


def main():
    """
    argv[1]: path to data, argv[2]: 'line' or 'cdf' or 'venn'
    :return:
    """
    data_path = sys.argv[1]
    graph_option = sys.argv[2]
    graph_type = data_path.split('./data/')[1]
    config_dict = set_configuration(graph_type)
    file_path = get_file(data_path)
    if graph_option == 'line':
        draw_line_chart(file_path, data_path, config_dict, graph_type)
    elif graph_option == 'cdf':
        draw_cdf_chart( file_path, data_path, config_dict )
    elif graph_option == 'venn':
        draw_venn_chart(file_path, data_path, config_dict)

def draw_venn_chart(file_path, data_path, config_dict):
    data_set = []
    group_name = []
    for index, file in enumerate( file_path ):
        with open(data_path + '/' + file) as f:
            lines = f.readlines()
        data = [i.strip("\n") for i in lines]
        data_set.append(set(data))
        group_name.append(file.split(".")[0])
        print(len(set(data)), file.split(".")[0])
    if len(data_set)==2:
        out = venn2(data_set,group_name)
    elif len(data_set)==3:
        out = venn3(data_set,group_name)
    for text in out.set_labels:
        if text:
            text.set_fontsize( 20 )
    for text in out.subset_labels:
        if text:
            text.set_fontsize( 16 )
    plt.savefig( "./result/" + config_dict['save_to'] + ".eps", format='eps' )
    plt.show()


def draw_cdf_chart(file_path, data_path, config_dict):
    line_style = get_line_style(len(file_path))
    if len(file_path)==1:
        line_style = [(2,2)]
    for index, file in enumerate(file_path):
        with open(data_path + '/' + file) as f:
            lines = f.readlines()
        data_set = lines[0][1:-1].split(", ")
        axis_x = [float(i) for i in data_set]
        axis_x.sort()
        axis_y = [(i+1)/(len(axis_x)+34)*100 for i in range(len(axis_x))]
        axis_x.append(600)
        axis_y.append(axis_y[-1])
        plt.plot(axis_x,axis_y,label=file.split('.')[0], dashes=line_style[index])
        plt.ylim( ymin=0, ymax = 100 )
        plt.xlim( xmin=0, xmax = 600)
    # plt.title(config_dict['graph_name'])
    plt.xlabel(config_dict['axis_x'], fontsize=16)
    plt.ylabel(config_dict['axis_y'], fontsize=16)
    # plt.legend(loc=config_dict['legend'])
    plt.grid()
    plt.savefig( "./result/" + config_dict['save_to'] + ".eps", format='eps' )
    plt.show()


def draw_line_chart(file_path, data_path, config_dict, graph_type):
    line_style = get_line_style(len(file_path))
    y_list = []
    x_list = []
    for index, file in enumerate(file_path):
        with open(data_path + '/' + file) as f:
            lines = f.readlines()
        axis_x = []
        axis_y = []
        based_value = float(lines[1].split(" ")[2].strip("\n"))
        for key, value in enumerate(lines[1:]):
            datalist = value.split(" ")
            axis_y.append(float(datalist[1]))
            axis_x.append(float(datalist[2].strip("\n")) - based_value)
        y_list.append(axis_y)
        x_list.append(axis_x)
        plt.plot( axis_x, axis_y, label=file.split('.')[0], dashes=line_style[index])
    if graph_type == 'code_cov':
        x1 = x_list[0]
        x2 = x_list[1]
        y1 = y_list[0]
        y2 = y_list[1]
        xfill = np.sort( np.concatenate( [x1, x2] ) )
        y1fill = np.interp( xfill, x1, y1 )
        y2fill = np.interp( xfill, x2, y2 )
        plt.fill_between( xfill, y1fill, y2fill, where=y1fill < y2fill, interpolate=True, color='dodgerblue', alpha=0.2, hatch="/",edgecolor='red' )
        plt.fill_between( xfill, y1fill, y2fill, where=y1fill > y2fill, interpolate=True, color='crimson', alpha=0.2, hatch="/",edgecolor='red' )
    # plt.title(config_dict['graph_name'])
    # plt.xlim( xmin=0)
    plt.xlabel(config_dict['axis_x'], fontsize=16)
    plt.ylabel(config_dict['axis_y'], fontsize=16)
    plt.legend(loc=config_dict['legend'])
    plt.grid()
    plt.savefig( "./result/" + config_dict['save_to'] + ".eps", format='eps' )
    plt.show()


def set_configuration(graph_type):
    """
    set configuration for graph within configure.txt
    :return:
    """
    config_dict = {}
    with open("./configure.txt") as f:
        lines = f.readlines()
    flag = 0
    for config in lines:
        if config.strip('\n') == '//' + graph_type:
            flag = 1
            continue
        elif config[:2] == '//':
            flag = 0
            continue
        elif flag == 0:
            continue
        key, value = config.strip("\n").split(" = ")
        config_dict[key] = value
    return config_dict

def get_line_style(line_num):
    """
    line_num line style
    :return:
    """
    # line1.set_dashes([2, 2, 10, 2])  # 2pt line, 2pt break, 10pt line, 2pt break

    style = []
    for i in range(line_num):
        tmp = []
        for j in range(4):
            tmp.append(random.randint(1,10))
        style.append(tmp)
    return style
    # return [(5,2),(2,2),(4,6),(3,3,2,2),(5,2,20,2)]

def get_file(data_path):
    """
    get file in data folder
    :param data_path:
    :return:
    """
    file_path = []
    for (dirpath, dirnames, filenames) in walk(data_path):
        filenames = [i for i in filenames if not i.startswith(".")]
        file_path += filenames
    return file_path


if __name__ == "__main__":
    main()