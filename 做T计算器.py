while True:
    ask = input("请问是正T操作还是倒T操作？（1表示正T，0表示倒T）")
    if int(ask) == 1:
        a = (input("请输入买入价格："))
        print("您的买价为：" + a)
    
        b = (input("请输入买入股数："))
        print("您买入的股数为：" + b)
    
        c = (input("请输入卖出价格："))
        print("您的卖出价格为：" + c + "，（默认您卖出的股数与买入股数相同）")
    
    else:
        c = (input("请输入卖出价格："))
        print("您的卖出价格为：" + c)
    
        b = (input("请输入卖出股数："))
        print("您卖出的股数为：" + b)
    
        a = (input("请输入买入价格："))
        print("您的买价为：" + a + "，（默认您买入的股数与卖出股数相同）")
    
    
    
    buyprice = float(a)
    buycount = float(b)
    sellprice = float(c)
    
    print("正在为您计算盈亏...")
    d = buyprice*buycount*0.0003 #佣金万分之三
    e = buycount*sellprice*0.001 #印花税千分之一，卖方单边缴税
    f = sellprice*buycount*0.0003 #佣金万分之三
    if d < 5.0:#佣金5元起征
        d = 5.0
    if f < 5.0:
        f = 5.0
    gain = sellprice*buycount - buyprice*buycount -f -d -e
    moneytake = buyprice*buycount +f +d +e
    lv = (gain / moneytake)*100
    print("↓↓↓经核算，您本次交易相关数据如下↓↓↓")
    print("买入佣金为：" + str(d))
    print("印花税为："+ str(e))
    print("卖出佣金为："+str(f))
    print("您本次交易的扣费后盈利为" + str(gain) + "元，操作盈亏比例为" + str(lv) + "%")
