from qdsm import MediaPlayer

"""
Neste exemplo, a classe MediaPlayer representa o media player e contém um estado atual e uma
fila de músicas a serem reproduzidas. A classe State é uma classe base abstrata que define os
métodos que devem ser implementados por cada estado específico. As classes StoppedState,
PlayingState e PausedState são estados específicos que implementam os métodos definidos
na classe State.

A máquina de estados é baseada em fila, onde cada evento é adicionado à fila e processado pelo
estado atual. Por exemplo, quando o método play() é chamado, o estado atual é responsável por
reproduzir a música atual da fila. Quando o método next() é chamado, o estado atual é responsável
por avançar para a próxima música na fila.

Para mudar de estado, a classe MediaPlayer possui um método change_state() que recebe um novo
estado como argumento e atualiza o estado atual. Isso permite que a máquina de estados mude de
estado de forma dinâmica à medida que os eventos são processados.
"""

if __name__ == '__main__':
    # Cria um objeto MediaPlayer
    player = MediaPlayer()

    # Altera o estado do objeto Player e imprime o estado atual do objeto a cada transição
    player.play() ; print(player.state)  # playing
    player.pause() ; print(player.state) # paused
    player.play() ; print(player.state)  # playing
    player.stop() ; print(player.state)  # stopped
    player.stop() ; print(player.state)  # stopped
    player.play() ; print(player.state)  # playing
    player.stop() ; print(player.state)  # stopped


