import sys
import heapq
import numpy as np
from dataclasses import dataclass
from typing import Tuple, Set, Generator
import utils

@dataclass
class Cell:
    x: int
    y: int
    distance: float
    
    def __lt__(self, other):
        return self.distance < other.distance

@dataclass
class Point:
    id: int
    x: float
    y: float
    distance: float
    
    def __lt__(self, other):
        return self.distance < other.distance

def mindist(qx: float, qy: float, cell_bounds: Tuple[float, float, float, float]) -> float:
    """
    Calculate minimum distance from query point to cell
    cell_bounds: (min_x, max_x, min_y, max_y)
    """
    dx = dy = 0
    min_x, max_x, min_y, max_y = cell_bounds
    
    # Calculate x-distance
    if qx < min_x:
        dx = min_x - qx
    elif qx > max_x:
        dx = qx - max_x
        
    # Calculate y-distance
    if qy < min_y:
        dy = min_y - qy
    elif qy > max_y:
        dy = qy - max_y
        
    return np.sqrt(dx * dx + dy * dy)

def get_cell_bounds(cell: Tuple[int, int], grid_bounds: Tuple[float, float, float, float], 
                   intervals: Tuple[float, float]) -> Tuple[float, float, float, float]:
    """Calculate the boundaries of a cell"""
    x_min, x_max, y_min, y_max = grid_bounds
    x_interval, y_interval = intervals
    cell_x, cell_y = cell
    
    cell_x_min = x_min + cell_x * x_interval
    cell_x_max = x_min + (cell_x + 1) * x_interval
    cell_y_min = y_min + cell_y * y_interval
    cell_y_max = y_min + (cell_y + 1) * y_interval
    
    return (cell_x_min, cell_x_max, cell_y_min, cell_y_max)

def get_neighbor_cells(cell: Tuple[int, int]) -> list:
    """Get valid neighboring cells"""
    x, y = cell
    neighbors = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x <= 9 and 0 <= new_y <= 9:
                neighbors.append((new_x, new_y))
    return neighbors

def nearest_neighbor_search(qx: float, qy: float, grid_bounds: Tuple[float, float, float, float],
                          intervals: Tuple[float, float], cells: dict) -> Generator[Point, None, None]:
    """Generator function that yields nearest neighbors incrementally"""
    # Priority queue for cells and points
    pq = []
    visited_cells = set()
    
    # Find the cell containing q
    x_min, x_max, y_min, y_max = grid_bounds
    x_interval, y_interval = intervals
    
    cell_x = min(9, max(0, int((qx - x_min) / x_interval)))
    cell_y = min(9, max(0, int((qy - y_min) / y_interval)))
    start_cell = (cell_x, cell_y)
    
    # Add starting cell to queue if it exists
    if start_cell in cells:
        cell_bounds = get_cell_bounds(start_cell, grid_bounds, intervals)
        dist = mindist(qx, qy, cell_bounds)
        heapq.heappush(pq, Cell(cell_x, cell_y, dist))
        visited_cells.add(start_cell)
    
    with open('grid.grd', 'r') as grd_file:
        while pq:
            current = heapq.heappop(pq)
            
            if isinstance(current, Point):
                # If it's a point, yield it as the next nearest neighbor
                yield current
            else:
                # If it's a cell, process its points and neighbors
                cell = (current.x, current.y)
                print(f"Reading cell: {cell}")  # Print cells being read
                
                # Read and add points from the cell
                points = utils.read_points_from_cell(cells[cell], grd_file)
                for point_id, px, py in points:
                    dist = np.sqrt((qx - px)**2 + (qy - py)**2)
                    heapq.heappush(pq, Point(point_id, px, py, dist))
                
                # Add unvisited neighbor cells
                for neighbor in get_neighbor_cells(cell):
                    if neighbor not in visited_cells and neighbor in cells:
                        visited_cells.add(neighbor)
                        cell_bounds = get_cell_bounds(neighbor, grid_bounds, intervals)
                        dist = mindist(qx, qy, cell_bounds)
                        heapq.heappush(pq, Cell(neighbor[0], neighbor[1], dist))

def main():
    if len(sys.argv) != 4:
        print("Usage: python knn.py <k> <query_x> <query_y>")
        return
    
    # Parse command line arguments
    k = int(sys.argv[1])
    qx = float(sys.argv[2])
    qy = float(sys.argv[3])
    
    # Read grid information
    grid_bounds, intervals, cells = utils.read_grid_dir()
    
    # Find k nearest neighbors
    print(f"\nFinding {k} nearest neighbors to point ({qx}, {qy}):")
    print("\nCells read during search:")
    
    nn_generator = nearest_neighbor_search(qx, qy, grid_bounds, intervals, cells)
    
    print("\nNearest neighbors (in order):")
    for i in range(k):
        try:
            point = next(nn_generator)
            print(f"{i+1}. Point {point.id}: ({point.x}, {point.y}), distance: {point.distance:.6f}")
        except StopIteration:
            print(f"\nOnly found {i} points. No more points available.")
            break

if __name__ == "__main__":
    main() 