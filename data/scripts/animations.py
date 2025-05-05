

class Animation:

    def __init__(self, total_delay: int):
        self.delay = -1
        self.total_delay = total_delay
        self.on_animation = False

    def check_delay(self):
        if self.delay > 0:
            self.delay -= 1
        elif self.delay == 0 and not self.on_animation:
            self.on_animation = True
            self.delay = -1

    def update(self):
        pass

class NewBlocksAnimation(Animation):
    
    def __init__(self, total_delay):
        super().__init__(total_delay)
        self.y = 0

    def update(self, blocks, delta_time: int):
        if self.y < 70:
            for block in blocks:
                block.rect.y += 500 * delta_time
            self.y += 500 * delta_time
        else:
            self.on_animation = False