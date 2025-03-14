def read_points_from_cell(cell_info, grd_file):
    """Read points from a specific cell in grid.grd file"""
    byte_pos, count = cell_info
    points = []
    
    # Seek to the byte position
    grd_file.seek(0)  # First seek to start to ensure consistent position
    current_pos = 0
    
    # Read and count bytes until we reach the target position
    while current_pos < byte_pos:
        line = grd_file.readline()
        current_pos += len(line.encode())  # Count actual bytes in the file
    
    # Now we're at the correct position, read the points
    for _ in range(count):
        line = grd_file.readline()
        if not line:  # End of file
            break
        values = line.strip().split()
        point_id, x, y = map(float, values)
        points.append((int(point_id), x, y))
        
    return points

def read_grid_dir():
    """Read grid.dir file and return grid information"""
    with open('grid.dir', 'r') as f:
        # Read boundary information
        bounds = list(map(float, f.readline().strip().split()))
        x_min, x_max, y_min, y_max = bounds
        
        # Calculate intervals
        x_interval = (x_max - x_min) / 10.0
        y_interval = (y_max - y_min) / 10.0
        
        # Read cell information
        cells = {}
        for line in f:
            cell_coords_x, cell_coords_y, pos, count = line.strip().split()
            x = int(cell_coords_x)
            y = int(cell_coords_y)
            cells[(x, y)] = (int(pos), int(count))
            
    return (x_min, x_max, y_min, y_max), (x_interval, y_interval), cells