
CUBE = {
    'vertices': [
        # x, y, z
        -.5, -.5, .5,
        .5, -.5, .5,
        -.5, .5, .5,
        .5, .5, .5,
        -.5, -.5, -.5,
        .5, -.5, -.5,
        -.5, .5, -.5,
        .5, .5, -.5
    ],
    'face_uv': [
        0, 0,
        1, 0,
        1, 1,
        0, 1
    ],
    'tex_coord_indices': [
        # top
        2, 3, 0,
        2, 0, 1,
        # bottom
        0, 1, 2,
        0, 2, 3,
        # left
        2, 3, 0,
        2, 0, 1,
        # right
        2, 3, 0,
        2, 0, 1,
        # front
        2, 3, 0,
        0, 1, 2,
        # back
        2, 3, 0,
        2, 0, 1
    ],
    'indices': [
        # top
        7, 6, 2,
        7, 2, 3,

        # bottom
        1, 0, 4,
        1, 4, 5,

        # left
        2, 6, 4,
        2, 4, 0,

        # right
        7, 3, 1,
        7, 1, 5,

        # front
        3, 2, 0,
        0, 1, 3,

        # back
        6, 7, 5,
        6, 5, 4
    ]
}

PYRAMID = {
    'vertices':[
        0, 0, 1,
        0, 0, 0,
        1, 0, .5,
        .5, 1, .5
    ],
    'indices': [
        # front
        3, 2, 1,

        # left
        3, 1, 0,

        # right
        2, 3, 0,

        # bottom
        0, 1, 2
    ],
    'face_uv': [
        0, 0,
        1, 0,
        .5, 1,
    ],
    'tex_coord_indices': [
        # left
        2, 1, 0,
        # right
        2, 1, 0,
        # back
        2, 1, 0,
        # bottom
        0, 2, 1
    ]
}

AXIS = {
    'vertices': [
        0, 0, 0,
        1, 0, 0,
        0, 1, 0,
        0, 0, 1
    ],

    'indices': [
        # X
        0, 1,
        # Y
        0, 2,
        # Z
        0, 3,
    ],

    'color_indices': [
        # X
        1, 1,
        # Y
        2, 2,
        # Z
        3, 3,
    ],

    'color': [
        0, 0, 0,
        # X
        1, 0, 0,
        # Y
        0, 1, 0,
        # Z
        0, 0, 1
    ]
}