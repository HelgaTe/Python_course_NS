from N2G import v3d_diagramm as create_v3d_diagram

sample_data_list = [
    {'data': {}, 'label': 'bla1', 'source': {'id': 'node-1', 'nodeResolution': 16}, 'src_label': '', 'target': {'id': 'node-2'}, 'trgt_label': ''},
    {'data': {}, 'label': 'bla2', 'source': 'node-1', 'src_label': '', 'target': 'node-3', 'trgt_label': ''},
    {'data': {}, 'label': 'bla3', 'source': {'id': 'node-3'}, 'src_label': '', 'target': 'node-5', 'trgt_label': ''},
    {'data': {}, 'label': 'bla4', 'source': {'id': 'node-3', 'data': {'val': 4}}, 'src_label': '', 'target': 'node-4', 'trgt_label': ''},
    {'data': {}, 'label': 'bla77', 'source': 'node-33', 'src_label': '', 'target': 'node-44', 'trgt_label': ''},
    {'data': {'cd': 123, 'ef': 456}, 'label': 'bla6', 'source': {'id': 'node-6', 'data': {'a': 'b', 'c': 'd'}}, 'src_label': '', 'target': 'node-1', 'trgt_label': ''}
]

v3d_drawing = create_v3d_diagram()
v3d_drawing.from_list(sample_data_list)
v3d_drawing.run(ip="0.0.0.0", port=9000)
