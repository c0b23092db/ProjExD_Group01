import os
import sys
import pygame as pg
import random

WIDTH,HEIGHT = 1280,720
FRAMERATE = 60
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Player():
    '''クリック対象の作成
    中心は320,360
    クリック判定はmain'''
    def __init__(self,defsize :float):
        self.defsize =defsize
        self.size = defsize
        #self.img=pg.Surface((2*defsize, 2*defsize))
        #pg.draw.circle(self.img, (150,130,100), (defsize, defsize), defsize)
        self.img = pg.transform.rotozoom(pg.image.load(f"image/Click_Image.png"), 0, self.size)
        self.img.set_colorkey((0, 0, 0))
        self.rct: pg.Rect = self.img.get_rect()
        self.rct.center = (320,360)
    
    def change_img(self,screen): #クリックされたときsizeを50
        self.size = self.defsize+0.1 #大きくする

    def update(self,screen,score): 
        if self.size > self.defsize:
            self.size -= 0.01
        else:
            self.size = self.defsize
        #self.img=pg.Surface((2*self.size, 2*self.size))
        #pg.draw.circle(self.img, (150,130,100), (self.size, self.size), self.size)
        self.img = pg.transform.rotozoom(pg.image.load(f"image/Click_Image.png"), 0, self.size+score/10000)
        self.img.set_colorkey((0, 0, 0))
        self.rct: pg.Rect = self.img.get_rect()
        self.rct.center = (320,360)
        screen.blit(self.img, self.rct) 

class Reinforcement(pg.sprite.Sprite):
    '''
    total_output -> totalを入れる
    timer_clock -> フレーム
    total_input -> 消費する量
    '''
    def box(self,x,y):
        self.font = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体",25)
        # box
        self.image_box = pg.Surface((WIDTH/2-200,100))
        pg.draw.rect(self.image_box,(55,55,55),(WIDTH/2-200,0,WIDTH/2+200,100))
        self.rect_box = self.image_box.get_rect()
        self.rect_box.center = x,y
        # Image
        self.image_image = pg.transform.rotozoom(pg.image.load(f"image\Reinforcement_Image_{self.num}.png"),0,0.2)
        self.rect_image = self.image_image.get_rect()
        self.rect_image.center = x-150,y
        # name
        self.font = pg.font.Font(None,50)
        self.text_name = self.font.render(str(self.name), True, (255, 255, 255))
        self.rect_text_name = self.text_name.get_rect()
        # output
        self.text_output = self.font.render(str(""), True, (255, 255, 255))
        self.rect_text_output = self.text_output.get_rect()
        # counter
        self.text_counter = self.font.render(str(""), True, (255, 255, 255))
        self.rect_text_counter = self.text_counter.get_rect()

    def draw(self,screen,x,y):
        self.font = pg.font.Font(None,50)
        self.text_output = self.font.render(str(self.powerup_count),True,(255, 255, 255))
        self.font = pg.font.Font(None,100)
        self.text_counter = self.font.render(str(self.object_number),True,(255, 255, 255))
        screen.blit(self.image_box,self.rect_box)
        screen.blit(self.image_image,self.rect_image)
        screen.blit(self.text_name,(x-100,y-30))
        screen.blit(self.text_output,(x-100,y+15))
        screen.blit(self.text_counter,(int(x+200-len(str(self.object_number))*40),y-25))

    def __init__(self,name,num,x,y,total_output,timer_clock,total_input) -> None:
        super().__init__()
        self.name = name
        self.num = num
        self.x = x
        self.y = y
        self.total_output = total_output
        self.powerup_count = total_output
        self.timer_clock = timer_clock
        self.total_input = total_input
        self.object_number = 0
        self.box(x,y)

    def check(self, pos):
       return self.rect_box.collidepoint(pos)

    def counter(self,total):
        if total >= self.powerup_count:
            self.object_number += 1
            return self.powerup_count
        else:
            return 0

    def update(self,screen:pg.Surface):
        self.powerup_count = self.total_output+self.object_number*int(self.object_number*2+self.total_output/4)
        self.draw(screen,self.x,self.y)

class Total():  # ここ
    '''現在の総数'''
    def __init__(self) -> None:
        """変数の初期化"""
        self.fonto = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 75)
        self.color = (255, 255, 255)
        self.sum = 0
        self.total = 0
        self.img = self.fonto.render(f"{self.total}:崛起ー", 0, self.color)
        self.centery = (WIDTH/4/2, 120)

    def update(self, total, screen):
        """数値を更新"""
        self.total = int(total)  # int表示算
        total = 0
        if self.total < 10000:
            total = self.total
            self.img = self.fonto.render(f"{total}:スコア", 0, self.color)
        elif self.total >= 10000:  # 本家を見習って表示変更（必要なら億も実装）
            total = round(self.total/10000, 4)
            self.img = self.fonto.render(f"{total}万:スコア", 0, self.color)
        screen.blit(self.img, self.centery)

class FallingImage(pg.sprite.Sprite):
    def __init__(self, image_path):
        super().__init__()
        self.original_image = pg.image.load(image_path)
        self.image = pg.transform.scale(self.original_image,(self.original_image.get_width()//5,self.original_image.get_height()//5))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, (WIDTH//2)-self.rect.width)
        self.rect.y = -self.rect.height

    def update(self):
        self.rect.y += 5
        if self.rect.y > HEIGHT:
            self.kill()


def main():
    pg.display.set_caption("こうかとんクリッカー")
    screen = pg.display.set_mode((WIDTH,HEIGHT))
    bg_img = pg.image.load(f"image/background.jpg")
    falling_images = pg.sprite.Group()
    player = Player(2)
    reinforcement_list = [["finger",5,FRAMERATE,1],["Finger?",20,FRAMERATE/2,1],["GOD!",100,FRAMERATE/6,1],["Death;)",1000,1,1]]
    r_blocks = pg.sprite.Group()
    for y,(q,w,e,r) in zip(range(len(reinforcement_list)),reinforcement_list):
        r_blocks.add(Reinforcement(q,y,WIDTH/4*3,100+y*125,w,e,r))
    total = Total()
    total.value = 0
    total_sum = 0
    click_volume = 1
    timer = 0
    clock = pg.time.Clock()
    font = pg.font.Font(None,80)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0
            if event.type == pg.KEYDOWN:
                # デバッグ：増減
                if event.key == pg.K_z:
                    total.value -= 10000
                if event.key == pg.K_x:
                    total.value += 10000
                print(total.value)
            if event.type == pg.MOUSEBUTTONDOWN:
                mouseX,mouseY = event.pos
                for r_block in r_blocks:
                    if r_block.check(event.pos):
                        total.value -= r_block.counter(total.value)
                        print(total.value,r_block.y)
                if 220<= mouseX and mouseX <= 420: #xのあたり範囲　ターゲットの中心320,360
                    if 260<= mouseY and mouseY <= 460: # yのあたり範囲
                        # マウスクリック
                        total.value += click_volume
                        player.change_img(screen)
                print(f"mouse moved -> ({mouseX},{mouseY})")

        total_sum = 0
        click_volume = 1
        for r_block in r_blocks:
            click_volume += int((r_block.total_input * r_block.object_number) / 2)
            if timer % r_block.timer_clock == 0:
                total_sum += r_block.total_input * r_block.object_number
        total.value += total_sum

        spawn_probability = min(0.1+(total_sum/1000) **2,10)
        if random.random() < spawn_probability:
            new_image = FallingImage(f"image/fall/{random.randint(1,2)}.png")
            falling_images.add(new_image)
        
        screen.blit(bg_img,(0,0))
        screen.fill((50, 50, 50), rect = (WIDTH/2,0,WIDTH,HEIGHT))
        falling_images.update()
        falling_images.draw(screen)
        player.update(screen,total.value)
        r_blocks.update(screen)
        screen.blit(font.render("Timer:"+str(int(timer/FRAMERATE)), True, (255, 255, 255)),(50,50))
        total.update(total.value,screen)  # クッキーの合計量の更新
        timer += 1
        clock.tick(FRAMERATE)
        pg.display.update()

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()