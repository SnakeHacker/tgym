# tgym

基于[OpenAI Gym](https://gym.openai.com/)的程序化交易环境模拟器, 旨在为沪深A股基于增强学习的交易算法提供方便使用, 接近真实市场的交易环境

基于tgym的RL算法baselines repo: [tbase](https://github.com/iminders/tbase)

## Features

- 自动从tushare下载数据, 不需要你织组数据，已经下载的数据(默认目录"/tmp/tgym")不会重复下载
- 撮合规则:

  - 基于最高，最低价成交
  - 对交易量不作限制

- 下单按照A股的规则，买卖按照1手100股为基本交易单位

- 有拆分时，会根据复权因子对持仓进行相应的倍增, 以保持与真实市场一致

- gym.step() 比OpenAI gym多返回一个名为rewards的list, 包含每支股票的reward, 以方便Multi-Agent算法实现

## 安装指南

支持: MacOS/Linux(window未测试), python 2.7, python 3.5+, 推荐使用 python3.7

**依赖**

[tushare](https://github.com/waditu/tushare), [gym](https://github.com/openai/gym)

**安装**

```
git clone https://github.com/iminders/tgym
cd tgym
pip install -r requirements.txt
pip install -e .
```

## 使用

设置 tushare token[(token注册链接:https://tushare.pro/register?reg=124861)](https://tushare.pro/register?reg=124861):

```
export TUSHARE_TOKEN=YOUR_TOKEN
```

[Examples](tgym/envs)

场景                   | 实现           | action                                           | observation | reward | 使用例子
-------------------- | ------------ | ------------------------------------------------ | ----------- | ------ | -----------------
单支股票, 全仓操作, 每日先卖再买   | simple.py    | [scaled_sell_price, scaled_buy_price                                  | 市场信息+部分账户信息 | 可参数选择  | simple_test.py
多支股票平均分仓, 每日先卖再买     | average.py   | [scaled_sell_price, scaled_buy_price] * n                              | 市场信息+部分账户信息 | 可参数选择  | average_test.py
多支股票, 支持仓位控制, 每日先卖再买 | multi_vol.py | [scaled_sell_price, scaled_sell_volume, scaled_buy_price, scaled_buy_volume] * n | 市场信息+部分账户信息 | 可参数选择  | multi_vol_test.py

场景:

- [x] 单支股票, 全仓操作
- [x] 多支股票, 均匀分仓操作
- [x] 多支股票，支持仓位控制

[reward functions](tgym/envs/reward.py):

- [x] simple: 盈利=1,否则=-1
- [x] daily_return: 每日的收益率
- [x] daily_return_add_count_rate: 收益率 + 成交统计信息
- [x] daily_return_add_price_bound: 收益率 - 最高最低价与买卖价差MSE
- [x] daily_return_with_chl_penalty: 收益率 - [close,high,low]与买卖价格相应惩罚

## Contribution
- Fork this repo
- Add or change code && **Please add tests for changes**
- Test
  - step1. 设置[docker-compose](docker-compose.yml)需要的环境变量: BAZEL_USER_ROOT, OUTPUT_DIR, TUSHARE_TOKEN
  - step2. `docker-compose up`
- Send pull request

### 扩展Scenario

可以参考[average.py](tgym/envs/average.py)的写法

- 定义action
- 定义observation
- 定义reward

## TODO List(欢迎一起完善)

- [x] [Bazel build](https://bazel.build/)
- [ ] 更全面的测试用例
- [ ] 场景增加

  - [ ] 增加更多, 更有效的reward函数
  - [ ] 增加observation中信息(因子挖掘)

线上交流方式

- QQ群: 477860214
