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
        self.dy = 4
        self.invulnerable = False #無敵状態のフラグを追加
        
    def update(self, key_lst: list[bool], screen: pg.Surface):
        """
        押下キーに応じてこうかとんを移動させる
        引数1 key_lst:押下キーの真理値リスト
        引数2 screen:画面Surface
        """
        if key_lst[pg.K_SPACE]:
            self.dy = -5
            
        self.rect.centery += self.dy
        self.dy = 4
        screen.blit(self.img, self.rect)
        
    def change_img(self, num: int, screen: pg.Surface):
        """
        こうかとん画像を切り替え，画面に転送する
        引数1 num:こうかとん画像ファイル名の番号
        引数2 screen:画面Surface
        """
        self.img = pg.transform.rotozoom(pg.image.load(f"./fig/{num}.png"), 0, 2.5)
        self.img = pg.transform.flip(self.img , True, False)
        screen.blit(self.img, self.rect)
        

        
class Pipe(pg.sprite.Sprite):
    
    def __init__(self, xy: tuple[int, int], n):
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
        
class Score:
    """
    打ち落とした爆弾，敵機の数をスコアとして表示するクラス
    爆弾:1点
    敵機:10点
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
    #score.score = 50 #←スコアが10で割れ切れるとき、無敵状態（当たり判定無し）
    #score.score = 51　# ←スコアが10で割れ切れないとき、無敵状態じゃなくなる（当たり判定あり）


    tmr = 0 #timer = 0
    n_tmr = 0 #now timer = 0
    clock = pg.time.Clock()
    while True:
        key_lst = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0
            
        if not bird.invulnerable :    
            if len(pg.sprite.spritecollide(bird, pips, True)) != 0:
                return
        else :
            pass
        
        if bird.rect.centery > HEIGHT:
            return
        
        if tmr % 180 == 0: 
            r = random.randint(0, pipe.img0.get_height()//2)
            pips.add(Pipe([WIDTH+pipe.img0.get_width()//2, r], 0))
            pips.add(Pipe([WIDTH+pipe.img0.get_width()//2, HEIGHT-r], 1))
            
        if score.score % 10 == 0 and score.score != 0 :# こうかとんが10枚ごとに（10の倍数になったときに）コインを取ったとき
            n_tmr = tmr #「今の経過時間 = これまでの経過時間」の場合
            bird.invulnerable = True #無敵状態
            bird.change_img(6, screen)
            
        if tmr - n_tmr == 150: #「元々の時間 - 今の時間」　が150フレームになったときに
            bird.invulnerable = False #無敵状態じゃなくなる（土管の当たり判定再開）
            bird.change_img(3, screen)

        
        # 背景移動 第一回参照                            
        screen.blit(bg_img, [-(tmr%3200), 0])
        screen.blit(bg_r_img, [3200-(tmr%3200), 0])
        screen.blit(bg_r_img, [-(tmr%3200), 0])
        screen.blit(bg_img, [1600-(tmr%3200), 0])


        bird.update(key_lst, screen)
        pips.update()
        pips.draw(screen)
        score.update
        
        # チェック用　カウントされてスコアの判定が確認できる
        # if tmr % 100 == 0:
        #     score.score_up(1)
        
        pg.display.update()
        tmr += 1
        clock.tick(100)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
