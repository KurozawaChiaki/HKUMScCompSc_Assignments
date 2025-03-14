import numpy as np
from collections import defaultdict

def main():
    locations = []
    point_ids = []  # Store point IDs (line numbers)
    
    # read data
    with open('Beijing_restaurants.txt', 'r') as f:
        n = int(f.readline())
        
        for i in range(n):
            location_str = f.readline().split(' ')
            location = [float(location_str[0]), float(location_str[1])]
            locations.append(location)
            point_ids.append(i + 1)  # Line number as ID

    locations = np.array(locations)
    point_ids = np.array(point_ids)

    # Calculate grid boundaries
    x_min = min(locations[:, 0])
    x_max = max(locations[:, 0])
    y_min = min(locations[:, 1])
    y_max = max(locations[:, 1])

    x_interval = (x_max - x_min) / 10.0
    y_interval = (y_max - y_min) / 10.0

    # Group points by cell
    cells = defaultdict(list)
    for i in range(n):
        x = locations[i, 0]
        y = locations[i, 1]
        index_x = min(9, int((x - x_min) / x_interval))
        index_y = min(9, int((y - y_min) / y_interval))
        cells[(index_x, index_y)].append((point_ids[i], locations[i], (index_x, index_y)))

    # Sort cells by cell index and points within cells by identifier
    sorted_cells = []
    for cell_idx in sorted(cells.keys()):
        # Sort points within the cell by their original identifier
        cell_points = sorted(cells[cell_idx], key=lambda x: x[0])
        sorted_cells.extend(cell_points)

    # Write grid.grd file
    with open('grid.grd', 'w') as f:
        for point_id, location, _ in sorted_cells:
            f.write(f"{point_id} {location[0]} {location[1]}\n")

    # Prepare directory information
    cell_info = {}
    current_pos = 0
    cell_counts = {}

    # Calculate file positions and counts
    current_cell = None
    for point_id, location, cell in sorted_cells:
        line = f"{point_id} {location[0]} {location[1]}\n"
        
        if cell not in cell_info:
            cell_info[cell] = current_pos
            cell_counts[cell] = 1
        else:
            cell_counts[cell] += 1
            
        current_pos += len(line)

    # Write grid.dir file
    with open('grid.dir', 'w') as f:
        # Write boundaries
        f.write(f"{x_min} {x_max} {y_min} {y_max}\n")
        
        # Write cell information
        for cell in sorted(cell_info.keys()):
            f.write(f"{cell[0]} {cell[1]} {cell_info[cell]} {cell_counts[cell]}\n")

    print("Grid index files have been created successfully!")

if __name__ == '__main__':
    main()
