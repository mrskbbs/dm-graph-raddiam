import datetime

def timer(func):
    def wrapper(*args, **kwargs):
        t1 = datetime.datetime.now()
        result = func(*args, **kwargs)
        print(f"Выполнено за -> {(datetime.datetime.now() - t1).total_seconds() * 1000}мс")
        return result
    return wrapper

class Graph:
    graph: dict[int, set[int]] 

    def __init__(self, path_adj_mat: str):
        self.graph: dict[int, set[int]] = dict()
        
        with open(path_adj_mat) as f:
            i = 1
            for row_str in f:
                vertn = 1
                row = []
                for val in row_str.split():
                    if val == "1":
                        row.append(vertn)
                    vertn += 1
                self.graph[i] = set(row)
                i += 1

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass
    
    def shortestDistance(self, st: int, end: int):
        visited: set[int] = set()
        queue = [[st]]
         
        if st == end:
            return 0
         
        while queue:
            path = queue.pop(0)
            node = path[-1]
             
            if node not in visited:
                neighbours = self.graph[node]

                for neighbour in neighbours:
                    if neighbour == end:
                        return len(path)
                    
                    new_path = list(path)
                    new_path.append(neighbour)
                    queue.append(new_path)

            visited.add(node)
    
        return 0
    
    @timer
    def getRadiusAndDiameter(self):
        """
        Output
        1) Radius
        2) Diameter
        """
        
        matrix: list = [[0 for j in range(len(self.graph))] for i in range(len(self.graph))]
        st = 1
        for y in range(0, len(self.graph) - 1):
            for x in range(st, len(self.graph)):
                matrix[x][y] = matrix[y][x] = self.shortestDistance(x+1, y+1)
            st += 1

        seq = [max(row) for row in matrix]

        return min(seq), max(seq)

if __name__ == "__main__":
    pathname = str(input("Введите путь к матрице смежности в формате \n0 1 0\n1 0 1\n0 0 0:\n"))

    with Graph(pathname) as g:
        radius, diameter = g.getRadiusAndDiameter()
        print(f"Радиус графа: {radius}")
        print(f"Диаметр графа: {diameter}")

