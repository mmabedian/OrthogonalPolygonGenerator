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


def find_reflex_vertices(polygon):
    """Find reflex vertices (interior angle > 180 degrees) in a polygon."""
    vertices = list(polygon.exterior.coords)[:-1]  # Remove duplicate last point
    print(vertices)
    reflex_vertices = []

    for i in range(len(vertices)):
        prev_pt = np.array(vertices[i - 1])
        curr_pt = np.array(vertices[i])
        next_pt = np.array(vertices[(i + 1) % len(vertices)])

        v1 = prev_pt - curr_pt
        v2 = next_pt - curr_pt
        v1 = np.array([v1[0], v1[1], 0])  # تبدیل به بردار سه‌بعدی
        v2 = np.array([v2[0], v2[1], 0])  # تبدیل به بردار سه‌بعدی
        cross_product = np.cross(v1, v2)

        cross_product = np.cross(v1, v2)[2]
        if cross_product > 0:  # Reflex if cross product is positive
            reflex_vertices.append(tuple(curr_pt))

    return reflex_vertices


def extend_edges(polygon, reflex_vertices):
    """Extend edges at reflex vertices to form bounding rectangles."""
    extended_lines = []

    for rv in reflex_vertices:
        x, y = rv

        # Extend horizontally left and right
        left_intersection = None
        right_intersection = None

        for edge in polygon.exterior.coords:
            line = LineString([edge, polygon.exterior.coords[
                (list(polygon.exterior.coords).index(edge) + 1) % len(polygon.exterior.coords)]])

            if line.intersects(LineString([(x, y - 1000), (x, y + 1000)])):
                intersection = line.intersection(LineString([(x, y - 1000), (x, y + 1000)]))
                if intersection.geom_type == 'Point':
                    if intersection.x < x:
                        left_intersection = intersection
                    elif intersection.x > x:
                        right_intersection = intersection

        if left_intersection and right_intersection:
            extended_lines.append((left_intersection, right_intersection))

    return extended_lines


def divide_into_rectangles(polygon, extended_lines):
    """Divide the polygon into rectangles using extended lines."""
    rectangles = []
    # Implementation of the splitting logic
    return rectangles

# print(border_vertices)
#
# polygon = Polygon(border_vertices)
#
# # Process polygon
# reflex_vertices = find_reflex_vertices(polygon)
# print("reflex vertices", reflex_vertices)
# extended_lines = extend_edges(polygon, reflex_vertices)
# rectangles = divide_into_rectangles(polygon, extended_lines)
#
# print("Rectangles:", rectangles)
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