import math
import random
import sys
import time

import pygame as pg
from pygame.sprite import AbstractGroup

WIDTH = 500
HEIGHT = 600
star_points = [
    (0, -50), (14, -20), (47, -15), (23, 7),
    (29, 40), (0, 25), (-29, 40), (-23, 7),
    (-47, -15), (-14, -20)

] #星の生成

def check_bound(obj: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内か画面外かを判定し，真理値タプルを返す
    引数 obj：オブジェクト（自機）SurfaceのRect
    戻り値：横方向，縦方向のはみ出し判定結果（画面内：True／画面外：False）
    """
    yoko, tate = True, True
    if obj.left < 0 or WIDTH < obj.right:  # 横方向のはみ出し判定
        yoko = False
    if obj.top < 0 or HEIGHT < obj.bottom:  # 縦方向のはみ出し判定
        tate = False
    return yoko, tate

class Player(pg.sprite.Sprite):
    """
    自機に関するクラス
    """
    delta = {  # 押下キーと移動量の辞書
        pg.K_UP: (0, -1),
        pg.K_DOWN: (0, +1),
        pg.K_LEFT: (-1, 0),
        pg.K_RIGHT: (+1, 0),
    }

    def __init__(self, xy: tuple[int, int]):
        """
        自機画像Surfaceを生成する
        引数2 xy：自機画像の位置座標タプル
        """
        super().__init__()
        img0 = pg.transform.rotozoom(pg.image.load(f"ex05/fig/jiki.png"), 0, 0.04)  # 左向き，2倍
        self.img = img0
        self.rect = self.img.get_rect()
        self.rect.center = xy
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0
            else:
                self.speed = 7

    def update(self, key_lst: list[bool], screen: pg.Surface):
        """
        押下キーに応じて自機を移動させる
        引数1 key_lst：押下キーの真理値リスト
        引数2 screen：画面Surface
        """
        sum_mv = [0, 0]
        for k, mv in __class__.delta.items():
            if key_lst[k]:
                self.rect.move_ip(+self.speed*mv[0], +self.speed*mv[1])
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        if check_bound(self.rect) != (True, True):
            for k, mv in __class__.delta.items():
                if key_lst[k]:
                    self.rect.move_ip(-self.speed*mv[0], -self.speed*mv[1])
        screen.blit(self.img, self.rect) 

class Beam(pg.sprite.Sprite):
 
    def __init__(self, player: Player):
        """
        ビーム画像Surfaceを生成する
        引数 bird：ビームを放つ
        """ 
        
        super().__init__()
        self.image = pg.transform.rotozoom(pg.image.load(f"ex05/fig/beam.png"), 0, 0.7)
        self.rect = self.image.get_rect()
        self.rect.center = player.rect.center
        self.speed = 10

    def update(self,screen):
        """
        ビームを速度ベクトルself.vx, self.vyに基づき移動させる
        引数 screen：画面Surface
        """
        self.rect.move_ip(0,-self.speed)
        screen.blit(self.image,self.rect)
        #print(self.rct.center)
        if check_bound(self.rect) != (True, True):
            self.kill()

class Enemy(pg.sprite.Sprite):
    """
    敵Surfaceを生成する
    敵の生成は、出現方向、上下位置ともにランダム。
    出現した方向によって動きを変える。
    """

    def __init__(self):
        super().__init__()
        self.image = pg.transform.rotozoom(pg.image.load("ex05/fig/tekibig.png"), 0, 0.03)
        self.rect = self.image.get_rect()
        self.direction = random.randint(1,1000) #方向を決める数値
        if self.direction < 500:
            self.rect.centerx = 0
        else:
            self.rect.centerx = 500
        self.rect.centery = random.randint(0,150)
        print("deta")  #出現したタイミングと、Surfaceの位置を監視する
        print(self.rect)
    
    def update(self):
        if self.direction < 500 : #
            self.rect.move_ip(2,1)
            if self.rect.left > 100:
                self.rect.move_ip(0, -1)
            if self.rect.left > 480:
                self.rect.move_ip(0, -1)
        else :
            self.rect.move_ip(-2, 1)
            if self.rect.left > 100:
                self.rect.move_ip(0, -1)
            if self.rect.left > 480:
                self.rect.move_ip(0, -1)
        if self.rect.right < 0:
            self.kill()
        if self.rect.left > 600:
            self.kill()

class Score:
    """
    打ち落とした爆弾，敵機の数をスコアとして表示するクラス
    敵機：10点
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

class Star:
    """
    スターに関するクラス
    一定の確率で画面外から降ってくる
    """
    def __init__(self):
        self.x = random.randint(-WIDTH, WIDTH)
        self.y = random.randint(-100, 0)
        self.speed_x = random.uniform(1,2)
        self.speed_y = random.uniform(2, 1)
        self.scale = random.uniform(0.04, 0.25)

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
    def draw(self, screen):
        transformed_points = [(point[0] * self.scale + self.x, point[1] * self.scale + self.y) for point in star_points]
        pg.draw.polygon(screen, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), transformed_points)

stars = []
for _ in range(1):
    stars.append(Star())

class Explosion(pg.sprite.Sprite):
    """
    爆発エフェクトに関するクラス
    """

    def __init__(self,enemy:Enemy):
        """
        爆弾が爆発するエフェクトを生成する
        引数 enemy：爆発する敵インスタンス
        """
        super().__init__()
        img = pg.image.load("ex05/fig/explosion.gif")
        img = pg.transform.rotozoom(img, 0, 0.1)
        self.imgs = [img, pg.transform.flip(img, 1, 1)] # 通常の画像と、左右上下を反転させた画像
        self.image = self.imgs[0]
        self.rect = self.image.get_rect(center=enemy.rect.center)
        self.life = 50 # 表示時間を200に設定
    
    def update(self,screen:pg.Surface):
        """
        爆発時間を1減算した爆発経過時間_lifeに応じて爆発画像を切り替えることで
        爆発エフェクトを表現する
        引数 screen：画像Surface
        """
        self.life -= 1
        self.image = self.imgs[self.life//10%2] # 時間が経過するごとに交互に画像を変更させる
        screen.blit(self.image,self.rect)
        if self.life < 0:
            self.kill()


def main():
    pg.display.set_caption("はじめてのPygame")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("ex05/fig/haikei.jpg")
    bg_img = pg.transform.rotozoom(bg_img, 0, 2)
    bg_img2 = pg.image.load("ex05/fig/haikei.jpg")
    bg_img2  = pg.transform.flip(pg.transform.rotozoom(bg_img2, 0, 2), False, True) #変えた（森川）
    player = Player((250, 500))
    emys = pg.sprite.Group()
    tmr = 0
    tmrs=0
    clock = pg.time.Clock()
    score=Score()
    beams = pg.sprite.Group()
    exps = pg.sprite.Group()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                beams.add(Beam(player))

        screen.blit(bg_img, [0,0])

        #screen.blit(bg_img, [0,0])
        y = tmr % 1200
        screen.blit(bg_img, [0, -y])
        screen.blit(bg_img2, [0, 600-y])
        screen.blit(bg_img, [0, 1200-y])

        if tmr%200 == 0:  # 200フレームに1回，敵機を出現させる

            emys.add(Enemy())
        if tmrs<=199:
            if tmr%100==0:
                tmrs+=1
        if tmr%20==0:
            score.score_up(1)


        for emy in pg.sprite.groupcollide(emys, beams, True, True).keys():
            exps.add(Explosion(emy))
            score.score_up(10)

        key_lst = pg.key.get_pressed()
        emys.update()
        emys.draw(screen)
        beams.update(screen)
        exps.update(screen)
        exps.draw(screen) 
        player.update(key_lst, screen)
        score.update(screen)
        if random.random() < 0.1:  # 星が出る確率(ここから)
            star = Star()
            stars.append(star)
        for star in stars:
            star.update()
            star.draw(screen) #(ここまで変えた)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()