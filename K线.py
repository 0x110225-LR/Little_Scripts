import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
from matplotlib import pyplot as plt
from pylab import mpl
import matplotlib.dates as mdates
from mplfinance.original_flavor import candlestick_ohlc
import os

while True:
    i = 1
    a = input("请输入想查询的股票编号：")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.1708.400 QQBrowser/9.5.9635.400'
    }
    
    url = 'http://quotes.money.163.com/trade/lsjysj_'+ a +'.html?year=2019&season=4'
    wb_data = requests.get(url, headers =headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')            # 用.text提取 HTTP体，即 HTML 文档
    table = soup.findAll('table', {'class':'table_bg001'})[0]
    rows = table.findAll('tr')      
    #findAll()方法搜索当前tag的所有tag子节点,并判断是否符合过滤器的条件
    
    csvFile = open(a + '.csv', 'w+', newline = '')   #newline='',解决多一排空行问题
    writer = csv.writer(csvFile)
    
    writer.writerow(['日期', '开盘价', '最高价', '最低价', '收盘价', \
                         '涨跌额', '涨跌幅', '成交量', '成交金额', '振幅', '换手率'])

          
    try:
        for row in rows:
            csvrow = []
            for cell in row.findAll('td'):
                csvrow.append(cell.get_text())
    #Test1
            if csvrow != []:
                writer.writerow(csvrow)
    except:
        print('-----ERROR01:测试未通过，请检查网址信息是否正确！-----')
    finally:
        csvFile.close()
        print('-------SUCCESS!成功------')
    #自适应中文输出格式（字体、坐标显示）
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    mpl.rcParams['axes.unicode_minus'] = False
    
    K_Name = str(soup.find(attrs = {"name":"keywords"})['content'])
    K_Name = K_Name[0:4]
    print ("你查询的股票名是：  " + K_Name)
    filename = a + '.csv'
    with open(filename) as f:
        reader = csv.reader(f)
        header_row = next(reader)
    
        dates, openprices, highprices, lowprices, closeprices = [], [], [], [], []
    
        for row in reader:      
            current_date = datetime.strptime(row[0], '%Y-%m-%d')
            dates.append(current_date)
    
            openprice = float(row[1])
            openprices.append(openprice)
    
            highprice = float(row[2])
            highprices.append(highprice)
    
            lowprice = float(row[3])
            lowprices.append(lowprice)
    
            closeprice = float(row[4])
            closeprices.append(closeprice)
    
    datas = []
    for i in range(len(dates)):
        datas.append([mdates.date2num(dates[i]), float(openprices[i]), float(highprices[i]), \
                     float(lowprices[i]), float(closeprices[i])])        
    ###print(datas)
    ''''----------绘制折线图--------'''
    
    fig = plt.figure(1, dpi =128, figsize =(10,6))            # figure 定义一张图片, figsize决定图片的大小
    plt.plot(dates, openprices, color ='r')
    plt.title(K_Name , fontsize =24)
    plt.xlabel('', fontsize =16)
    plt.ylabel('股价（元）', fontsize =16)
    plt.grid(True)                            #显示网格
    fig.autofmt_xdate()                       #倾斜日期
    #保存
    plt.savefig('D:/折线图.png',dpi=100)
    if os.path.exists(r'D:/折线图.png'):
        print('----折线图.png保存成功 ------')
    else:
        print('---------折线图.png保存失败-----------')
    
    '''--------------绘制K线图-------------'''
    
    fig = plt.figure(2, dpi =128, figsize =(10,6))
    ax2 = plt.subplot(111)
    ax2.set_title(K_Name , fontsize =24)
    ax2.set_xlabel('', fontsize =16)
    ax2.set_ylabel('股价（元）', fontsize =16)
    ax2.grid(True)                            #显示网格
    ax2.xaxis_date()                         #显示为日期
    fig.autofmt_xdate()
    candlestick_ohlc(ax2, datas, width =0.6, colorup ='r', colordown ='g')
    #保存 
    plt.savefig('D:/K线图.png',dpi=100)
    if os.path.exists(r'D:/K线图.png'):
        print('----K线图.png保存成功 ------')
    else:
        print('-------K线图.png保存失败-------')
    
    '''-------合并显示两张图-----------'''
    
    fig = plt.figure(3, dpi=128, figsize =(10,6))
    ax3 = plt.subplot(211)                         #分成2x1，占用第一个，即第一行第一列的子图 
    ax3.xaxis_date()
    ax3.set_title(K_Name , fontsize =14)
    ax3.set_xlabel('', fontsize =12)
    ax3.set_ylabel('股价（元）', fontsize =12)
    #fig.autofmt_xdate()
    ax3.grid(True)                            #显示网格
    ax3.plot(dates, openprices, c ='r')
    
    ax4 = plt.subplot(212)                    #  分成2x1，占用第二个，即第二行     
    ax4.set_xlabel('', fontsize =12)
    ax4.set_ylabel('股价（元）', fontsize =12)
    ax4.grid(True)                            #显示网格
    ax4.xaxis_date()
    candlestick_ohlc(ax4, datas, width=0.6, colorup ='r', colordown ='g')
    #保存   
    plt.savefig('D:/折线和K线图.png', dpi=100)
    if os.path.exists(r'D:/折线和K线图.png'):
        print('----折线和K线.png保存成功 ------')
    else:
        print('----折线和K线.png保存失败------')
    
    plt.show()
