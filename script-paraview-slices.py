from paraview.simple import *
import numpy as np
import sys
import os
import string
import matplotlib.pyplot as plt

if len(sys.argv) != 4:
    print("Not enough arguments")
    sys.exit(1)

vtkfilepath = sys.argv[1]
slicesfilepath = sys.argv[2]
label = sys.argv[3]

vtk_file = LegacyVTKReader(FileNames=[vtkfilepath])

with open(slicesfilepath, 'r') as file:
    line = file.readline()
    temp = line.split()
    nslices = int(temp[0])
    slices = np.empty((int(nslices), 6))

    for i in range(int(nslices)):
        line = file.readline()
        temp = line.split()
        for j in range(6):
            slices[i, j] = float(temp[j])
        resolution = int(temp[6])

slices_filter = Slice(Input=vtk_file)

for i in range(int(nslices)):
    slices_filter.SliceType.Origin = [slices[i, 0], slices[i, 1], slices[i, 2]]
    slices_filter.SliceType.Normal = [slices[i, 3], slices[i, 4], slices[i, 5]]
    
    Show(slices_filter)

    slice_data = GetActiveSource()

    slice_data2 = servermanager.Fetch(slice_data)

    coords = slice_data2.GetPoints().GetData()
    point_data = slice_data2.GetPointData().GetArray(label)

    coords_np = np.array([coords.GetTuple3(i) for i in range(coords.GetNumberOfTuples())])
    point_data_np = np.array([point_data.GetTuple1(i) for i in range(point_data.GetNumberOfTuples())])

    data_array = np.column_stack((coords_np, point_data_np))

    output_file_path = vtkfilepath.replace(".vtk","_" + str(i) + ".txt")

    output_file_path2 = vtkfilepath.replace(".vtk","_" + str(i) + ".png")

    np.savetxt(output_file_path, data_array, header="X Y Z " + label, comments="")

    plt.figure(figsize=(8, 6))

    plt.scatter(data_array[:, 0], data_array[:, 3], marker='o', color='b', label=label)

    plt.grid(True)
    plt.legend()
    plt.savefig(output_file_path2)

