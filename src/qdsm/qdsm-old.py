from queue import Queue
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network

class MediaPlayer:
    def __init__(self):
        state = StoppedState(self)
        self.state = state
        self.queue = Queue()
        self.graph = nx.DiGraph()
        self.build_initial_graph()

    """
    Cada nó do grafo representa um estado e as arestas representam as transições entre
    os estados. Cada aresta tem um atributo action que representa a ação que deve ser
    executada para fazer a transição de um estado para outro.
    No método next, em vez de chamar diretamente o método next do estado atual, o código
    obtém a ação correspondente à transição do estado atual para o próximo estado a partir
    do grafo e chama o método correspondente no estado atual.
    """
    def build_initial_graph(self):
        self.graph.add_node('StoppedState')
        self.graph.add_node('PlayingState')
        self.graph.add_node('PausedState')
        self.graph.add_edge('StoppedState', 'PlayingState', action='play')
        self.graph.add_edge('PlayingState', 'PausedState', action='pause')
        self.graph.add_edge('PlayingState', 'StoppedState', action='stop')
        self.graph.add_edge('PausedState', 'PlayingState', action='play')
        self.graph.add_edge('PausedState', 'StoppedState', action='stop')

        def build_and_save_graph_using_pyvis():
            # Cria um objeto Network do vis.js
            net = Network(height='500px', width='100%', bgcolor='#ffffff', 
                font_color=True, directed=True, 
            )
            # options for nodes: https://visjs.github.io/vis-network/docs/network/nodes.html
            options = {
                'nodes': {
                    'font': '24px arial'
                }
            }
            # net.set_options(options)        Não Funcionou ! 
            net.barnes_hut(spring_length=200)

            # Adiciona os nós do grafo ao objeto Network
            for n in self.graph.nodes:
                net.add_node(n, label=n, font_size='40px', color='blue', size=30)
            # Adiciona as arestas do grafo ao objeto Network
            for e in self.graph.edges:
                net.add_edge(e[0], e[1], label=self.graph.edges[e]['action'], font={'size': 30})

            # Exibe o grafo
            html_filename = 'mygraph.html'
            # net.show(html_filename)
            net.save_graph(html_filename)
            print(f'Gráfico gerado em {html_filename}')

        build_and_save_graph_using_pyvis()

        def build_and_show_graph_using_matplotlib():
            # Define a posição dos nós no grafo usando circular_layout ou spring_layout
            pos = nx.circular_layout(self.graph)

            # Desenha os nós do grafo
            nx.draw_networkx_nodes(self.graph, pos)

            # Desenha as arestas do grafo
            nx.draw_networkx_edges(self.graph, pos, edgelist=[('StoppedState', 'PlayingState'), ('PlayingState', 'PausedState')], arrows=True, connectionstyle='arc3, rad = 0.2')
            nx.draw_networkx_edges(self.graph, pos, edgelist=[('PlayingState', 'StoppedState'), ('PausedState', 'PlayingState'), ('PausedState', 'StoppedState')], arrows=True, connectionstyle='arc3, rad = 0.3')


            # Adiciona os rótulos das arestas do grafo
            labels = nx.get_edge_attributes(self.graph, 'action')
            nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels)

            # Adiciona os rótulos dos nós do grafo
            nx.draw_networkx_labels(self.graph, pos)

            # Exibe o grafo
            plt.show()
            print('Gráfico desenhado')
        
        # build_and_show_graph_using_matplotlib()

    def change_state(self, state):
        self.state = state

    def play(self):
        self.state.play()

    def stop(self):
        self.state.stop()

    def pause(self):
        self.state.pause()

    def next(self):
        # Obtendo o atributo action da aresta do grafo que conecta o estado atual com o
        # estado PlayingState. Para isso, é utilizado o método edges da biblioteca networkx,
        # que retorna um dicionário com todas as arestas do grafo. O índice do dicionário
        # é uma tupla com o nome do estado atual e o nome do estado de destino da transição.
        # O nome do estado atual é obtido através do método __class__.__name__, que retorna
        # o nome da classe do objeto self.state.
        actual_state = self.state.__class__.__name__
        action = self.graph.edges[actual_state, 'PlayingState']['action']
        # Utilizamos a função getattr do Python para obter o método correspondente à ação
        # obtida na linha anterior. A função getattr recebe dois argumentos: o primeiro é
        # o objeto do qual se deseja obter o método e o segundo é o nome do método. Nesse
        # caso, o objeto é self.state e o nome do método é o valor da variável action.
        next_action = getattr(self.state, action)
        next_action()

    def previous(self):
        self.state.previous()

    def add_to_queue(self, song):
        self.queue.put(song)

    def play_from_queue(self):
        if not self.queue.empty():
            song = self.queue.get()
            print(f"Playing song: {song}")
        else:
            print("Queue is empty")

class State:
    def __init__(self, player):
        self.player = player

    def play(self):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()

    def pause(self):
        raise NotImplementedError()

    def next(self):
        raise NotImplementedError()

    def previous(self):
        raise NotImplementedError()

class StoppedState(State):
    def play(self):
        self.player.change_state(PlayingState(self.player))
        self.player.play_from_queue()

    def stop(self):
        print("Already stopped")

    def pause(self):
        print("Cannot pause, player is stopped")

    def next(self):
        print("Cannot play next, player is stopped")

    def previous(self):
        print("Cannot play previous, player is stopped")

class PlayingState(State):
    def play(self):
        print("Already playing")

    def stop(self):
        self.player.change_state(StoppedState(self.player))

    def pause(self):
        self.player.change_state(PausedState(self.player))

    def next(self):
        self.player.play_from_queue()

    def previous(self):
        print("Cannot play previous, already at the beginning of the queue")

class PausedState(State):
    def play(self):
        self.player.change_state(PlayingState(self.player))

    def stop(self):
        self.player.change_state(StoppedState(self.player))

    def pause(self):
        print("Already paused")

    def next(self):
        self.player.play_from_queue()

    def previous(self):
        print("Cannot play previous, already at the beginning of the queue")

if __name__ == "__main__":
    media_player = MediaPlayer()

    media_player.play()
    media_player.pause()
    media_player.stop()
    media_player.next()
    media_player.previous()

    media_player.add_to_queue("Song 1")
    media_player.add_to_queue("Song 2")
    media_player.add_to_queue("Song 3")

    media_player.play()
    media_player.pause()
    media_player.next()
    media_player.previous()
    media_player.next()
    media_player.next()
    media_player.next()
    media_player.previous()
    media_player.previous()
    media_player.previous()
