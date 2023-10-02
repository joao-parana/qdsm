from transitions import Machine
import random

class MediaPlayer:
    states = ['stopped', 'playing', 'paused']

    def __init__(self,):
        self.machine = Machine(model = self, 
                               states = MediaPlayer.states, 
                               initial = 'stopped')
        self.machine.add_transition('play', 'stopped', 'playing', before='side_efect_before')
        self.machine.add_transition('play', 'paused', 'playing', after='side_efect_after')
        self.machine.add_transition('pause', 'playing', 'paused')
        self.machine.add_transition('stop', '*', 'stopped', conditions=['is_valid'])
        self.machine.states['paused'].add_callback('enter', self.enter_state)
        print('States:')
        print(f'machine.states = {self.machine.states}')
        for state_name in self.machine.states.keys():
            state = self.machine.states[state_name]
            print(f'name = {state.name}, dynamic_methods = {state.dynamic_methods}')

    @property
    def is_valid(self):
        """ Basically a coin toss. """
        if random.random() < 0.5:
            print('is_valid: heads')
            return True
        else:
            print('is_valid: tails')
            return False
    
    def enter_state(self):
        print('enter_state called')        

    def side_efect_before(self):
        m = self.machine
        s = m.get_model_state(self)
        print('side efect before')

    def side_efect_after(self):
        print('side efect after')
        
    def side_efect_after_1(self):
        print('side efect after_1')
        
if __name__ == '__main__':
    # Cria um objeto MediaPlayer
    player = MediaPlayer()

    # Altera o estado do objeto Player e imprime o estado atual
    # do objeto a cada transição. Os efeitos colaterais e os
    # valores das conditions também são impressos.
    player.play() ; print(player.state)  # side efect before
                                         # playing
    player.pause() ; print(player.state) # paused
                                         # side efect after
    player.play() ; print(player.state)  # playing
                                         # heads or tails
    player.stop() ; print(player.state)  # stopped
                                         # tails or heads
    player.stop() ; print(player.state)  # stopped
    player.play() ; print(player.state)  # side efect before
                                         # playing
    player.stop() ; print(player.state)  # stopped
