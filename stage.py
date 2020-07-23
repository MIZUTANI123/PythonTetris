import block
import random


class Stage:
    """
    テトリスの盤面を管理するクラスです。
    """
    WIDTH = 10 # 盤面の幅
    HEIGHT = 20 # 盤面の幅高さ
    NONE = 0 # 空マス
    BLOCK = [10, 11, 12, 13, 14, 15, 16]  # ブロックマス
    FIX = [20, 21, 22, 23, 24, 25, 26, 27] # 固定ブロックマス


    def __init__(self):
        """
        盤面の生成
        """
        self.data = [[Stage.NONE for i in range(Stage.WIDTH)] for j in range(Stage.HEIGHT)]
        self.block = block.Block()

        self.type = 0
        self.rot = 0
        self.next_type = 0
        self.next_rot = 0
        self.can_drop = True
        self.remove_line = [False for i in range(Stage.HEIGHT)]
        self.is_fix = False
        self.__select_block()
        self.__select_next_block()
        self.cnt = 0
        self.lines = 0
        self.score = 0


    def update(self):
        """
        stageの更新処理を行うmethod
        """
        self.__marge_block()

        #もし下方向に衝突しない場合
        if not self.is_collision_bottom():
            self.is_fix = False
            if self.can_drop:
                self.__drop_block()
        #もし下方向に衝突する場合
        else:
            self.is_fix = True
            self.__fix_block()
            self.check_remove_lines()
            self.remove_lines()
            self.add_scores()
            self.block.reset()
            self.update_block()
            self.__select_next_block()




    def input(self, key):
        """
        キー入力を受け付けるメソッド
        各キーの入力に対しての処理を記述
        Wキー
        Aキー
        Sキー
        Dキー
        """
        if key == 'space':
            self.can_drop = not self.can_drop
        if key == 'w':
            self.__rotation_block()
        if key == 'a':
            if not self.is_collision_left():
                self.block.x -= 1
        if key == 's':
            self.hard_drop()
        if key == 'd':
            if not self.is_collision_right():
                self.block. x += 1

    def __select_block(self):
        """
        blockのタイプと角度をランダムに選択する。
        """
        self.type = random.randint(0, block.Block.TYPE_MAX-1)
        self.rot = random.randint(0, block.Block.ROT_MAX-1)


    def __select_next_block(self):
        """
        blockのタイプと角度をランダムに選択する。
        """
        self.next_type = random.randint(0, block.Block.TYPE_MAX-1)
        self.next_rot = random.randint(0, block.Block.ROT_MAX-1)


    def __rotation_block(self):
        if self.__can_rotation_block():
            self.rot = (self.rot + 1) % block.Block.ROT_MAX

    def __can_rotation_block(self):
        """
        現在のblockが回転可能かを判定するmethod。回転可能ならTrueとする
        """

        n_rot = (self.rot + 1) % block.Block.ROT_MAX
        b_x = self.block.x
        b_y = self.block.y

        for i in range(block.Block.SIZE):
            for j in range(block.Block.SIZE):
                # 次の角度のブロック情報を取得する
                if self.block.get_cell_data(self.type, n_rot, j, i) in Stage.BLOCK:
                    if self.is_out_of_stage(b_x + j, b_y + i):
                        return False
                    # 固定ブロックとの衝突チェック
                    if self.data[b_y + i][b_x + j] in Stage.FIX:
                        return False
        return True




    def __drop_block(self):
        """
        blockを一段下げるメソッド
        """
        self.block.y +=1

    def __marge_block(self):
        """
        stageのdataにblockのdataをmargeするmethod
        """

        b_t = self.type
        b_r = self.rot
        b_x = self.block.x
        b_y = self.block.y

        # Stageの状態を一度リセット
        for i in range(Stage.HEIGHT):
            for j in range(Stage.WIDTH):
                if self.data[i][j] in Stage.BLOCK:
                    self.data[i][j] = Stage.NONE

        # ブロックデータをステージに反映
        for i in range(block.Block.SIZE):
            for j in range(block.Block.SIZE):
                if self.block.get_cell_data(b_t, b_r, j, i) in Stage.BLOCK:
                    if not self.is_out_of_stage(b_x + j, b_y + i):
                        self.data[b_y + i][b_x + j] = self.block.get_cell_data(b_t, b_r, j, i)

    def __fix_block(self):
        """
        blockを固定するmethod
        """
        b_t = self.type
        b_r = self.rot
        b_x = self.block.x
        b_y = self.block.y

        for i in range(block.Block.SIZE):
            for j in range(block.Block.SIZE):
                if self.block.get_cell_data(b_t, b_r, j, i) in Stage.BLOCK:
                    self.data[b_y + i][b_x + j] = self.block.get_cell_data(b_t, b_r, j, i) + 10


    def is_out_of_stage(self, x, y):
        """
        指定されたステージの座標が範囲外かを調べるmethod
        x: stagecell x軸
        y: stagecell y軸
        """
        return x < 0 or x >= Stage.WIDTH or y < 0 or y >= Stage.HEIGHT

    def is_collision_bottom(self, x=-1, y=-1):
        """
        下方向の衝突判定を行うmethod
        衝突していればTrueが返却され、そうでなければFalseが返却される。
        x: 対象のブロックのx座標
        y: 対象のブロックのy座標
        """

        b_t = self.type
        b_r = self.rot

        if x == -1 and y == -1:
            x = self.block.x
            y = self.block.y

        for i in range(block.Block.SIZE):
            for j in range(block.Block.SIZE):
                # 取得したブロックの1マスのデータがBLOCK(1)だった場合
                if self.block.get_cell_data(b_t, b_r, j, i) in Stage.BLOCK:
                    # 対象のブロックマスの位置から一つ下げたマスがステージの範囲外だった場合
                    if self.is_out_of_stage(x + j, y + i + 1):
                        return True
                    # 対象のブロックマスの位置から一つ下げたマスが固定されたブロックのマス(2)だった場合
                    if self.data[y + i + 1][x + j] in Stage.FIX:
                        return True
        # どの条件にも当てはまらない場合は常にどこにも衝突していない
        return False

    def is_collision_left(self, x=-1, y=-1):
        """
        左方向の衝突判定を行うmethod
        衝突していればTrueが返却され、そうでなければFalseが返却される。
        x: 対象のブロックのx座標
        y: 対象のブロックのy座標
        """

        b_t = self.type
        b_r = self.rot

        if x == -1 and y == -1:
            x = self.block.x
            y = self.block.y

        for i in range(block.Block.SIZE):
            for j in range(block.Block.SIZE):
                # 取得したブロックの1マスのデータがBLOCK(1)だった場合
                if self.block.get_cell_data(b_t, b_r, j, i) in Stage.BLOCK:
                    # 対象のブロックマスの位置から一つ左のマスがステージの範囲外だった場合
                    if self.is_out_of_stage(x + j - 1, y + i):
                        return True
                    # 対象のブロックマスの位置から一つ左のマスが固定されたブロックのマス(2)だった場合
                    if self.data[y + i][x + j - 1] in Stage.FIX:
                        return True
        # どの条件にも当てはまらない場合は常にどこにも衝突していない
        return False

    def is_collision_right(self, x=-1, y=-1):
        """
        左方向の衝突判定を行うmethod
        衝突していればTrueが返却され、そうでなければFalseが返却される。
        x: 対象のブロックのx座標
        y: 対象のブロックのy座標
        """

        b_t = self.type
        b_r = self.rot

        if x == -1 and y == -1:
            x = self.block.x
            y = self.block.y

        for i in range(block.Block.SIZE):
            for j in range(block.Block.SIZE):
                # 取得したブロックの1マスのデータがBLOCK(1)だった場合
                if self.block.get_cell_data(b_t, b_r, j, i) in Stage.BLOCK:
                    # 対象のブロックマスの位置から一つ右のマスがステージの範囲外だった場合
                    if self.is_out_of_stage(x + j + 1, y + i):
                        return True
                    # 対象のブロックマスの位置から一つ右のマスが固定されたブロックのマス(2)だった場合
                    if self.data[y + i][x + j + 1] in Stage.FIX:
                        return True
        # どの条件にも当てはまらない場合は常にどこにも衝突していない
        return False

    def hard_drop(self):
        while not self.is_collision_bottom():
            self.__drop_block()

    

    def check_remove_lines(self):
        for i in range(Stage.HEIGHT):
            flg = True
            for j in range(Stage.WIDTH):
                if self.data[i][j] not in Stage.FIX:
                    flg = False
                    break
            self.remove_line[i] = flg



    def remove_lines(self):

        # そろっている列を削除
        for i in range(Stage.HEIGHT):
            if self.remove_line[i]:
                for j in range(Stage.WIDTH):
                    self.data[i][j] = Stage.NONE
                self.cnt +=1

        # 置き換え先の列を参照するポインタ
        idx = Stage.HEIGHT - 1

        # そろっている列を積み上げなおす
        for i in reversed(range(Stage.HEIGHT)):
            if not self.remove_line[i]:
                for j in range(Stage.WIDTH):
                    self.data[idx][j] = self.data[i][j]
                idx -= 1

    def add_scores(self):
        if self.cnt != 0:
            self.lines += self.cnt
            self.score += 100 * pow(2, self.lines - 1)
            self.cnt = 0

    def update_block(self):
        self.type = self.next_type
        self.rot = self.next_rot

    def shadow_position(self):
        """
        テトリミノの影を作るy軸座標を計算してそのy軸座標を返却
        """
        # 現在のブロックの座標を退避
        tx = self.block.x
        ty = self.block.y

        while not self.is_collision_bottom(tx, ty):
            ty += 1

        return ty

    def is_end(self):
        """
        tetrisのゲームオーバの判定
        オーバーならTrueとする
        """
        t = self.type
        r = self.rot
        x = self.block.x
        y = self.block.y

        for i in range(block.Block.SIZE):
            for j in range(block.Block.SIZE):
                cell_data = self.block.get_cell_data(t, r, j, i)
                if cell_data in Stage.BLOCK:
                    # 範囲外チェック
                    if not self.is_out_of_stage(x + j, y + i):
                        #衝突チェック
                        if self.data[y + i][x + j] in Stage.FIX:
                            return True
        # どの条件にも当てはまらない場合は常にどこにも衝突していない
        return False
















