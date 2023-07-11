import math
import random
import sys
import time

import pygame as pg


WIDTH = 1600  # ゲームウィンドウの幅
HEIGHT = 900  # ゲームウィンドウの高さ

class Bird(pg.sprite.Sprite):
    """
    ゲームキャラクター（こうかとん）に関するクラス
    """

    def __init__(self, num: int, xy: tuple[int, int]):
        """
        こうかとん画像Surfaceを生成する
        引数1 num:こうかとん画像ファイル名の番号
        引数2 xy:こうかとん画像の位置座標タプル
        """
        super().__init__()
        self.img0 = pg.transform.rotozoom(pg.image.load(f"./fig/{num}.png"), 0, 2.5)
        self.img = pg.transform.flip(self.img0, True, False)
        self.rect = self.img.get_rect()
        self.rect.center = xy
        self.dy = 7  
        
    def update(self, key_lst: list[bool], screen: pg.Surface):
        """
        押下キーに応じてこうかとんを移動させる
        引数1 key_lst:押下キーの真理値リスト
        引数2 screen:画面Surface
        """
        if key_lst[pg.K_SPACE]:
            self.dy = -9
            
        self.rect.centery += self.dy
        self.dy = 7
        screen.blit(self.img, self.rect)
        
class Pipe(pg.sprite.Sprite):
    
    def __init__(self, xy: tuple[int, int], n):
        """ 土管を生成する

        Args:
            xy (tuple[int, int]): _出現座標 画像左上
            n (_type_): _1->下向きの土管 2->上向きの土管
        """
        super().__init__()
        self.img0 = pg.transform.rotozoom(pg.image.load(f"./fig/dokan.png"), 0, 0.5)
        
        if n == 0: # 引数で0が指定されたら下向き
            self.image = pg.transform.flip(self.img0, False, True)
        elif n == 1: # 引数で1が指定されたら上向き
            self.image = pg.transform.flip(self.img0, False, False)
            
        self.rect = self.image.get_rect()
        self.rect.center = xy
        self.tmr = 0
        
    def update(self):
        """
        土管をスクロールする(位置の更新)を行う
        """
        self.rect.centerx -= 2
        if self.rect.right < 0:
            self.kill()
        
class Score:
    """
    コインを獲得した時のスコアが増える
    """
    def __init__(self):
        self.font = pg.font.Font(None, 50)
        self.color = (0, 0, 255)
        self.score = 0
        self.image = self.font.render(f"Score: {self.score}", 0, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = 100, HEIGHT-50

    def score_up(self, add):
        self.score += add

    def update(self, screen: pg.Surface):
        self.image = self.font.render(f"Score: {self.score}", 0, self.color)
        screen.blit(self.image, self.rect)
        
        
def main():
    pg.display.set_caption("flappy koukaton")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("./fig/pg_bg.jpg")
    bg_r_img = pg.transform.flip(bg_img, True, False)
    
    bird = Bird(3, (400, HEIGHT//3))
    pipe = Pipe([400, 0], 0)
    score = Score()
    pips = pg.sprite.Group()

    tmr = 0
    clock = pg.time.Clock()
    while True:
        key_lst = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0
            
        if len(pg.sprite.spritecollide(bird, pips, True)) != 0:
            return
        
        if bird.rect.centery > HEIGHT:
            return
        
        if tmr % 180 == 0: 
            r = random.randint(0, pipe.img0.get_height()//2)
            pips.add(Pipe([WIDTH+pipe.img0.get_width()//2, r], 0))
            pips.add(Pipe([WIDTH+pipe.img0.get_width()//2, r+(pipe.img0.get_height()+400)], 1))
        
        
        
        # 背景移動 第一回参照                            
        screen.blit(bg_img, [-(tmr%3200), 0])
        screen.blit(bg_r_img, [3200-(tmr%3200), 0])
        screen.blit(bg_r_img, [-(tmr%3200), 0])
        screen.blit(bg_img, [1600-(tmr%3200), 0])


        bird.update(key_lst, screen)
        pips.update()
        pips.draw(screen)
        score.update(screen)
        
        pg.display.update()
        tmr += 1 
        clock.tick(100)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
