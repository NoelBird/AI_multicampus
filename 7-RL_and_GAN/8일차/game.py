import numpy as np
import random

import matplotlib.pyplot as plt
import matplotlib.patches as patches


class Game:
    def __init__(self, screen_width, screen_height, show_game=True):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.road_width = int(screen_width / 2)
        self.road_left = int(self.road_width / 2 + 1)
        self.road_right = int(self.road_left + self.road_width - 1)

        self.car = {"col": 0, "row": 2}
        self.block = [
            {"col": 0, "row": 0, "speed": 1},
            {"col": 0, "row": 0, "speed": 2},
        ]

        self.total_reward = 0.
        self.current_reward = 0.
        self.total_game = 0
        self.show_game = show_game

        if show_game:
            self.fig, self.axis = self._prepare_display()

    def _prepare_display(self):
        fig, axis = plt.subplots(figsize=(4, 6))
        fig.set_size_inches(4, 6)
        fig.canvas.mpl_connect('close_event', exit)
        plt.axis((0, self.screen_width, 0, self.screen_height))
        plt.tick_params(top='off', right='off',
                        left='off', labelleft='off',
                        bottom='off', labelbottom='off')

        plt.draw()
        plt.ion()
        plt.show()

        return fig, axis

    def _get_state(self):

        state = np.zeros((self.screen_width, self.screen_height))

        state[self.car["col"], self.car["row"]] = 1

        if self.block[0]["row"] < self.screen_height:
            state[self.block[0]["col"], self.block[0]["row"]] = 1

        if self.block[1]["row"] < self.screen_height:
            state[self.block[1]["col"], self.block[1]["row"]] = 1

        return state

    def _draw_screen(self):
        title = " Avg. Reward: %d Reward: %d Total Game: %d" % (
                        self.total_reward / self.total_game,
                        self.current_reward,
                        self.total_game)

        self.axis.set_title(title, fontsize=12)

        road = patches.Rectangle((self.road_left - 1, 0),
                                 self.road_width + 1, self.screen_height,
                                 linewidth=0, facecolor="#333333")
        car = patches.Rectangle((self.car["col"] - 0.5, self.car["row"] - 0.5),
                                1, 1,
                                linewidth=0, facecolor="#00FF00")
        block1 = patches.Rectangle((self.block[0]["col"] - 0.5, self.block[0]["row"]),
                                   1, 1,
                                   linewidth=0, facecolor="#0000FF")
        block2 = patches.Rectangle((self.block[1]["col"] - 0.5, self.block[1]["row"]),
                                   1, 1,
                                   linewidth=0, facecolor="#FF0000")

        self.axis.add_patch(road)
        self.axis.add_patch(car)
        self.axis.add_patch(block1)
        self.axis.add_patch(block2)

        self.fig.canvas.draw()
        plt.pause(0.0001)

    def reset(self):
        self.current_reward = 0
        self.total_game += 1

        self.car["col"] = int(self.screen_width / 2)

        self.block[0]["col"] = random.randrange(self.road_left, self.road_right + 1)
        self.block[0]["row"] = 0
        self.block[1]["col"] = random.randrange(self.road_left, self.road_right + 1)
        self.block[1]["row"] = 0

        self._update_block()

        return self._get_state()

    def _update_car(self, move):


        self.car["col"] = max(self.road_left, self.car["col"] + move)
        self.car["col"] = min(self.car["col"], self.road_right)

    def _update_block(self):

        reward = 0

        if self.block[0]["row"] > 0:
            self.block[0]["row"] -= self.block[0]["speed"]
        else:
            self.block[0]["col"] = random.randrange(self.road_left, self.road_right + 1)
            self.block[0]["row"] = self.screen_height
            reward += 1

        if self.block[1]["row"] > 0:
            self.block[1]["row"] -= self.block[1]["speed"]
        else:
            self.block[1]["col"] = random.randrange(self.road_left, self.road_right + 1)
            self.block[1]["row"] = self.screen_height
            reward += 1

        return reward

    def _is_gameover(self):
        if ((self.car["col"] == self.block[0]["col"] and
             self.car["row"] == self.block[0]["row"]) or
            (self.car["col"] == self.block[1]["col"] and
             self.car["row"] == self.block[1]["row"])):

            self.total_reward += self.current_reward

            return True
        else:
            return False

    def step(self, action):
        self._update_car(action - 1)
        escape_reward = self._update_block()
        stable_reward = 1. / self.screen_height if action == 1 else 0
        gameover = self._is_gameover()

        if gameover:
            reward = -2
        else:
            reward = escape_reward + stable_reward
            self.current_reward += reward

        if self.show_game:
            self._draw_screen()

        return self._get_state(), reward, gameover
