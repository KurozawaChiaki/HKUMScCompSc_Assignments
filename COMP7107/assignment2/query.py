import sys
import numpy as np
import utils

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

def get_intersecting_cells(query_window, grid_bounds, intervals):
    """Determine grid cells that intersect with the query window"""
    x_min, x_max, y_min, y_max = grid_bounds
    x_interval, y_interval = intervals
    x_low, x_high, y_low, y_high = query_window
    
    # Calculate intersecting grid range
    start_x = max(0, min(9, int((x_low - x_min) / x_interval)))
    end_x = max(0, min(9, int((x_high - x_min) / x_interval)))
    start_y = max(0, min(9, int((y_low - y_min) / y_interval)))
    end_y = max(0, min(9, int((y_high - y_min) / y_interval)))
    
    # For each intersecting cell, determine if it's fully or partially covered
    intersecting_cells = []
    for x in range(start_x, end_x + 1):
        for y in range(start_y, end_y + 1):
            cell_x_min = x_min + x * x_interval
            cell_x_max = x_min + (x + 1) * x_interval
            cell_y_min = y_min + y * y_interval
            cell_y_max = y_min + (y + 1) * y_interval
            
            # Check if cell is fully covered
            fully_covered = (x_low <= cell_x_min and x_high >= cell_x_max and
                           y_low <= cell_y_min and y_high >= cell_y_max)
            
            intersecting_cells.append((x, y, fully_covered))
            
    return intersecting_cells

def verify_result(query_window):
    """Verify results by directly scanning the original file"""
    x_low, x_high, y_low, y_high = query_window
    points_in_window = set()
    
    with open('Beijing_restaurants.txt', 'r') as f:
        n = int(f.readline())
        for i in range(n):
            x, y = map(float, f.readline().strip().split())
            if x_low <= x <= x_high and y_low <= y <= y_high:
                points_in_window.add(i + 1)
                
    return points_in_window

def main():
    if len(sys.argv) != 5:
        print("Usage: python query.py <x_low> <x_high> <y_low> <y_high>")
        return
        
    # Parse query window parameters
    query_window = tuple(map(float, sys.argv[1:]))
    x_low, x_high, y_low, y_high = query_window
    
    # Read grid information
    grid_bounds, intervals, cells = read_grid_dir()
    
    # Get intersecting cells
    intersecting_cells = get_intersecting_cells(query_window, grid_bounds, intervals)
    
    # Process each intersecting cell
    result_points = set()
    with open('grid.grd', 'r') as grd_file:
        for x, y, fully_covered in intersecting_cells:
            if (x, y) not in cells:
                continue
                
            points = utils.read_points_from_cell(cells[(x, y)], grd_file)
            
            if fully_covered:
                # For fully covered cells, include all points
                result_points.update([point_id for point_id, _, _ in points])
            else:
                # For partially covered cells, check each point
                for point_id, px, py in points:
                    if x_low <= px <= x_high and y_low <= py <= y_high:
                        result_points.add(point_id)

    
    # Verify results
    # actual_points = verify_result(query_window)
    
    print(f"Query Window: {query_window}")
    print(f"Number of Intersecting Cells: {len(intersecting_cells)}")
    print(f"Number of Points Found: {len(result_points)}")
    # print(f"Verification Result: {'Correct' if result_points == actual_points else 'Incorrect'}")
    # print(f"Actual Number of Points: {len(actual_points)}")

if __name__ == "__main__":
    main() 