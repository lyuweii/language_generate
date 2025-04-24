import numpy as np
import igraph as ig
import matplotlib.pyplot as plt


class BaseMemory:

    def __init__(self):
        self.data = ig.Graph()

    def match_node(self, data, **kwargs):
        """匹配节点，如果没有则直接添加，name 即 data.__repr()。"""
        if (not self.data.vs or
                not self.data.vs.select(name_eq=data)) and not (data is None):
            node = self.data.add_vertex(name=data.__repr__(),
                                        data=data,
                                        **kwargs)
        else:
            node = self.data.vs.find(name_eq=data.__repr__())
        return node

    def match_node_by_index(self, index):
        """通过索引匹配节点，如果没有则报异常。"""
        node = self.data.vs.find(index_eq=index)
        return node

    def match_edge(self,
                   node1: ig.Vertex,
                   node2: ig.Vertex,
                   weight: float = None):
        """匹配边，如果没有则直接添加，权重为 0-1 间的均匀分布随机数。"""
        if not self.data.are_adjacent(node1, node2):
            edge = self.data.add_edge(
                node1,
                node2,
                weight=np.random.rand() if weight is None else weight)
        else:
            edge = self.data.es[self.data.get_eid(node1, node2)]
        return edge

    def select_nodes(self, **kwargs):
        """选择节点，若不符合条件，返回 None。"""
        try:
            nodes = self.data.vs.select(**kwargs)
        except:
            nodes = None
        return nodes

    def incident_nodes(self, node: ig.Vertex, **kwargs):
        """获取节点的所有邻接节点，非节点索引，可能为 None。"""
        if not kwargs:
            return node.neighbors(mode="all")
        nodes = node.neighbors(mode='all')
        if nodes is not None:
            return [n for n in nodes if self.data.vs.select(n.index, **kwargs)]
        return None

    def incident_edges(self, node: ig.Vertex, **kwargs):
        """获取节点的所有邻接边，非边索引，可能为 None。"""
        if not kwargs:
            return node.incident(mode="all")
        # 过滤不符合条件的节点所对应的边
        edges = [
            e for e in node.incident(mode="all")
            if (e.source == node.index
                and self.data.vs.select(e.target, **kwargs)) or (
                    e.target == node.index
                    and self.data.vs.select(e.source, **kwargs))
        ]
        return edges

    def sort_weight_edges(self, node: ig.Vertex, n: int = 1, **kwargs):
        """获取权重排序的前 num 条边，非边索引，如果无边，返回 None。"""
        edges = self.incident_edges(node)
        if not edges:
            return None
        # 过滤不符合条件的节点所对应的边
        if kwargs:
            edges = [
                e for e in edges
                if (e.source == node.index
                    and self.data.vs.select(e.target, **kwargs)) or (
                        e.target == node.index
                        and self.data.vs.select(e.source, **kwargs))
            ]
        sorted_edges = sorted(edges, key=lambda e: e['weight'], reverse=True)
        result = sorted_edges[:n]
        return result

    def max_weight_edge(self, node: ig.Vertex, **kwargs):
        """获取节点邻接边的最大权重对应的边，无边返回 None。"""
        max_edges = self.sort_weight_edges(node, 1, **kwargs)
        if not max_edges:
            return None
        return max_edges[0]

    def max_weight_node(self, node: ig.Vertex, **kwargs):
        """获取节点邻接边的最大权重对应的节点，无边返回 None。"""
        max_edges = self.sort_weight_edges(node, 1, **kwargs)
        if not max_edges:
            return None
        edge = max_edges[0]
        if node.index == edge.target:
            return self.data.vs[edge.source]
        else:
            return self.data.vs[edge.target]

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
            connect_edges = self.incident_edges(node)
            if not connect_edges:
                continue
            # 按权重降序排序
            sorted_edges = sorted(connect_edges,
                                  key=lambda e: e['weight'],
                                  reverse=True)
            top_n_edges = [e.index for e in sorted_edges[:num]]
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
