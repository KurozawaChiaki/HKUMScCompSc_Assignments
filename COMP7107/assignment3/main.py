import heapq
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py k")
        return

    k = int(sys.argv[1])
    
    # Read rnd.txt and store scores in array R
    R = []
    with open("rnd.txt", "r") as f:
        for line in f:
            obj_id, score = line.strip().split()
            obj_id = int(obj_id)
            score = float(score)
            # Ensure R is large enough
            while len(R) <= obj_id:
                R.append(0.0)
            R[obj_id] = score
    
    # Initialize variables
    seq1_file = open("seq1.txt", "r")
    seq2_file = open("seq2.txt", "r")
    
    seen_objects = {}  # Dictionary to store seen objects and their information
    total_accesses = 0
    last_score_seq1 = None
    last_score_seq2 = None
    
    # Read in round-robin fashion until we have seen k objects
    while len(seen_objects) < k:
        # Read from seq1
        line = seq1_file.readline()
        if line:
            total_accesses += 1
            obj_id, score = line.strip().split()
            obj_id = int(obj_id)
            score = float(score)
            last_score_seq1 = score
            
            if obj_id in seen_objects:
                seen_objects[obj_id]['score'] += score
                seen_objects[obj_id]['seen_seq1'] = True
            else:
                seen_objects[obj_id] = {
                    'score': score + R[obj_id],
                    'seen_seq1': True,
                    'seen_seq2': False
                }
        
        if len(seen_objects) >= k:
            break
            
        # Read from seq2
        line = seq2_file.readline()
        if line:
            total_accesses += 1
            obj_id, score = line.strip().split()
            obj_id = int(obj_id)
            score = float(score)
            last_score_seq2 = score
            
            if obj_id in seen_objects:
                seen_objects[obj_id]['score'] += score
                seen_objects[obj_id]['seen_seq2'] = True
            else:
                seen_objects[obj_id] = {
                    'score': score + R[obj_id],
                    'seen_seq1': False,
                    'seen_seq2': True
                }
    
    # Initialize min-heap Wk with the top-k objects so far
    Wk = []
    for obj_id, info in seen_objects.items():
        # We want a min-heap, so the object with the lowest score is at the top
        heapq.heappush(Wk, (info['score'], obj_id))
        if len(Wk) > k:
            heapq.heappop(Wk)
    
    # Continue round-robin access until termination
    while True:
        # Calculate threshold T
        T = last_score_seq1 + last_score_seq2 + 5.0
        
        # Check if the minimum score in Wk is greater than or equal to T
        if Wk[0][0] >= T:
            # Check if there exists any seen object not in Wk with upper bound > minimum in Wk
            wk_objects = set(obj_id for _, obj_id in Wk)
            min_score_in_wk = Wk[0][0]
            
            can_terminate = True
            for obj_id, info in seen_objects.items():
                if obj_id not in wk_objects:
                    upper_bound = info['score']
                    if not info['seen_seq1']:
                        upper_bound += last_score_seq1
                    if not info['seen_seq2']:
                        upper_bound += last_score_seq2
                    
                    if upper_bound > min_score_in_wk:
                        can_terminate = False
                        break
            
            if can_terminate:
                break
        
        # Read from seq1
        line = seq1_file.readline()
        if line:
            total_accesses += 1
            obj_id, score = line.strip().split()
            obj_id = int(obj_id)
            score = float(score)
            last_score_seq1 = score
            
            if obj_id in seen_objects:
                # Update object score
                seen_objects[obj_id]['score'] += score
                seen_objects[obj_id]['seen_seq1'] = True
                new_score = seen_objects[obj_id]['score']
                
                # Update Wk if necessary
                wk_objects = set(obj_id for _, obj_id in Wk)
                if obj_id in wk_objects:
                    # Remove and re-add with updated score
                    Wk = [(s, o) for s, o in Wk if o != obj_id]
                    heapq.heapify(Wk)
                    heapq.heappush(Wk, (new_score, obj_id))
                else:
                    # Check if it should now be in Wk
                    if len(Wk) < k:
                        heapq.heappush(Wk, (new_score, obj_id))
                    elif new_score > Wk[0][0]:
                        heapq.heappop(Wk)
                        heapq.heappush(Wk, (new_score, obj_id))
            else:
                # New object
                new_score = score + R[obj_id]
                seen_objects[obj_id] = {
                    'score': new_score,
                    'seen_seq1': True,
                    'seen_seq2': False
                }
                
                # Check if it should be in Wk
                if len(Wk) < k:
                    heapq.heappush(Wk, (new_score, obj_id))
                elif new_score > Wk[0][0]:
                    heapq.heappop(Wk)
                    heapq.heappush(Wk, (new_score, obj_id))
        
        # Read from seq2
        line = seq2_file.readline()
        if line:
            total_accesses += 1
            obj_id, score = line.strip().split()
            obj_id = int(obj_id)
            score = float(score)
            last_score_seq2 = score
            
            if obj_id in seen_objects:
                # Update object score
                seen_objects[obj_id]['score'] += score
                seen_objects[obj_id]['seen_seq2'] = True
                new_score = seen_objects[obj_id]['score']
                
                # Update Wk if necessary
                wk_objects = set(obj_id for _, obj_id in Wk)
                if obj_id in wk_objects:
                    # Remove and re-add with updated score
                    Wk = [(s, o) for s, o in Wk if o != obj_id]
                    heapq.heapify(Wk)
                    heapq.heappush(Wk, (new_score, obj_id))
                else:
                    # Check if it should now be in Wk
                    if len(Wk) < k:
                        heapq.heappush(Wk, (new_score, obj_id))
                    elif new_score > Wk[0][0]:
                        heapq.heappop(Wk)
                        heapq.heappush(Wk, (new_score, obj_id))
            else:
                # New object
                new_score = score + R[obj_id]
                seen_objects[obj_id] = {
                    'score': new_score,
                    'seen_seq1': False,
                    'seen_seq2': True
                }
                
                # Check if it should be in Wk
                if len(Wk) < k:
                    heapq.heappush(Wk, (new_score, obj_id))
                elif new_score > Wk[0][0]:
                    heapq.heappop(Wk)
                    heapq.heappush(Wk, (new_score, obj_id))
    
    # Close files
    seq1_file.close()
    seq2_file.close()
    
    # Output results
    print(f"Total sequential accesses: {total_accesses}")
    
    # Sort Wk in descending order of scores
    result = sorted([(score, obj_id) for score, obj_id in Wk], reverse=True)
    for score, obj_id in result:
        print(f"{obj_id} {score:.2f}")

if __name__ == "__main__":
    main()