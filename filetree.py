import os

'''
node:
{
    dir: string,
    name: string,
    children: list of node,
    depth: int,
}
'''
    

id2node = {}

def init_file_tree(root_path):
    id2node.clear()
    id2node[0] = {
        'dir': root_path,
        'name': root_path,
        'children': None,
        'depth': 0,
        'hasChildren': len([dir for dir in os.listdir(root_path) if os.path.isdir(os.path.join(root_path, dir))])>0
    }
    # for dir in os.listdir(root_path):
    #     if os.path.isdir(os.path.join(root_path, dir)):
    #         child_dir = os.path.join(root_path, dir)
    #         new_node = {
    #             'dir': child_dir,
    #             'name': dir,
    #             'children': None,
    #             'depth': 1,
    #             'hasChildren': len([dir for dir in os.listdir(child_dir) if os.path.isdir(os.path.join(child_dir, dir))])>0
    #         }
    #         id2node[len(id2node)] = new_node
    #         id2node[0]['children'].append(len(id2node) - 1)

def expand_file_node(node_id):
    node = id2node[node_id]
    if node['children'] is not None:
        return
    node['children'] = []
    for dir in os.listdir(node['dir']):
        if os.path.isdir(os.path.join(node['dir'], dir)):
            child_dir = os.path.join(node['dir'], dir)
            new_node = {
                'dir': os.path.join(node['dir'], dir),
                'name': dir,
                'children': None,
                'depth': node['depth'] + 1,
                'hasChildren': len([dir for dir in os.listdir(child_dir) if os.path.isdir(os.path.join(child_dir, dir))])>0
            }
            id2node[len(id2node)] = new_node
            node['children'].append(len(id2node) - 1)

def collapse_file_node(node_id):
    node = id2node[node_id]
    if node['children'] is None:
        id2node.pop(node_id)
        return
    for child_id in node['children']:
        collapse_file_node(child_id)
        if child_id in id2node:
            id2node.pop(child_id)
    node['children'] = None

# class FileTreeNode:
#     def __init__(self, dir, pardir=None) -> None:
#         self.dir = str(dir)
#         self.parent = pardir.id if pardir is not None else None
#         self.name = os.path.basename(dir)
#         self.children = None
#         self.id = len(id2node)
#         id2node[self.id] = self
    
#     def parse_children(self):
#         if self.children is not None:
#             return
#         self.children = []
#         for dir in os.listdir(self.dir):
#             if os.path.isdir(os.path.join(self.dir, dir)):
#                 new_node = FileTreeNode(os.path.join(self.dir, dir), self)
#                 self.children.append(new_node.id)