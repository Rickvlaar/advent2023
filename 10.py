from matplotlib.patches import Polygon
from util import console, parse_file_as_list, time_function
from dataclasses import field, dataclass
import matplotlib.pyplot as plt
import heapq
import math
import sys
import numpy as np

test_file = parse_file_as_list('input/10_test.txt')
day_file = parse_file_as_list('input/10.txt')


@dataclass(order=True)
class Vertex:
    coordinate: tuple = field(compare=False)
    neighbours: list[tuple] = field(compare=False, default_factory=list)
    distance: int = field(default=math.inf)
    previous_vertex: 'Vertex' = field(compare=False, default=None)


@dataclass
class Graph:
    start_vertex_coordinate: tuple
    target_vertex_coordinate: tuple
    vertices_queue: list[Vertex] = field(default_factory=list)
    vertices_dict: dict[tuple, Vertex] = field(default_factory=dict)
    vertex_neighbours_dict: dict[tuple, list[tuple]] = field(default_factory=dict)
    target_vertex_with_path: Vertex = None
    map_dimensions: tuple = None

    def prepare_queue_from_list(self, vertex_coords: list):
        neighbour_coords = self.vertex_neighbours_dict.get(self.start_vertex_coordinate)

        start_vertex = Vertex(coordinate=self.start_vertex_coordinate,
                              neighbours=neighbour_coords,
                              distance=0)
        self.vertices_dict[start_vertex.coordinate] = start_vertex
        heapq.heappush(self.vertices_queue, start_vertex)

        for vertex_coord in vertex_coords:
            if vertex_coord == self.start_vertex_coordinate:
                continue

            vertex = Vertex(coordinate=vertex_coord,
                            neighbours=self.vertex_neighbours_dict.get(vertex_coord))

            self.vertices_dict[vertex_coord] = vertex

    def dijk_it(self):
        while self.vertices_queue:
            closest_vertex = heapq.heappop(self.vertices_queue)  # will be start_vertex_initially

            # do not process coordinates without neighbours
            neigbour_coords = self.vertex_neighbours_dict.get(closest_vertex.coordinate)
            if not neigbour_coords:
                continue

            # go over each neighbour and check whether the route from source vertex would be shorter
            dist_from_closest_vertex = closest_vertex.distance + 1
            for vertex_coord in neigbour_coords:
                vertex = self.vertices_dict.get(vertex_coord)

                # stop processing when target is reached
                if self.is_target(vertex):
                    vertex.previous_vertex = closest_vertex
                    vertex.distance = dist_from_closest_vertex
                    self.target_vertex_with_path = vertex
                    return vertex.distance

                elif dist_from_closest_vertex < vertex.distance:
                    vertex.distance = dist_from_closest_vertex
                    vertex.previous_vertex = closest_vertex
                    heapq.heappush(self.vertices_queue, vertex)

    def is_target(self, vertex: Vertex):
        if vertex.coordinate == self.target_vertex_coordinate:
            return True
        else:
            return False

    def plot_path_on_map(self):
        path_map = np.full(shape=self.map_dimensions, fill_value=0, dtype=int)
        self.fill_map_from_path_vertex(path_map, self.target_vertex_with_path)
        return path_map

    def fill_map_from_path_vertex(self, path_map: np.ndarray, vertex: Vertex):
        path_map[vertex.coordinate] = vertex.distance
        if vertex.previous_vertex:
            self.fill_map_from_path_vertex(path_map, vertex.previous_vertex)

    def get_path_coordinates_to_target_vertex(self, coordinates: list[tuple], target_vertex: Vertex):
        coordinates.append(target_vertex.coordinate)
        if target_vertex.previous_vertex:
            self.get_path_coordinates_to_target_vertex(coordinates, target_vertex.previous_vertex)

    def get_all_paths_length(self):
        length = 0
        for vertex in self.vertices_dict.values():
            length += 1 if isinstance(vertex.distance, int) else 0
        return length

    def plot_all_paths_on_map(self):
        paths_map = np.full(shape=self.map_dimensions, fill_value=0, dtype=int)
        for coord, vertex in self.vertices_dict.items():
            paths_map[coord] = vertex.distance if isinstance(vertex.distance, int) else -1
        return paths_map

    def plot_all_paths_on_map_as_image(self):
        paths_map = np.full(shape=self.map_dimensions, fill_value=0, dtype=str)
        for coord, vertex in self.vertices_dict.items():
            paths_map[coord] = '1' if isinstance(vertex.distance, int) else '.'
        return paths_map


@time_function()
def run_a(file: list[str]):
    # read the map
    pipe_map = np.array([[char for char in line] for line in file])
    pipe_neighbours = get_possible_neighbours(pipe_map)

    the_start = np.where(pipe_map == 'S')  # Y, X
    start_coord = (the_start[0][0], the_start[1][0])

    coords_list = [(y, x) for y in range(pipe_map.shape[0]) for x in range(pipe_map.shape[1])]

    pipe_graph = Graph(start_coord, (999999, 999999), vertex_neighbours_dict=pipe_neighbours)
    pipe_graph.prepare_queue_from_list(coords_list)
    pipe_graph.dijk_it()
    pipe_graph.map_dimensions = pipe_map.shape

    return max([vertex.distance for vertex in pipe_graph.vertices_dict.values() if isinstance(vertex.distance, int)])


@time_function()
def run_b(file: list[str], draw_polygon=False):
    # read the map
    sys.setrecursionlimit(15000)

    pipe_map = np.array([[char for char in line] for line in file])
    pipe_neighbours = get_possible_neighbours(pipe_map)

    the_start = np.where(pipe_map == 'S')  # Y, X
    start_coord = (the_start[0][0], the_start[1][0])

    coords_list = [(y, x) for y in range(pipe_map.shape[0]) for x in range(pipe_map.shape[1])]

    pipe_graph = Graph(start_coord, (999999, 999999), vertex_neighbours_dict=pipe_neighbours)
    pipe_graph.prepare_queue_from_list(coords_list)
    pipe_graph.dijk_it()
    pipe_graph.map_dimensions = pipe_map.shape

    # find all corners on the path
    paths_map = pipe_graph.plot_all_paths_on_map()

    loop_end_value = max([vertex.distance for vertex in pipe_graph.vertices_dict.values() if isinstance(vertex.distance, int)])
    target_coords_wheres = np.where(paths_map == (loop_end_value - 1))
    target_coord_1 = (target_coords_wheres[0][0], target_coords_wheres[1][0])
    target_coord_2 = (target_coords_wheres[0][1], target_coords_wheres[1][1])

    path_coords = []
    target_vertex = pipe_graph.vertices_dict[target_coord_1]
    pipe_graph.get_path_coordinates_to_target_vertex(path_coords, target_vertex)
    path_coords.reverse()

    loop_end = np.where(paths_map == loop_end_value)  # Y, X
    loop_end_coord = (loop_end[0][0], loop_end[1][0])
    path_coords.append(loop_end_coord)

    second_path_coords = []
    target_vertex = pipe_graph.vertices_dict[target_coord_2]
    pipe_graph.get_path_coordinates_to_target_vertex(second_path_coords, target_vertex)
    path_coords.extend(second_path_coords)

    coordinate_symbols = {'F', '7', 'J', 'L', 'S'}
    coords_to_plot = []
    for coord in path_coords:
        vertex = pipe_graph.vertices_dict[coord]
        # only plot the path
        if not isinstance(vertex.distance, int):
            continue

        if pipe_map[coord] in coordinate_symbols or coord == loop_end_coord:
            coords_to_plot.append(vertex)

    polygon_coords = []
    for vertex in coords_to_plot:
        polygon_coords.append((vertex.coordinate[1], vertex.coordinate[0]))

    if draw_polygon:
        draw_polygon_from_coords(polygon_coords, pipe_map.shape)

    area = get_polygon_surface_area_by_coords(polygon_coords)
    return int(area - loop_end_value + 1)


def segments(p):
    return


def get_polygon_surface_area_by_coords(polygon_coords: list[tuple]):
    # Shoelace formula https://en.wikipedia.org/wiki/Shoelace_formula
    segments = zip(polygon_coords, polygon_coords[1:] + [polygon_coords[0]])
    area = 0.5 * abs(sum(x0 * y1 - x1 * y0 for ((x0, y0), (x1, y1)) in segments))
    return area


def draw_polygon_from_coords(polygon_coords: list[tuple], shape: tuple):
    # draw the thing for fun
    polygon = Polygon(polygon_coords, facecolor='k', fill=False)
    fig, ax = plt.subplots(1, 1)
    ax.add_patch(polygon)
    plt.ylim(shape[0], 0)
    plt.xlim(0, shape[1])
    plt.show()


def get_possible_neighbours(pipe_map: np.ndarray) -> dict:
    possible_bottoms = {'|', 'J', 'L', 'S'}
    possible_tops = {'|', 'F', '7', 'S'}
    possible_rights = {'-', '7', 'J', 'S'}
    possible_lefts = {'-', 'L', 'F', 'S'}

    max_y = pipe_map.shape[0] - 1
    max_x = pipe_map.shape[1] - 1
    the_hood = dict()
    for y, line in enumerate(pipe_map):
        for x, num in enumerate(line):
            neighbs = []
            current_pipe = pipe_map[y, x]
            # left
            if x > 0:
                left_coord = (y, x - 1)
                left = pipe_map[left_coord]
                if left in possible_lefts and current_pipe in possible_rights:
                    neighbs.append(left_coord)
            # right
            if x < max_x:
                right_coord = (y, x + 1)
                right = pipe_map[right_coord]
                if right in possible_rights and current_pipe in possible_lefts:
                    neighbs.append(right_coord)
            # top
            if y > 0:
                top_coord = (y - 1, x)
                top = pipe_map[top_coord]
                if top in possible_tops and current_pipe in possible_bottoms:
                    neighbs.append(top_coord)
            # bottom
            if y < max_y:
                bottom_coord = (y + 1, x)
                bottom = pipe_map[bottom_coord]
                if bottom in possible_bottoms and current_pipe in possible_tops:
                    neighbs.append(bottom_coord)
            the_hood[(y, x)] = neighbs

    return the_hood


if __name__ == '__main__':
    answer_a = run_a(day_file)
    answer_b = run_b(day_file)

    console.print(f'solution A: {answer_a}')
    console.print(f'solution B: {answer_b}')
