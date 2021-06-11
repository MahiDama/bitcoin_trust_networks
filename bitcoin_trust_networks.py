# Name: Mahotsavy Dama

"""
citation: @inproceedings{kumar2016edge,
  title={Edge weight prediction in weighted signed networks},
  author={Kumar, Srijan and Spezzano, Francesca and Subrahmanian, VS and Faloutsos, Christos},
  booktitle={Data Mining (ICDM), 2016 IEEE 16th International Conference on},
  pages={221--230},
  year={2016},
  organization={IEEE}
}

@inproceedings{kumar2018rev2,
  title={Rev2: Fraudulent user prediction in rating platforms},
  author={Kumar, Srijan and Hooi, Bryan and Makhija, Disha and Kumar, Mohit and Faloutsos, Christos and Subrahmanian, VS},
  booktitle={Proceedings of the Eleventh ACM International Conference on Web Search and Data Mining},
  pages={333--341},
  year={2018},
  organization={ACM}
}
"""

import networkx as nx
import csv
import matplotlib.pyplot as plt

# reading the csv file and converting the columns to nodes to create the graph
file1 = '/Users/mahotsavydama/Desktop/NYUdocs/Data_engineering/HW1/FoodWebs/db/RFAnet.csv'
DG = nx.DiGraph()
node = 0
with open(file1) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        node_a = int(row['node1'])
        node_b = int(row['node2'])
        DG.add_edge(node_a, node_b)
        node+=1

scc = [(len(c),c) for c in sorted(nx.strongly_connected_components \
                                       (DG), key=len, reverse=True)][0][1]
scc_list = list(scc)
# print('length of scc:', len(scc))
# print('Number of nodes: ', DG.number_of_nodes())
# # print(len(scc))
OUT_component=[]
for n in scc:
    for s in DG.successors(n):
        if s in scc:
            continue
        if not s in OUT_component:
            OUT_component.append(s)

IN_component=[]
for n in scc:
    for s in DG.predecessors(n):
        if s in scc: continue
        if not s in IN_component:
            IN_component.append(s)

# generating the subgraph
bowtie = list(scc)+IN_component+OUT_component

DG_bowtie = DG.subgraph(bowtie)

# defining the proper layout
pos={}
in_y=100.0
in_step=700.0
for in_n in IN_component:
    pos[in_n]=(100.0,in_y)
    in_y=in_y+in_step


out_y=100.0
out_step=500.0
for out_n in OUT_component:
    pos[out_n]=(200,out_y)
    out_y=out_y+out_step

# adding the positions for scc, as the number is higher in this case due to a larger data set
# in the original code both the nodes of scc are located at the top of on component
# and at the bottom of out component respectively. So the positions are adjusted to reflect this.
scc_y=100.0
scc_step=(out_y-100)/len(scc)
for scc_n in scc_list:
    pos[scc_n]=(150,scc_y)
    scc_y=scc_y+scc_step

# Drawing the graph and adding the values
# plot the bowtie structure
nx.draw(DG_bowtie, pos, node_size=50)

# adding nodes from in_components
nx.draw_networkx_nodes(DG_bowtie, pos, IN_component, \
                       node_size=100, node_color='Black')

# adding nodes from out_components
nx.draw_networkx_nodes(DG_bowtie, pos, OUT_component, \
                       node_size=100, node_color='Blue')

# adding scc nodes
nx.draw_networkx_nodes(DG_bowtie, pos, scc, \
                       node_size=200, node_color='Grey')
# pos=nx.spring_layout(DG_bowtie)
# saving the plot and showing it
plt.savefig('./RFA_final.png',dpi=600)
plt.show()

#
# # using the tropic species function to identify the number of transcators in the trust network
# def get_node_key(node):
#     out_list=[]
#     # calculating the out_list that is sellers
#     for out_edge in DG.out_edges(node):
#         out_list.append(out_edge[1])
#     in_list=[]
#     # calculating the in_list that is buyers
#     for in_edge in DG.in_edges(node):
#         in_list.append(in_edge[0])
#     out_list.sort()
#     out_list.append('-')
#     in_list.sort()
#     out_list.extend(in_list)
#     return out_list
#
#
# # using the get_node_key function to identify individuals
# def TrophicNetwork(DG):
#     trophic={}
#     for n in DG.nodes():
#         k=tuple(get_node_key(n))
#         if k not in trophic:
#             trophic[k]=[]
#         trophic[k].append(n)
#     for specie in trophic.keys():
#         if len(trophic[specie])>1:
#             for n in trophic[specie][1:]:
#                 DG.remove_node(n)
#     return DG
#
# TrophicDG=TrophicNetwork(DG)
# print()
# print("Number of individuals, S:",TrophicDG.number_of_nodes())
# print("Number of transactions, L:",TrophicDG.number_of_edges())
# print("L/S:",float(TrophicDG.number_of_edges())/\
#       TrophicDG.number_of_nodes())
# print("Connectance of the network, L/S^2:",float(TrophicDG.number_of_edges())/ \
#       (TrophicDG.number_of_nodes()*TrophicDG.number_of_nodes()))
#
#
# # identifying the basal, intermediate and top species
# def compute_classes(DG):
#     basal_species=[]
#     top_species=[]
#     intermediate_species=[]
#     for n in DG.nodes():
#         if DG.in_degree(n)==0:
#             basal_species.append(n)
#         elif DG.out_degree(n)==0:
#             top_species.append(n)
#         else:
#             intermediate_species.append(n)
#     return basal_species,intermediate_species,top_species
#
#
# (B,I,T)=compute_classes(TrophicDG)
# print()
# print("Proportion of Basal species or Sellers,B:",float(len(B))/(len(B)+len(T)+len(I)))
# print("Proportion of Intermediate species,I:",float(len(I))/(len(B)+len(T)+len(I)))
# print("Proportion of Top species or Buyers, T:",float(len(T))/(len(B)+len(T)+len(I)))
#
#
# # Identifying the number of transactions between the classes
# def InterclassLinkProportion(DG,C1,C2):
#     count=0
#     for n1 in C1:
#         for n2 in C2:
#             if DG.has_edge(n1,n2):
#                 count+=1
#     return float(count)/DG.number_of_edges()
#
# print()
# print("links in BT:",InterclassLinkProportion(TrophicDG,B,T))
# print("links in BI:",InterclassLinkProportion(TrophicDG,B,I))
# print("links in II:",InterclassLinkProportion(TrophicDG,I,I))
# print("links in IT:",InterclassLinkProportion(TrophicDG,I,T))
#
# # Ratio buyers/sellers
# print()
# print("Ratio of Sellers to buyers:",float((len(B)+len(I)))/(len(I)+len(T)))