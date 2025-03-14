from typing import List, Any
from math import sqrt

# Mapping nominal/ordinal values to integers
season_map = {
    "spring": 0,
    "summer": 1,
    "autumn": 2,
    "winter": 3
}
seasons = ["spring", "summer", "autumn", "winter"]

river_size_map = {
    "small_": 0,
    "medium": 1,
    "large_": 2
}
river_size = ["small_", "medium", "large_"]

flow_velocity_map = {
    "low___": 0,
    "medium": 1,
    "high__": 2
}
flow_velocity = ["low__", "medium", "high__"]

# Attribute types: 0 - nominal, 1 - ordinal, 2 - interval
attribute_types: List[int] = [0, 1, 1] + [2] * 15


class Dataset:
    def __init__(self, data_path: str):
        self.data: List[Any] = self.input_data(data_path)
        self.min_values: List[Any] = []
        self.max_values: List[Any] = []

    def fix_merged_values(self, value_with_points: str) -> List[str]:
        dot_index: int = value_with_points.find(".")

        # If there is no decimal point (but this situation shouldn't happen).
        if dot_index == -1:
            return []
    
        # Keep everything up to that decimal + 5 more characters
        part_limit: int = dot_index + 1 + 5  # decimal + 5 digits
        start_index: int = dot_index - 3  # 3 digits before decimal point
        if start_index < 0:
            start_index = 0
            part_limit -= start_index
        float_str: str = value_with_points[start_index:part_limit]

        return [float_str] + self.fix_merged_values(value_with_points[start_index + part_limit:])

    def parse_attribute(self, index: int, raw_value: str) -> List[Any]:
        # If it's a missing value
        if raw_value.strip() == "XXXXXXX":
            return [-1]

        # If it's a wrongly-merged value
        if raw_value.count('.') >= 2:
            fixed_vals: List[str] = self.fix_merged_values(raw_value.strip())
            # We'll return them all as floats (interval values). 
            # We'll just treat them as a slice in the row. We'll handle them in the main loop.
            return fixed_vals

        # 3) Otherwise parse based on attribute_types:
        attr_type: int = attribute_types[index]

        if attr_type == 0:
            val_str = raw_value.strip().lower()
            if val_str in season_map:
                return [season_map[val_str]]
            else:
                return [-1]
        elif attr_type == 1:
            val_str = raw_value.strip().lower()
            if index == 1:
                if val_str in river_size_map:
                    return [river_size_map[val_str]]
                else:
                    return [-1]
            else:
                if val_str in flow_velocity_map:
                    return [flow_velocity_map[val_str]]
                else:
                    return [-1]
        else:
            try:
                return [float(raw_value)]
            except ValueError:
                return [-1]

    def input_data(self, filename: str) -> List[Any]:
        objects: List[Any] = []  

        with open(filename, 'r', encoding='utf-8') as f:
            line_number: int = 0
            for line in f:
                line = line.strip()

                # Skip empty lines
                if not line:
                    continue

                # Split the line by comma
                parts: List[str] = line.split(',')

                parsed_values: List[Any] = []
                attr_index: int = 0 

                i: int = 0
                while i < len(parts) and attr_index < 18:
                    # parse each part depending on the attribute type
                    current_part: str = parts[i]
                    vals: List[str] = self.parse_attribute(attr_index, current_part)

                    if len(vals) > 1 and attribute_types[attr_index] == 2:
                        for val in vals:
                            try:
                                f = float(val)
                            except ValueError:
                                f = -1
                            parsed_values.append(f)
                        attr_index += len(vals)
                    else:
                        # We have a list of exactly one parsed value
                        try:
                            if attribute_types[attr_index] == 2:
                                val = float(vals[0])
                            else:
                                val = int(vals[0])
                        except ValueError:
                            val = -1
                        parsed_values.append(val)
                        attr_index += 1

                    i += 1

                # If for some reason the line had fewer parts or we didn't fill all 18 attributes,
                # pad with -1 for the rest
                while attr_index < 18:
                    parsed_values.append("-1")
                    attr_index += 1

                objects.append(parsed_values)
                line_number += 1

        return objects
    
    def get_data(self):
        for record in self.data:
            print(record)

    def get_min_values(self) -> List[Any]:
        if len(self.min_values) != 0:
            return self.min_values
        
        self.min_values = [None] * 18
        
        for record in self.data:
            for i in range(18):
                if self.min_values[i] is None or (record[i] != -1 and record[i] < self.min_values[i]):
                    self.min_values[i] = record[i]

        return self.min_values
    
    def get_max_values(self) -> List[Any]:
        if len(self.max_values) != 0:
            return self.max_values
        
        self.max_values = [None] * 18
        
        for record in self.data:
            for i in range(18):
                if self.max_values[i] is None or (record[i] != -1 and record[i] > self.max_values[i]):
                    self.max_values[i] = record[i]

        return self.max_values
    
    def missing_values(self) -> int:
        count: int = 0
        
        for record in self.data:
            for i in range(18):
                if record[i] == -1:
                    count += 1

        return count
    
    def get_record(self, index: int) -> List[Any]:
        res: List[Any] = []
        for i in range(18):
            if i == 0:
                res.append(seasons[self.data[index][i]])
            elif i == 1:
                res.append(river_size[self.data[index][i]])
            elif i == 2:
                res.append(flow_velocity[self.data[index][i]])
            else:
                if self.data[index][i] == -1:
                    res.append("XXXXXXX")
                else:
                    res.append("{:.5f}".format(self.data[index][i]))

        return res
    
    def get_similarity(self, index1: int, index2: int) -> float:
        record1: List[Any] = self.data[index1]
        record2: List[Any] = self.data[index2]
        self.get_min_values()
        self.get_max_values()
        
        similarity: float = 0.0
        arrtibute_count: int = 0
        for i in range(18):
            if record1[i] == -1 or record2[i] == -1:
                continue

            if i == 0:
                similarity += 1 if record1[i] == record2[i] else 0
            elif i == 1 or i == 2:
                similarity += (1 - abs(record1[i] - record2[i]) / 2)
            else:
                similarity += 1 - abs(record1[i] - record2[i]) / (self.max_values[i] - self.min_values[i])
            arrtibute_count += 1

        return similarity / arrtibute_count
    
    def get_similarity_with_record(self, index1: int, record: List[Any]) -> float:
        record1: List[Any] = self.data[index1]
        self.get_min_values()
        self.get_max_values()
        
        similarity: float = 0.0
        arrtibute_count: int = 0
        for i in range(18):
            if record1[i] == -1 or record[i] == -1:
                continue

            if i == 0:
                similarity += 1 if record1[i] == record[i] else 0
            elif i == 1 or i == 2:
                similarity += (1 - abs(record1[i] - record[i]) / 2)
            else:
                similarity += 1 - abs(record1[i] - record[i]) / (max(self.max_values[i], record[i]) - min(self.min_values[i], record[i]))
            arrtibute_count += 1

        return similarity / arrtibute_count
    
    def len(self) -> int:
        return len(self.data)
    
    def get_euclidean_distance(self, index1: int, index2: int) -> float:
        record1: List[Any] = self.data[index1]
        record2: List[Any] = self.data[index2]
        self.get_min_values()
        self.get_max_values()
        
        distance: float = 0.0
        for i in range(18):
            if record1[i] == -1 or record2[i] == -1:
                continue

            if i <= 2:
                continue

            d1: float = (record1[i] - self.min_values[i]) / (self.max_values[i] - self.min_values[i])
            d2: float = (record2[i] - self.min_values[i]) / (self.max_values[i] - self.min_values[i])
            distance += (d1 - d2) ** 2

        return sqrt(distance)
    
    def get_distance_with_record(self, index: int, record: List[Any]) -> float:
        record1: List[Any] = self.data[index]
        self.get_min_values()
        self.get_max_values()
        
        distance: float = 0.0
        for i in range(18):
            if record1[i] == -1 or record[i] == -1:
                continue

            if i <= 2:
                continue
            
            current_min = min(self.min_values[i], record[i])
            current_max = max(self.max_values[i], record[i])
            d1: float = (record1[i] - current_min) / (current_max - current_min)
            d2: float = (record[i] - current_min) / (current_max - current_min)
            distance += (d1 - d2) ** 2

        return sqrt(distance)