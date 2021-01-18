import tkinter as tk
from tkinter import filedialog as fd
import networkx as nx
from Graph import graph_custom
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure


class GUI_graph:
    def __init__(self):
        self.window = tk.Tk(className="Анализ локальных и структурных характеристик больших сетей")
        self.frame = tk.Frame(self.window)
        self.window.geometry('1000x1000')
        info = tk.Frame(self.window)    # расположение информации в интерфейсе о графе

        self.button = tk.Button(info, text="Открыть файл(.net)", command=self._open)
        # лейблы текстов в интерфейсе
        self.nodes_text = tk.Label(info)
        self.edges_text = tk.Label(info)
        self.closeness_centrality = tk.Label(info)
        self.degree_centrality = tk.Label(info)
        self.netowork_dia_text = tk.Label(info)
        self.betweenness_centrality = tk.Label(info)
        self.density_text = tk.Label(info)
        self.average_clus_text = tk.Label(info)
        self.max_clus_text = tk.Label(info)
        self.average_distance_text = tk.Label(info)
        self.network_commun_text = tk.Label(info)
        # упаковка текстовых лейблов сверху
        info.pack()
        self.button.pack(side=tk.BOTTOM)
        self.closeness_centrality.pack(side=tk.BOTTOM)
        self.degree_centrality.pack(side=tk.BOTTOM)
        self.betweenness_centrality.pack(side=tk.BOTTOM)
        self.netowork_dia_text.pack(side=tk.BOTTOM)
        self.density_text.pack(side=tk.BOTTOM)
        self.average_clus_text.pack(side=tk.BOTTOM)
        self.max_clus_text.pack(side=tk.BOTTOM)
        self.average_distance_text.pack(side=tk.BOTTOM)
        self.edges_text.pack(side=tk.BOTTOM)
        self.nodes_text.pack(side=tk.BOTTOM)
        self.network_commun_text.pack(side=tk.BOTTOM)
        # создание место вывода графа
        self.fig = Figure(figsize=(5, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.window)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.ax = self.fig.add_subplot(111)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.frame.pack()
        # создаем объект класса graph для дальнейщего взаимодействия
        self.G = graph_custom()
        # переменная отвечающая за количество сетей в графе
        self.community = 1
        # бесконечный цикл окна
        self.window.mainloop()
    # функция открытия файла графа
    def _open(self):
        # открываем файл и записываем путь в метод класса graph_custom
        self.G.read_from_file(fd.askopenfile(title="Выберите граф", filetypes=(("pajek format", "*.net"),)).name)
        # выводим информацию в тех лейблах что создавали в инциацлизации
        self.nodes_text.configure(text="вершин: " + str(self.G.g.number_of_nodes()))
        self.edges_text.configure(text="связей: " + str(self.G.g.number_of_edges()))
        self.netowork_dia_text.config(text="диаметр графа: " + str(self.G.get_diameter()))
        self.closeness_centrality.configure(text="важная вершина по близоски: " + str(self.G.get_closeness_centrality()))
        self.degree_centrality.configure(text="по числу ребер: " + str(self.G.get_degree_centrality()))
        self.betweenness_centrality.configure(text="по степени сотрудничества: " + str(self.G.get_betweenness_centrality()))
        self.average_clus_text.config(text="среднее знач. кластеризации: " + str(self.G.get_average_clustering()))
        self.max_clus_text.config(text="макс знач. кластеризации: " + str(self.G.get_max_clustering()))
        self.density_text.config(text="плотность графа: " + str(self.G.get_density()))
        self.average_distance_text.config(text="среднее расстояние между вершинами: " + str(self.G.get_average_shortest_path_length()))
        self.community = self.G.get_comminity() # получаем сообщества
        self.network_commun_text.config(text="сетевых сообществ: "+ str(len(self.community)))
        # выводим в консоль общую информацию о графах
        print(nx.info(self.G.g))
        self.drawing()
    # функция задания в графе сообществ в качестве параметра у вершины
    def set_node_community(self, G, communities):
        for c, v_c in enumerate(communities):
            for v in v_c:
                G.nodes[v]['community'] = c + 1
    # получение цвета для раскраски различных сообществе
    def get_color(self, i, r_off=1, g_off=1, b_off=1):
        n = 16
        low, high = 0.1, 0.9
        span = high - low
        r = low + span * (((i + r_off) * 3) % n) / (n - 1)
        g = low + span * (((i + g_off) * 5) % n) / (n - 1)
        b = low + span * (((i + b_off) * 7) % n) / (n - 1)
        return (r, g, b)
    # функция рисования на фигуре ранее созданной в окне
    def drawing(self):
        self.ax.clear()
        x = self.G.g  # получаем граф, чтобы оригинал не трогать
        self.set_node_community(x, self.community) # задаем параметры в вершинах сообщества
        node_color=[self.get_color(x.nodes[v]['community']) for v in x.nodes] # получаем цвета
        nx.draw(x, with_labels=True, ax=self.ax, node_color=node_color) # рисуем
        self.canvas.draw()

# запуск программы
if __name__ == '__main__':
    GUI_graph()
