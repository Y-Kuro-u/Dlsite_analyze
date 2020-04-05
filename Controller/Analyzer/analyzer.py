import itertools
import collections
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import rcParams
from pathlib import Path

class CoOccurrenceNetwork:
    def __init__(self):
        rcParams['font.family'] = 'sans-serif'
        rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'Noto Sans CJK JP']

    def make_count_tags(self,tags):
        count_tags = []
        for tag_lists in tags:
            count_tag = []
            for tag_list in tag_lists:
                for tag in tag_list:
                    count_tag.append(tag)
            
            count_tags.append(count_tag)

        counter_dicts = []
        for count_tag in count_tags:
            counter_dict = {}
            counters = collections.Counter(count_tag)
            for item,value in counters.items():
                counter_dict[item] = value
            counter_dicts.append(counter_dict)
        return counter_dicts

    def make_combination_tags(self,tags):
        combination_tags = []

        """
        tagの組み合わせを作成。
        [[(tag1, tag2),(tag1, tag2)...],[(tag1, tag2),(tag1, tag2)...],...]
        各ランキングごとにタグの組み合わせを作成する。
        """
        for tag_list in tags:
            combinations = []
            for tag in tag_list:
                combination_tag = [combination for combination in list(itertools.combinations(tag,2))]
                combinations.extend(combination_tag)
            combination_tags.append(combinations)
        word_associates = []

        
        #tagの組み合わせの出現回数を計算する。
        for combination_tag in combination_tags:
            word_associate = []
            for key, value in collections.Counter(combination_tag).items():
                word_associate.append([key[0], key[1], value])
            word_associates.append(word_associate)
    
        return word_associates
    
    def make_network(self,tag,dir_path=None,file_name = None):
        tag_df = tag.query("count > 1")
        tag_set = set(tag_df["tag1"].tolist() + tag_df["tag2"].tolist())

        graph = nx.Graph()
        graph.add_nodes_from(tag_set)

        for i in range(len(tag_df)):
            row_data = tag_df.iloc[i]
            graph.add_edge(row_data["tag1"],row_data["tag2"],weight=row_data["jaccard"])

        isolated_nodes = []
        
        for node in graph.nodes:
            if len([node_num for node_num in nx.all_neighbors(graph,node)]) == 0:
                isolated_nodes.append(node)
            else:
                pass

        for node in isolated_nodes:
            graph.remove_node(node)

        plt.figure(figsize = (15,15))

        pos = nx.spring_layout(graph, k=0.3) 

        pr = nx.pagerank(graph)

        nx.draw_networkx_nodes(graph, pos, node_color=list(pr.values()),
                            cmap=plt.cm.Reds,
                            alpha=0.7,
                            node_size=[60000*v for v in pr.values()])

        nx.draw_networkx_labels(graph, pos, fontsize=14, font_family='sans-serif', font_weight="bold")

        edge_width = [d["weight"] * 10 for (u, v, d) in graph.edges(data=True)]
        nx.draw_networkx_edges(graph, pos, alpha=0.4, edge_color="darkgrey", width=edge_width)

        plt.savefig("./network.png", bbox_inches="tight")


class DlSiteNetwork(CoOccurrenceNetwork):
    def make_data_frame(self, tags):
        word_associates = self.make_combination_tags(tags)
        tag_counter = self.make_count_tags(tags)


        #単語の出現回数とjaccard係数を追加
        for word_associate, counter_dict in zip(word_associates,tag_counter):
            for column in word_associate:

                #単語の出現回数を追加
                column.extend([
                    counter_dict[column[0]],
                    counter_dict[ column[1]],
                    counter_dict[column[0]] + counter_dict[column[1]]
                    ])

                #jaccard係数を追加
                column.extend([
                    column[2] / column[5]
                ])
        
        #各ランキングごとのデータフレームを作成
        rank1_100_df = pd.DataFrame(word_associates[0],columns =["tag1","tag2","count","count1","count2","union_count","jaccard"])
        rank101_200_df = pd.DataFrame(word_associates[1],columns =["tag1","tag2","count","count1","count2","union_count","jaccard"])
        rank201_300_df = pd.DataFrame(word_associates[2],columns =["tag1","tag2","count","count1","count2","union_count","jaccard"])

        return [rank1_100_df, rank101_200_df, rank201_300_df]