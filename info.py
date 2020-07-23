import tkinter
import block
import stage
import random


class Info:
    RIGHT_SECTION_WIDTH = block.Block.SCALE * block.Block.SIZE
    RIGHT_SECTION_HEIGHT = block.Block.SCALE * block.Block.SIZE



    def __init__(self):
        self.next_block_data = [[stage.Stage.NONE for i in range(block.Block.SIZE)] for j in range(block.Block.SIZE)]
        self.block = block.Block()
        self.type = 0
        self.rot = 0
        self.render_next_block()

    def render_next_block(self):
        """
        next blockのdataを右に表示するmethod
        """

        b_t = self.type
        b_r = self.rot
        b_x = self.block.x
        b_y = self.block.y

        # infoの状態を一度リセット
        for i in range(stage.Stage.HEIGHT+1, Info.RIGHT_SECTION_HEIGHT):
            for j in range(stage.Stage.WIDTH+1, Info.RIGHT_SECTION_WIDTH):
                if self.next_block_data[i][j] in stage.Stage.BLOCK:
                    self.next_block_data[i][j] = stage.Stage.NONE

        # ブロックデータをinfoに反映
        for i in range(block.Block.SIZE):
            for j in range(block.Block.SIZE):
                if self.block.get_cell_data(b_t, b_r, j, i) in Stage.BLOCK:
                    self.next_block_data[b_y + i][b_x + j] = self.block.get_cell_data(b_t, b_r, j, i)
