import random
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Polygon, LineString

def sign(x):
    if x > 0:
        return 1
    if x == 0:
        return 0
    return -1

def is_border(x, y):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Top, Bottom, Left, Right
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if nx < 0 or ny < 0 or nx >= a or ny >= a or grid[nx][ny] == 0:
            return True
    return False

def sidesOfSquare(x , y):
    mySides = []
    if squares[x][y] == 1:
        if isValid(x, y + 1):
            if squares[x][y + 1] == 0:
                mySides.append(((x, y + 1), (x + 1, y + 1)))
        else:
            mySides.append(((x, y + 1), (x + 1, y + 1)))
        if isValid(x, y - 1):
            if squares[x][y - 1] == 0:
                mySides.append(((x, y), (x + 1, y)))
        else:
            mySides.append(((x, y), (x + 1, y)))
        if isValid(x + 1, y):
            if squares[x + 1][y] == 0:
                mySides.append(((x + 1, y), (x + 1, y + 1)))
        else:
            mySides.append(((x + 1, y), (x + 1, y + 1)))
        if isValid(x - 1, y):
            if squares[x - 1][y] == 0:
                mySides.append(((x, y), (x, y + 1)))
        else:
            mySides.append(((x, y), (x, y + 1)))
    return mySides


n = int(input("Enter number of iterations: "))


a = 60
squares = [[0 for _ in range(a)] for i in range(a)]
blues = []
sides = []

x = a // 2
y = a // 2
def isValid(x, y):
    return x >= 0 and x < a and y >= 0 and y < a

def borders():
    minX = a
    maxX = 0
    minY = a
    maxY = 0
    for x, y in blues:
        if x < minX:
            minX = x
        if x > maxX:
            maxX = x
        if y < minY:
            minY = y
        if y > maxY:
            maxY = y
    return minX, maxX, minY, maxY
blues.append((x, y))

for i in range(n):
    d = random.randint(6, 30)
    random.shuffle(blues)
    u = random.randint(0, len(blues) - 1)
    square = blues[u]
    sqX, sqY = square
    colorSquareNumber = 0
    while colorSquareNumber == 0:
        colorSquareNumber = random.randint(-d, d)
    direction = random.randint(0, 1)
    if direction == 0:
        for i in range(1, colorSquareNumber, sign(colorSquareNumber)):
            if isValid(sqX, sqY + i):
                squares[sqX][sqY + i] = 1
                blues.append((sqX, sqY + i))
            else:
                break
    else:
        for i in range(1, colorSquareNumber, sign(colorSquareNumber)):
            if isValid(sqX + i, sqY):
                squares[sqX + i][sqY] = 1
                blues.append((sqX + i, sqY))
            else:
                break



# Create a numpy array from the squares list
grid = np.array(squares)

# Plotting the grid
plt.figure(figsize=(8, 8))
plt.imshow(grid, cmap='Blues', origin='upper')  # Use 'Blues' for coloring
plt.colorbar(label='Square Color Intensity')   # Optional: color intensity bar
plt.xticks(ticks=range(a), labels=range(a))
plt.yticks(ticks=range(a), labels=range(a))
plt.grid(which='both', color='gray', linestyle='--', linewidth=0.5)
plt.title("Colored Squares Grid")
plt.show()

border_vertices = set()
def fill_enclosed_regions(grid):
    rows, cols = len(grid), len(grid[0])
    safe = set()


    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def flood_fill(x, y):
        stack = [(x, y)]
        while stack:
            cx, cy = stack.pop()
            if (cx, cy) in safe or grid[cx][cy] == 1:
                continue
            safe.add((cx, cy))
            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in safe and grid[nx][ny] == 0:
                    stack.append((nx, ny))

    # Step 1: Flood-fill from border cells
    for i in range(rows):
        if grid[i][0] == 0:
            flood_fill(i, 0)
        if grid[i][cols - 1] == 0:
            flood_fill(i, cols - 1)
    for j in range(cols):
        if grid[0][j] == 0:
            flood_fill(0, j)
        if grid[rows - 1][j] == 0:
            flood_fill(rows - 1, j)

    # Step 2: Convert enclosed 0s to 1s
    for i in range(rows):
        for j in range(cols):
            if (i, j) not in safe and grid[i][j] == 0:
                grid[i][j] = 1
                blues.append((i, j))

    # Step 3: Restore safe cells to 0
    for x, y in safe:
        grid[x][y] = 0
        if (x, y) in blues:
            blues.remove((x, y))

    return grid
squares = fill_enclosed_regions(squares)
for x in range(a):
    for y in range(a):
        sides += sidesOfSquare(x, y)
        if squares[x][y] == 1 and is_border(x, y):
            border_vertices.add((x, y))

blues = list(set(blues))
import matplotlib.patches as patches


plt.figure(figsize=(12, 12))
for side in sides:
    (x1, y1), (x2, y2) = side
    plt.plot([y1, y2], [x1, x2], linewidth=3, color = "blue")  # Black lines for sides
xMin, xMax, yMin, yMax = borders()
a = min(xMin, yMin)
b = max(xMax, yMax)
print(np.array(squares)[xMin:xMax, yMin:yMax])
plt.yticks(ticks=range(xMin, xMax + 2), labels=range(xMin, xMax + 2))
plt.xticks(ticks=range(yMin, yMax + 2), labels=range(yMin, yMax + 2))
plt.grid(which='both', color='lightblue', linestyle='--', linewidth=1.5)

for x, y in blues:
    square = patches.Rectangle((y, x), 1, 1, linewidth=0, edgecolor='none', facecolor='lightblue', alpha=0.5)
    plt.gca().add_patch(square)
plt.gca().set_aspect('equal', adjustable='box')
plt.title("Grid with Border Sides and Vertices")
plt.show()

def merge_edges(edges):
    from collections import defaultdict

    # Sort edges for consistency
    edges = sorted(edges)

    # Group edges by orientation (horizontal or vertical)
    horizontal = defaultdict(list)
    vertical = defaultdict(list)

    for (x1, y1), (x2, y2) in edges:
        if x1 == x2:  # Vertical edge
            vertical[x1].append((min(y1, y2), max(y1, y2)))
        else:  # Horizontal edge
            horizontal[y1].append((min(x1, x2), max(x1, x2)))

    def merge_ranges(ranges):
        ranges.sort()
        merged = []
        start, end = ranges[0]

        for s, e in ranges[1:]:
            if s <= end:  # Overlapping or adjacent
                end = max(end, e)
            else:
                merged.append((start, end))
                start, end = s, e
        merged.append((start, end))

        return merged

    # Merge adjacent ranges
    for key in horizontal:
        horizontal[key] = merge_ranges(horizontal[key])
    for key in vertical:
        vertical[key] = merge_ranges(vertical[key])

    # Convert back to edge list
    merged_edges = []
    for y, ranges in horizontal.items():
        for x1, x2 in ranges:
            merged_edges.append(((x1, y), (x2, y)))
    for x, ranges in vertical.items():
        for y1, y2 in ranges:
            merged_edges.append(((x, y1), (x, y2)))

    return merged_edges

#print(sides)
print("merge", merge_edges(sides))
real_edges = merge_edges(sides)


from collections import defaultdict


def sort_polygon_edges(sides):
    # ساخت گراف اتصالات رأس‌ها
    graph = defaultdict(list)
    for (x1, y1), (x2, y2) in sides:
        graph[(x1, y1)].append((x2, y2))
        graph[(x2, y2)].append((x1, y1))

    # یافتن یک رأس شروع (کوچکترین نقطه بر اساس y سپس x)
    start = min(graph.keys())

    # بازسازی ترتیب اضلاع با DFS
    sorted_sides = []
    visited = set()
    current = start
    prev = None

    while len(visited) < len(sides):
        visited.add(current)
        neighbors = sorted(graph[current], key=lambda p: (p[1], p[0]))  # مرتب‌سازی بر اساس y و سپس x

        # انتخاب همسایه بعدی که قبلاً بازدید نشده باشد
        next_vertex = None
        for neighbor in neighbors:
            if neighbor != prev:  # جلوگیری از حرکت به عقب
                next_vertex = neighbor
                break

        if next_vertex is None:
            break  # پایان در صورت بسته بودن چندضلعی

        sorted_sides.append((current, next_vertex))
        prev, current = current, next_vertex

    return sorted_sides

print(sort_polygon_edges(real_edges))
sorted_sides = sort_polygon_edges(real_edges)


def find_reflex_vertices(sides):
    def turn_direction(o, a, b):
        """ محاسبه جهت چرخش از بردار OA به OB """
        (ox, oy), (ax, ay), (bx, by) = o, a, b
        dx1, dy1 = ax - ox, ay - oy
        dx2, dy2 = bx - ax, by - ay
        return dx1 * dy2 - dy1 * dx2  # تعیین جهت چرخش

    vertices = [sides[0][0]] + [edge[1] for edge in sides]  # استخراج ترتیب رأس‌ها
    reflex_vertices = []

    for i in range(len(vertices)):
        prev, current, next_vertex = vertices[i - 1], vertices[i], vertices[(i + 1) % len(vertices)]
        if turn_direction(prev, current, next_vertex) < 0:  # اگر چرخش به راست باشد (زاویه داخلی ۲۷۰ درجه)
            reflex_vertices.append(current)

    return reflex_vertices

reflex_vertices = find_reflex_vertices(sorted_sides)
print("Reflex Vertices:", reflex_vertices)


def plot_polygon_with_reflex(sides, reflex_vertices):
    plt.figure(figsize=(12, 12))
    for side in sides:
        (x1, y1), (x2, y2) = side
        plt.plot([y1, y2], [x1, x2], linewidth=3, color="blue")  # خطوط چندضلعی

    # رسم رأس‌های رفلکس
    for x, y in reflex_vertices:
        plt.scatter(y, x, color='red', s=100, zorder=3,
                    label='Reflex Vertex' if 'Reflex Vertex' not in plt.gca().get_legend_handles_labels()[1] else "")

    plt.legend()
    plt.gca().set_aspect('equal', adjustable='box')
    plt.title("Polygon with Reflex Vertices")
    plt.grid(which='both', color='lightblue', linestyle='--', linewidth=1.5)
    plt.show()


# رسم چندضلعی همراه با رأس‌های رفلکس
plot_polygon_with_reflex(sorted_sides, reflex_vertices)


def separate_vertical_horizontal(sides):
    vertical_sides = []
    horizontal_sides = []
    for (x1, y1), (x2, y2) in sides:
        if x1 == x2:
            vertical_sides.append(((x1, y1), (x2, y2)))
        elif y1 == y2:
            horizontal_sides.append(((x1, y1), (x2, y2)))

    vertical_sides.sort(key=lambda side: (side[0][0], side[0][1]))
    horizontal_sides.sort(key=lambda side: (side[0][1], side[0][0]))

    return vertical_sides, horizontal_sides


def find_direction_of_vertex(vertex, vertical_sides, horizontal_sides):
    x, y = vertex
    dirx = 0
    diry = 0
    for (x1, y1), (x2, y2) in vertical_sides:
        if x1 == x:
            if y1 == y or y2 == y:
                diry = y1 - y2
    for (x1, y1), (x2, y2) in horizontal_sides:
        if y1 == y:
            if x1 == x or x2 == x:
                dirx = x2 - x1
    dirx, diry = sign(dirx), sign(diry)
    if dirx * diry > 0:
        return dirx, diry
    else:
        return diry, dirx


def extend_reflex_lines(reflex_vertices, vertical_sides, horizontal_sides):
    extension_lines = []

    for rx, ry in reflex_vertices:
        # Extend horizontally (leftward)
        dirx, diry = find_direction_of_vertex((rx, ry), vertical_sides, horizontal_sides)
        print("Reflex vertex: ", (rx, ry), dirx, diry)
        if diry > 0:
            for (x1, y1), (x2, y2) in horizontal_sides:
                a, b = min(x1, x2), max(x1, x2)
                print("Coor", ((x1, y1), (x2, y2)), "y1 > ry", y1 > ry, "x1 <= rx <= x2", x1 <= rx <= x2)
                if y1 > ry and a <= rx <= b:
                    extension_lines.append(((rx, ry), (rx, y1)))
                    break
        else:
            for (x1, y1), (x2, y2) in horizontal_sides[::-1]:
                a, b = min(x1, x2), max(x1, x2)
                print("Coor", ((x1, y1), (x2, y2)), "y1 < ry", y1 < ry, "x1 <= rx <= x2", x1 <= rx <= x2)
                if y1 < ry and a <= rx <= b:
                    extension_lines.append(((rx, ry), (rx, y1)))
                    break

        if dirx > 0:
            for (x1, y1), (x2, y2) in vertical_sides:
                a, b = min(y1, y2), max(y1, y2)
                if x1 > rx and a <= ry <= b:
                    extension_lines.append(((rx, ry), (x1, ry)))
                    break
        else:
            for (x1, y1), (x2, y2) in vertical_sides[::-1]:
                a, b = min(y1, y2), max(y1, y2)
                if x1 < rx and a <= ry <= b:
                    extension_lines.append(((rx, ry), (x1, ry)))
                    break
    return extension_lines


def plot_polygon_with_reflex_and_extensions(sides, reflex_vertices, extension_lines):
    plt.figure(figsize=(12, 12))
    for side in sides:
        (x1, y1), (x2, y2) = side
        plt.plot([x1, x2], [y1, y2], linewidth=3, color="blue")

    for x, y in reflex_vertices:
        plt.scatter(x, y, color='red', s=100, zorder=3,
                    label='Reflex Vertex' if 'Reflex Vertex' not in plt.gca().get_legend_handles_labels()[1] else "")

    for (x1, y1), (x2, y2) in extension_lines:
        plt.plot([x1, x2], [y1, y2],  linestyle='dashed', color='green', linewidth=2,
                 label='Extension' if 'Extension' not in plt.gca().get_legend_handles_labels()[1] else "")

    plt.legend()
    plt.gca().set_aspect('equal', adjustable='box')
    plt.title("Polygon with Reflex Vertices and Extensions")
    plt.grid(which='both', color='lightblue', linestyle='--', linewidth=1.5)
    plt.show()

vertical_sides, horizontal_sides = separate_vertical_horizontal(sorted_sides)
extension_lines = extend_reflex_lines(reflex_vertices, vertical_sides, horizontal_sides)
print("Extension Lines:", extension_lines)
print("Vertical Sides:", vertical_sides)
print("Horizontal Sides:", horizontal_sides)
plot_polygon_with_reflex_and_extensions(sorted_sides, reflex_vertices, extension_lines)

