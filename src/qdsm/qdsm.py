from transitions import Machine

class MediaPlayer:
    states = ['stopped', 'playing', 'paused']

    def __init__(self):
        self.machine = Machine(model = self, states = MediaPlayer.states, initial = 'stopped')
        self.machine.add_transition('play', 'stopped', 'playing')
        self.machine.add_transition('play', 'paused', 'playing')
        self.machine.add_transition('pause', 'playing', 'paused')
        self.machine.add_transition('stop', '*', 'stopped')

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