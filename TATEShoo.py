import math
import random
import sys
import time

import pygame as pg
from pygame.sprite import AbstractGroup

WIDTH = 600
HEIGHT = 1000

def check_bound(area: pg.Rect, obj: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内か画面外かを判定し，真理値タプルを返す
    引数1 area：画面SurfaceのRect
    引数2 obj：オブジェクト（爆弾，こうかとん）SurfaceのRect
    戻り値：横方向，縦方向のはみ出し判定結果（画面内：True／画面外：False）
    """
    yoko, tate = True, True
    if obj.left < area.left or area.right < obj.right:  # 横方向のはみ出し判定
        yoko = False
    if obj.top < area.top or area.bottom < obj.bottom:  # 縦方向のはみ出し判定
        tate = False
    return yoko, tate

class Player(pg.sprite.Sprite):
    """
    ゲームキャラクター（こうかとん）に関するクラス
    """
    _delta = {  # 押下キーと移動量の辞書
        pg.K_UP: (0, -1),
        pg.K_DOWN: (0, +1),
        pg.K_LEFT: (-1, 0),
        pg.K_RIGHT: (+1, 0),
    }

    def __init__(self, xy: tuple[int, int]):
        """
        こうかとん画像Surfaceを生成する
        引数1 num：こうかとん画像ファイル名の番号
        引数2 xy：こうかとん画像の位置座標タプル
        """
        super().__init__()
        img0 = pg.transform.rotozoom(pg.image.load(f"ex05/fig/jiki.png"), 0, 0.05)  # 左向き，2倍
        self.img = img0
        self.rct = self.img.get_rect()
        self.rct.center = xy
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0
            else:
                self.speed = 10

    def update(self, key_lst: list[bool], screen: pg.Surface):
        """
        押下キーに応じてこうかとんを移動させる
        引数1 key_lst：押下キーの真理値リスト
        引数2 screen：画面Surface
        """
        sum_mv = [0, 0]
        for k, mv in __class__._delta.items():
            if key_lst[k]:
                self.rct.move_ip(mv)
                sum_mv[0] += mv[0]  # 横方向合計
                sum_mv[1] += mv[1]  # 縦方向合計
        if check_bound(screen.get_rect(), self.rct) != (True, True):
            for k, mv in __class__._delta.items():
                if key_lst[k]:
                    self.rct.move_ip(-mv[0], -mv[1])
        screen.blit(self.img, self.rct) 




def main():
    pg.display.set_caption("はじめてのPygame")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("ex05/fig/haikei.jpg")
    bg_img = pg.transform.rotozoom(bg_img, 0, 2)
    player = Player((300, 800))
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return

        screen.blit(bg_img, [0,0])

        key_lst = pg.key.get_pressed()
        player.update(key_lst, screen)
        pg.display.update()
        clock.tick(10000)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()