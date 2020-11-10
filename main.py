import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from file_handling import *
from selection import *
from sklearn.cluster import KMeans


def column_selection_type(start_index: int):
    # Ask whether to use all columns, exclude certain columns, or select certain columns
    selection_type = ["Enter 0 to use all columns in dataset.",
                      "Enter 1 to use all columns excluding selected columns.",
                      "Enter 2 to select columns for Clustering."]

    while True:
        try:
            for index, i in enumerate(selection_type):
                if start_index <= index:
                    print(i)
            index_selection = int(input("Enter Selection: "))
            selection_type[index_selection]
            if index_selection < start_index:
                int("Error")
        except (ValueError, IndexError):
            print("Input must be integer between " + str(start_index) + " and " + str(len(selection_type) - 1))
            continue
        else:
            break
    return index_selection


def main():
    print("Program: Clustering")
    print("Release: 1.0.0")
    print("Date: 2020-11-10")
    print("Author: Brian Neely")
    print()
    print()
    print("This program reads a csv file and performs clustering on it.")
    print()
    print()

    # Hide Tkinter GUI
    Tk().withdraw()

    # Find input file
    file_in = select_file_in()

    # Set output file
    file_out = select_file_out_csv(file_in)

    # Ask for delimination
    delimination = input("Enter Deliminator: ")

    # Open input csv using the unknown encoder function
    data = open_unknown_csv(file_in, delimination)

    # Ask whether to use all columns, exclude certain columns, or select certain columns
    column_selection_type_input = column_selection_type(0)

    # Get list of columns from PCA
    columns = column_list(data, column_selection_type_input)

    # Ask number of clusters
    while True:
        try:
            number_of_clusters = int(input("Input the number of clusters: "))
            if number_of_clusters < 2:
                print("The number of clusters needs to be greater than 1...")
            else:
                break
        except:
            print("The number of clusters needs to be an integer...")

    # Cluster Data
    kmeans = KMeans(n_clusters=number_of_clusters)
    kmeans.fit(data[columns])
    data["cluster"] = kmeans.predict(data[columns])

    # Write Data Out
    data.to_csv(file_out)


def column_list(data, column_selection_type_in):
    print("Reading Column List")
    headers = list(data.columns.values)
    if column_selection_type_in == 1:
        while True:
            try:
                print("Select columns to exclude from Clustering...")
                for j, i in enumerate(headers):
                    print(str(j) + ": to exclude column [" + str(i) + "]")

                # Ask for index list
                column_index_list_string = input("Enter selections separated by spaces: ")

                # Check if input was empty
                if not column_index_list_string:
                    print("No selection was used, all columns will be used.")

                # Split string based on spaces
                column_index_list = column_index_list_string.split()

                # Get column names list
                column_name_list_excld = list()
                for i in column_index_list:
                    column_name_list_excld.append(headers[int(i)])

                column_name_list = list()
                for i in headers:
                    if i not in column_name_list_excld:
                        column_name_list.append(i)

                # Check if columns are valid for PCA
                try:
                    invalid_selection = 0
                    # Test open every column and convert to number
                    for i in column_name_list:
                        test_column = i
                        for j in data[i]:
                            float(j)
                except:
                    print(test_column + ' is invalid for PCA, please select a new column list.')
                    invalid_selection = 1
                    continue

                if invalid_selection == 1:
                    break

            except ValueError:
                print("An invalid column input was detected, please try again.")
                continue

            else:
                break
    elif column_selection_type_in == 2:
        while True:
            try:
                print("Select columns to include into the PCA...")
                for j, i in enumerate(headers):
                    print(str(j) + ": to include column [" + str(i) + "]")

                # Ask for index list
                column_index_list_string = input("Enter selections separated by spaces: ")

                # Check if input was empty
                while not column_index_list_string:
                    column_index_list_string = input("Input was blank, please select columns to include.")

                # Split string based on spaces
                column_index_list = column_index_list_string.split()

                # Check to make sure at least to columns were selected
                while len(column_index_list) < 2:
                    column_index_list_string = input("Only 1 column was selected for PCA, a minimum of 2 is required.")
                    column_index_list = column_index_list_string.split()

                # Get column names list
                column_name_list = list()
                for i in column_index_list:
                    column_name_list.append(headers[int(i)])

                # Check if columns are valid for PCA
                try:
                    invalid_selection = 0
                    # Test open every column and convert to number
                    for i in column_name_list:
                        test_column = i
                        for j in data[i]:
                            float(j)
                except:
                    print(test_column + ' is invalid for PCA, please select a new column list.')
                    invalid_selection = 1
                    continue

                if invalid_selection == 1:
                    break

            except:
                print("An invalid column input was detected, please try again.")
                continue

            else:
                break

    else:
        columns = list(data.columns.values)

        # Check if columns are valid for PCA
        try:
            invalid_selection = 0
            # Test open every column and convert to number
            for i in columns:
                test_column = i
                for j in data[i]:
                    float(j)
        except ValueError:
            print(test_column + ' is invalid for PCA.')
            invalid_selection = 1

        if invalid_selection == 1:
            print("Due to invalid columns for PCA, please change your column selection type.")
            print()
            new_selection = column_selection_type(int(1))
            print("New Selection")
            column_name_list = column_list(data, new_selection)

    # Return column_name list to original function
    return column_name_list

if __name__ == '__main__':
    main()
