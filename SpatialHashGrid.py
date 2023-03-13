class SpatialHashGrid:
    def __init__(self, width, cell_size=50):
        self.width = width
        self.cell_size = cell_size
        self.grid = {}

    def add_point(self, point):
        cell_x = int(point.x / self.cell_size)
        cell_y = int(point.y / self.cell_size)
        if cell_x not in self.grid:
            self.grid[cell_x] = {}
        if cell_y not in self.grid[cell_x]:
            self.grid[cell_x][cell_y] = set()
        self.grid[cell_x][cell_y].add(point)

    def _get_nearby_cells(self, point, radius):
        cells = set()
        cell_x = int(point.x / self.cell_size)
        cell_y = int(point.y / self.cell_size)
        radius_cells = int(radius / self.cell_size)
        for x in range(cell_x - radius_cells, cell_x + radius_cells + 1):
            for y in range(cell_y - radius_cells, cell_y + radius_cells + 1):
                if x in self.grid and y in self.grid[x]:
                    cells.add((x, y))
        return cells

    def get_nearby_points(self, point, radius):
        nearby_points = set()
        cells = self._get_nearby_cells(point, radius)
        for cell in cells:
            for p in self.grid[cell[0]][cell[1]]:
                dx = p.x - point.x
                dy = p.y - point.y
                distance = (dx ** 2 + dy ** 2) ** 0.5
                if distance <= radius:
                    nearby_points.add(p)
        return nearby_points
