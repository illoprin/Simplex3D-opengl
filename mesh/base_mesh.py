import os.path

from settings import *

class BaseMesh():
    name = None
    # storage all data about mesh (verts, UV, colors etc)
    data: dict[str, list] = None
    # all attribute names list ('in_position', 'in_color')
    attributes: tuple[str, ...] = None
    # all formats of attibutes '3u 3f 2i'
    format_data: str = None


def get_index_based_data(vertices, indices, format_size, type='f4', decrement=0):
    vertex_data = np.array(
        [vertices[(index-decrement) * format_size : (index-decrement) * format_size + format_size] for index in indices],
        dtype=type
    )
    return vertex_data


def load_from_obj(model_name: str):
    file_path = os.path.realpath(f'assets/models/{model_name}.obj')
    name: str = None
    vertices = []
    normals = []
    uv = []

    indices = []
    normals_indices = []
    uv_indices = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for line in file.readlines():
                line_data = line.split(" ")
                if line.startswith('o'):
                    name = ''.join(filter(str.isalnum, line_data[1]))
                elif line_data[0] == 'v':
                    vertices.append(float(line_data[1]))
                    vertices.append(float(line_data[2]))
                    vertices.append(float(line_data[3]))
                elif line_data[0] == 'vn':
                    normals.append(float(line_data[1]))
                    normals.append(float(line_data[2]))
                    normals.append(float(line_data[3]))
                elif line_data[0] == 'vt':
                    uv.append(float(line_data[1]))
                    uv.append(float(line_data[2]))
                elif line_data[0] == 'f':
                    for i in range(len(line_data)):
                        if i == 0: continue
                        raw_indices = line_data[i].split('/')
                        indices.append(int(raw_indices[0]))
                        uv_indices.append(int(raw_indices[1]))
                        normals_indices.append(int(raw_indices[2]))


            file.close()
    else:
        print(f"OBJ Loader: File by path {file_path} is not exists")

    prepared_vertices = get_index_based_data(
        vertices, indices, 3, decrement=1
    )
    prepared_normals = get_index_based_data(
        normals, normals_indices, 3,decrement=1
    )
    prepared_uv = get_index_based_data(
        uv, uv_indices, 2, decrement=1
    )

    print(f"OBJ Loader: Model named {name} loaded successfully")
    return {'name': name, 'vertices': prepared_vertices, 'normal': prepared_normals, 'uv': prepared_uv}
