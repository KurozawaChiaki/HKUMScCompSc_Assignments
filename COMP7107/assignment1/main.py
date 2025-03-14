import sys
from typing import List, Any
from dataset import Dataset, attribute_types

def task1(data: Dataset) -> None:
    print("type of attributes: ", attribute_types)
    print("minimum values per attribute: ", data.get_min_values())
    print("maximum values per attribute: ", data.get_max_values())
    print("total number of missing values: ", data.missing_values())

def task2(data: Dataset, record_input: List[Any]) -> None:
    maximums: List[Any] = [None, None, None]
    minimums: List[Any] = [None, None, None]
    request: List[Any] = [None, None]
    
    for i in range(data.len()):
        for j in range(i, data.len()):
            if i != j:
                similarity: float = data.get_similarity(i, j)
                if maximums[0] is None or similarity > maximums[0]:
                    maximums[0] = similarity
                    maximums[1] = i
                    maximums[2] = j
                if minimums[0] is None or similarity < minimums[0]:
                    minimums[0] = similarity
                    minimums[1] = i
                    minimums[2] = j
        similarity: float = data.get_similarity_with_record(i, record_input)
        if request[0] is None or similarity > request[0]:
            request[0] = similarity
            request[1] = i

    print("maximum similarity: " + str(maximums[0]) + "; pair with maximum similarity: [" + str(maximums[1]) + ", " + str(maximums[2]) + "]")
    print("object " + str(maximums[1]) + " = " + str(data.get_record(maximums[1])))
    print("object " + str(maximums[2]) + " = " + str(data.get_record(maximums[2])))

    print("minimum similarity: " + str(minimums[0]) + "; pair with minimum similarity: [" + str(minimums[1]) + ", " + str(minimums[2]) + "]")
    print("object " + str(minimums[1]) + " = " + str(data.get_record(minimums[1])))
    print("object " + str(minimums[2]) + " = " + str(data.get_record(minimums[2])))

    print("highest similarity to input object: " + str(request[0]) + "; object with highest similarity: " + str(request[1]))
    print("object " + str(request[1]) + " = " + str(data.get_record(request[1])))

def task3(data: Dataset, record_input: List[Any]) -> None:
    maximums: List[Any] = [None, None, None]
    minimums: List[Any] = [None, None, None]
    request: List[Any] = [None, None]
    
    for i in range(data.len()):
        for j in range(i, data.len()):
            if i != j:
                distance: float = data.get_euclidean_distance(i, j)
                if maximums[0] is None or distance > maximums[0]:
                    maximums[0] = distance
                    maximums[1] = i
                    maximums[2] = j
                if minimums[0] is None or distance < minimums[0]:
                    minimums[0] = distance
                    minimums[1] = i
                    minimums[2] = j
        distance: float = data.get_distance_with_record(i, record_input)
        if request[0] is None or distance < request[0]:
            request[0] = distance
            request[1] = i

    print("maximum distance: " + str(maximums[0]) + "; pair with maximum distance: [" + str(maximums[1]) + ", " + str(maximums[2]) + "]")
    print("object " + str(maximums[1]) + " = " + str(data.get_record(maximums[1])))
    print("object " + str(maximums[2]) + " = " + str(data.get_record(maximums[2])))

    print("minimum distance: " + str(minimums[0]) + "; pair with minimum distance: [" + str(minimums[1]) + ", " + str(minimums[2]) + "]")
    print("object " + str(minimums[1]) + " = " + str(data.get_record(minimums[1])))
    print("object " + str(minimums[2]) + " = " + str(data.get_record(minimums[2])))

    print("smallest distance to input object: " + str(request[0]) + "; object with smallest distance: " + str(request[1]))
    print("object " + str(request[1]) + " = " + str(data.get_record(request[1])))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 process_coil.py <datafile>")
        sys.exit(1)

    data_filename: str = sys.argv[1]
    data = Dataset(data_filename)
    # winter,large_,high__,8.10000,7.50000,140.00000,1.00000,60.00000,100.00000,140.00000,31.00000,1.00000,10.00000,3.00000,1.00000,0.00000,0.00000,5.00000
    record_input: List[Any] = [3, 2, 2, 8.1, 7.5, 140, 1.0, 60.0, 100.0, 140.0, 31.0, 1.0, 10.0, 3.0, 1.0, 0.0, 0.0, 5.0]

    
    print("Tasks:\n1)data loading, cleaning, and transformation\n2)computation of similarity\n3)computation of Euclidean distance\n\n0)Exit")
    while(True):
        print("---------------------------------")
        task = int(input("Enter the task number: "))

        if task == 0:
            break
        
        if task == 1:
            task1(data)
        elif task == 2:
            task2(data, record_input)
        elif task == 3:
            task3(data, record_input)     