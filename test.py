import fizu_pygame as fpg



#setting win sizes etc


class Loop(fpg.GameLoop):
    def __init__(self):
        super().__init__()

    def init(self):
        self.player = fpg.DynamicBody((100,18))
        self.enemy = fpg.StaticBody((0,0))
        self.enemy.sprite.fill((0,0,0))

        self.hud = fpg.HUD_Sprite((0,0))
        

    def input(self):
        pass
    

    def update(self):
        self.camera.clipped_movement()

    def display(self):
        pass




loop = Loop()
loop.loop()