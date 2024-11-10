import matplotlib.pyplot as plt

# Define the points for Class1 and Class2
class1 = [(1, 1), (1, 2), (2, 1)]
class2 = [(0, 0), (1, 0), (0, 1)]

# Separate the points into x and y coordinates
class1_x, class1_y = zip(*class1)
class2_x, class2_y = zip(*class2)

# Create the plot
plt.figure(figsize=(6, 6))
plt.scatter(class1_x, class1_y, color='blue', label='Class1', marker='o')
plt.scatter(class2_x, class2_y, color='red', label='Class2', marker='x')

# Add labels and title
plt.title('Class Points Plot')
plt.xlabel('X1-axis')
plt.ylabel('X2-axis')
plt.axhline(0, color='black',linewidth=0.5, ls='--')
plt.axvline(0, color='black',linewidth=0.5, ls='--')
plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
plt.xlim(-1, 3)
plt.ylim(-1, 3)
plt.legend()
plt.gca().set_aspect('equal', adjustable='box')

# Show the plot
plt.show()