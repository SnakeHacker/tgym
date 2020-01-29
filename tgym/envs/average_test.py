# -*- coding:utf-8 -*-

import datetime
import logging
import os
import random
import unittest

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters

from tgym.envs.average import AverageEnv
from tgym.market import Market

logging.root.setLevel(logging.INFO)
register_matplotlib_converters()


class TestAverage(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # NOTE: 需要在环境变量中设置 TUSHARE_TOKEN
        ts_token = os.getenv("TUSHARE_TOKEN")
        self.start = "20190101"
        self.end = "20200101"
        self.codes = ["000001.SZ", "000002.SZ"]
        # self.indexs = ["000001.SH", "399001.SZ"]
        self.indexs = []
        self.show_plot = True
        # self.indexs = []
        self.data_dir = "/tmp/tgym"
        self.m = Market(
            ts_token=ts_token,
            start=self.start,
            end=self.end,
            codes=self.codes,
            indexs=self.indexs,
            data_dir=self.data_dir)
        self.invesment = 100000.0
        self.look_back_days = 10
        self.env = AverageEnv(
            self.m,
            investment=self.invesment,
            look_back_days=self.look_back_days)

    def plot_portfolio_value(self, name):
        plt.figure(figsize=(15, 7))
        MTFmt = '%Y%m%d'
        ax = plt.gca()
        ax.xaxis.set_major_formatter(mdates.DateFormatter(MTFmt))
        plt.title(name, fontsize=10)
        dates = [datetime.datetime.strptime(d, MTFmt) for d in self.env.dates[
            self.look_back_days:]]
        plt.plot(dates,
                 self.env.portfolio_value_logs,
                 label="portfolio_value")
        plt.show()

    def test_get_open_dates(self):
        actual = self.env.get_open_dates()
        self.assertEqual(244, len(actual))

    def test_get_init_portfolio_obss(self):
        self.env.reset()
        actual = self.env.get_init_portfolio_obss()
        self.assertEqual(2, len(actual))
        self.assertEqual(10, len(actual[0]))
        self.assertEquals([[0, 0]] * self.look_back_days, actual[0].tolist())

    def test_get_init_obss(self):
        self.env.reset()
        actual = self.env.get_init_obss()
        self.assertEqual(2, len(actual))
        self.assertEqual(10, len(actual[0]))
        # TODO: 更具体的测试

    def test_get_action_price(self):
        self.env.reset()
        # pre_close: 10.24
        action, code = [-0.1, 0.1], self.codes[0]
        sell_price, buy_price = self.env.get_action_price(action, code)
        self.assertEqual(10.14, sell_price)
        self.assertEqual(10.34, buy_price)

    def test_buy_and_hold(self):
        # 20190116, 收盘涨 2.38%
        action = [0, 0.238, 0, 0.103]
        self.env.reset()
        obs, reward, done, info = self.env.step(action, only_update=False)
        action = [0] * 4
        while not done:
            # buy and hold, 持仓不动
            _, _, done, _ = self.env.step(action, only_update=True)
        self.assertEqual(144057.17, self.env.portfolio_value)
        if self.show_plot:
            self.plot_portfolio_value("buy_and_hold")

    def test_random(self):
        random.seed(0)
        # 20190116, 收盘涨 2.38%
        action = [0, 0.238, 0, 0.103]
        self.env.reset()
        obs, reward, done, info = self.env.step(action, only_update=False)
        while not done:
            # buy and hold, 持仓不动
            action = self.env.get_random_action()
            _, _, done, _ = self.env.step(action, only_update=False)
        self.assertEqual(21408.2, round(self.env.portfolio_value, 1))
        if self.show_plot:
            self.plot_portfolio_value("random_action")

    def test_static(self):
        # 20190116, 收盘涨 2.38%
        action = [0, 0.238, 0, 0.103]
        self.env.reset()
        obs, reward, done, info = self.env.step(action, only_update=False)
        action = [0.1, -0.1, 0.1, -0.1]
        while not done:
            # buy and hold, 持仓不动
            _, _, done, _ = self.env.step(action, only_update=False)
        self.assertEqual(104933.3, round(self.env.portfolio_value, 1))
        if self.show_plot:
            self.plot_portfolio_value("static")


if __name__ == '__main__':
    unittest.main()
