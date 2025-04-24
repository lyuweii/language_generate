import numpy as np
import igraph as ig
import matplotlib.pyplot as plt


class Memory:

    def __init__(self):
        self.data = ig.Graph()

    def match_node(self, name: str, data=None, **kwargs):
        """匹配节点"""
        if (not self.data.vs or
                not self.data.vs.select(name_eq=name)) and not (data is None):
            node = self.data.add_vertex(name=name, data=data, **kwargs)
        else:
            node = self.data.vs.select(name_eq=name)[0]
        return node

    def match_edge(self, node1: ig.Vertex, node2: ig.Vertex):
        """匹配边，如果不存在则添加对应边，返回边和之前是否存在。"""
        flag = self.data.are_connected(node1, node2)
        if not flag:
            edge = self.data.add_edge(node1, node2, weight=np.random.rand())
        else:
            edge = self.data.es[self.data.get_eid(node1, node2)]
        return edge, flag

    def are_adjacent(self, node1: ig.Vertex, node2: ig.Vertex):
        """判断两个节点是否相邻"""
        return self.data.are_adjacent(node1, node2)

    def select_nodes(self, **kwargs):
        """选择节点"""
        try:
            nodes = self.data.vs.select(**kwargs)
        except:
            nodes = None
        return nodes

    def incident_nodes(self, node: ig.Vertex):
        """获取节点的所有邻接节点"""
        return node.neighbors()

    def incident_edges(self, node: ig.Vertex,**kwargs):
        """获取节点的所有邻接边"""
        return self.data.incident(node, **kwargs)

    def sort_weight_edges(self, node: ig.Vertex, num: int = 1, **kwargs):
        """获取权重排序的前 num 条边"""
        edges = self.data.incident(node, **kwargs)
        if not edges:
            return None
        sorted_edges = sorted(edges,
                              key=lambda e: self.data.es[e]['weight'],
                              reverse=True)
        result = [self.data.es[e] for e in sorted_edges[:num]]
        return result

    def max_weight_edge(self, node: ig.Vertex, **kwargs):
        """获取节点邻接边的最大权重对应的边"""
        max_edges = self.sort_weight_edges(node, 1, **kwargs)
        if not max_edges:
            return None
        return max_edges[0]

    def max_weight_node(self, node: ig.Vertex):
        """获取节点邻接边的最大权重对应的节点"""
        max_edges = self.sort_weight_edges(node, 1)
        if not max_edges:
            return None
        edge = max_edges[0]
        if node.index == edge.target:
            source = self.data.vs[edge.source]
            return source
        else:
            target = self.data.vs[edge.target]
            return target

    def plot(self, num: int = 5, names=None):
        """绘制图形"""
        # 确保边有原图索引属性
        if not hasattr(self.data.es, 'original_eid'):
            self.data.es['original_eid'] = list(range(len(self.data.es)))
        if not names:
            names = self.data.vs['name']

        selected_edges = []
        highlight_edges = []
        for name in names:
            try:
                node = self.data.vs.find(name=name)
            except ValueError:
                continue
            connect_edges = self.data.incident(node)
            if not connect_edges:
                continue

            # 按权重降序排序
            sorted_edges = sorted(connect_edges,
                                  key=lambda e: self.data.es[e]['weight'],
                                  reverse=True)
            top_n_edges = sorted_edges[:num]
            highlight_edges.append(top_n_edges[0])  # 记录原图边索引
            selected_edges.extend(top_n_edges)

        if selected_edges:
            # 生成子图（保留原始边属性）
            sub = self.data.subgraph_edges(selected_edges,
                                           delete_vertices=False)

            # 可视化设置
            layout = sub.layout("auto")
            fig, ax = plt.subplots(figsize=(10, 10))

            # 边颜色匹配：通过 original_eid 映射原图索引
            edge_colors = [
                "red" if e['original_eid'] in highlight_edges else "gray"
                for e in sub.es
            ]

            # 顶点颜色：通过名称直接匹配
            vertex_colors = [
                "orange" if v['name'] in names else "lightblue" for v in sub.vs
            ]

            ig.plot(sub,
                    target=ax,
                    layout=layout,
                    vertex_label=sub.vs["name"],
                    edge_label=[f"{int(w)}" for w in sub.es['weight']],
                    vertex_color=vertex_colors,
                    edge_color=edge_colors,
                    vertex_size=50)
            plt.show()
