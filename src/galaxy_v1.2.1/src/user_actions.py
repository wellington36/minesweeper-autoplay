from kivy.uix.relativelayout import RelativeLayout


def keyboard_closed(self):
	self._keyboard_unbind(on_key_down=self.on_keyboard_down)
	self._keyboard_unbind(on_key_up=self.on_keyboard_up)
	self._keyboard = None

def on_keyboard_down(self, keyboard, keycode, text, modifiers):

	if keycode[1] == 'left' or keycode[0] == 1073741904:
		self.current_speed_x = self.SPEED_X

	elif keycode[1] == 'right' or keycode[0] == 1073741903:
		self.current_speed_x = -self.SPEED_X
	
	return True


def on_keyboard_up(self, keyboard, keycode):
	self.current_speed_x = 0
	return True

def on_touch_down(self, touch):
	if not self.state_game_over and self.state_game_has_started:
		if touch.x < self.width / 2:
			self.current_speed_x = self.SPEED_X
	
		else:
			self.current_speed_x = -self.SPEED_X
	
	return super(RelativeLayout, self).on_touch_down(touch)

def on_touch_up(self, touch):
	self.current_speed_x = 0
	
# use enter keyboard do start game
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

