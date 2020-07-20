import tkinter
import stage
import block


class Game:
    """
    class for managing the whole game
    このクラスを生成し、start()を呼び出すことで、ゲームを開始する
    """

    def __init__(self, title, width, height):
        """
        ゲームの各パラメータの状態を初期化し、ゲームを開始させる準備を整える
        title: game title
        width: screen width
        height: screen height
        """
        self.title = title
        self.width = width
        self.height = height
        self.root = tkinter.Tk()
        self.root.bind('<KeyPress>', self.__input)
        self.canvas = tkinter.Canvas(self.root, width=self.width, height=self.height, bg='black')
        self.stage = stage.Stage()

        self.img_blocks = [tkinter.PhotoImage(file='o.png'),
                           tkinter.PhotoImage(file='i.png'),
                           tkinter.PhotoImage(file='l.png'),
                           tkinter.PhotoImage(file='j.png'),
                           tkinter.PhotoImage(file='s.png'),
                           tkinter.PhotoImage(file='z.png'),
                           tkinter.PhotoImage(file='t.png')]
        """
        self.img_block = tkinter.PhotoImage(file='block.png')
        self.img_fix = tkinter.PhotoImage(file='fix.png')
        """
        self.img_shadow = tkinter.PhotoImage(file='shadow.png')
        self.img_game_over = tkinter.PhotoImage(file='game_over.png')
        self.speed = 300

    def start(self):
        """
        gameを開始させるメソッド
        """
        self.__init()

    def __init(self):
        """
        gameの初期化を行うメソッド
        """
        self.__make_window()
        self.__game_loop()
        self.root.mainloop()

    def __make_window(self):
        """
        gameの画面を作成するメソッド
        """
        self.root.title(self.title)
        self.canvas.pack()

    def __game_loop(self):
        """
        gameのメインロジックを定義するメソッドです。
        """
        self.__update()
        self.__render()
        if not self.stage.is_end():
            self.root.after(self.speed, self.__game_loop)
        else:
            self.__render(True)

    def __input(self, e):
        """
        ユーザからの入力処理を定義するメソッド
        """
        self.stage.input(e.keysym)

    def __update(self):
        """
        ゲーム全体の更新処理を定義するメソッド
        """
        self.stage.update()
        if self.stage.is_fix:
            #速度を変更
            self.speed -= 1


    def __render(self, is_end=False):
        """
        gameの描画処理を定義するメソッド
        """
        self.canvas.delete('block')

        for y in range(stage.Stage.HEIGHT):
            for x in range(stage.Stage.WIDTH):
                cell_data = self.stage.data[y][x]

                if is_end:
                    #GameOver処理を描画
                    if cell_data in stage.Stage.FIX:
                        # ゲームオーバーのブロックを描画する
                        self.canvas.create_image(x * block.Block.SCALE, y * block.Block.SCALE, image=self.img_game_over,
                                                 anchor='nw', tag='block')
                else:
                    #Game画面を描画
                    """
                    if cell_data == stage.Stage.NONE:
                        # if cell_data==NONE, color>>Black 32*32
                        self.canvas.create_rectangle(x * block.Block.SCALE, y * block.Block.SCALE, x * block.Block.SCALE + block.Block.SCALE, y * block.Block.SCALE + block.Block.SCALE, fill='black', tag='block')
                    """
                    # 取得したマスのデータがブロックだった場合
                    if cell_data in stage.Stage.BLOCK:
                        # ブロックの画像を描画する。
                        self.canvas.create_image(
                            x * block.Block.SCALE,  # x座標
                            y * block.Block.SCALE,  # y座標
                            image=self.img_blocks[cell_data-10],  # 描画画像
                            anchor='nw',  # アンカー
                            tag='block'  # タグ
                        )
                    elif cell_data in stage.Stage.FIX:
                        # Fixの画像を描画する。
                        self.canvas.create_image(x * block.Block.SCALE, y * block.Block.SCALE, image=self.img_blocks[cell_data-20], anchor='nw', tag='block')

        self.__render_shadow(is_end)



    def __render_shadow(self, is_end=False):
        """
        現在のテトリミノの影を描画するメソッド
        """
        type = self.stage.type
        rot = self.stage.rot
        x = self.stage.block.x
        # 影を描画するy座標を取得
        y = self.stage.shadow_position()

        if not is_end:
            for i in range(block.Block.SIZE):
                for j in range(block.Block.SIZE):
                    if self.stage.block.get_cell_data(type, rot, j, i) in stage.Stage.BLOCK:
                        self.canvas.create_image(
                            (j + x) * block.Block.SCALE,                       # x0座標
                            (i + y) * block.Block.SCALE,                       # y0座標
                            image=self.img_shadow,  # 描画画像
                            anchor='nw',  # アンカー
                            tag='block'  # タグ
                        )

                        """
                        self.canvas.create_rectangle((j + x) * block.Block.SCALE,                       # x0座標
                                                     (i + y) * block.Block.SCALE,                       # y0座標
                                                     (j + x) * block.Block.SCALE + block.Block.SCALE,   # x1座標
                                                     (i + y) * block.Block.SCALE + block.Block.SCALE,   # y1座標
                                                     fill='LavenderBlush2',                                      # 装飾色
                                                     outline='gray',                                  # 枠線
                                                     tag='block')
                        """

