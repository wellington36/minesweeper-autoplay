from kivy.uix.relativelayout import RelativeLayout

def move_ship(self, direction):
    if direction == 'left':
        self.current_speed_x = self.SPEED_X
    #elif direction == 'right':
    #    self.current_speed_x = -self.SPEED_X
    #else:
    #    self.current_speed_x = 0

def on_keyboard_enter(self, keyboard, keycode):
	if self.state_game_over and not self.state_game_has_started and keyboard[1] == "enter":
		if self.state_game_over:
			self.sound_restart.play()
		else:
			self.sound_begin.play()
			
		self.sound_music1.play()
		self.reset_game()
		self.state_game_has_started = True
		self.menu_widget.opacity = 0