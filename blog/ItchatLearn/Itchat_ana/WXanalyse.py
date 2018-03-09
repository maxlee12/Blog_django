
import itchat
import jieba
import re
import matplotlib.pyplot as plt
from scipy.misc import imread
import pandas as pd
from wordcloud import WordCloud, ImageColorGenerator
import numpy
import os
from os import listdir
from PIL import Image
import math

def write_txt_file(path, txt):
    '''
    写入txt文本
    '''
    with open(path, 'a', encoding='gb18030', newline='') as f:
        f.write(txt)

def read_txt_file(path):
    '''
    读取txt文本
    '''
    with open(path, 'r', encoding='gb18030', newline='') as f:
        return f.read()

# 登录
def login():

    def lc():
        print("Finsh Login!")
    def ec():
        print("exit")

    itchat.auto_login(loginCallback=lc, exitCallback=ec, hotReload=True)
    # 爬取自己好友相关信息， 返回一个json文件
    friends = itchat.get_friends(update=True)[0:]
    return friends;

# 性别比例
def sex_ana(friends):
    # 初始化计数器
    male = female = other = 0
    # friends[0]是自己的信息，所以要从friends[1]开始
    for i in friends[1:]:
        sex = i["Sex"]
        if sex == 1:
            male += 1
        elif sex == 2:
            female += 1
        else:
            other += 1
    # 计算朋友总数
    total = len(friends[1:])
    # 打印出自己的好友性别比例
    print("男性好友： %.2f%%" % (float(male) / total * 100) + "\n" +
          "女性好友： %.2f%%" % (float(female) / total * 100) + "\n" +
          "不明性别好友： %.2f%%" % (float(other) / total * 100))


# 城市分布
def city_ana(friends):
    # 定义一个函数，用来爬取各个变量
    def get_var(var):
        variable = []
        for i in friends:
            value = i[var]
            variable.append(value)
        return variable

    # 调用函数得到各变量，并把数据存到csv文件中，保存到桌面
    NickName = get_var("NickName")
    Sex = get_var('Sex')
    Province = get_var('Province')
    City = get_var('City')
    Signature = get_var('Signature')
    from pandas import DataFrame
    data = {'NickName': NickName, 'Sex': Sex, 'Province': Province,
            'City': City, 'Signature': Signature}
    frame = DataFrame(data)
    frame.to_csv('data.csv', index=True)


# 个性签名
def singauter(friends):

    # 统计签名
    for friend in friends:
        # 对数据进行清洗，将标点符号等对词频统计造成影响的因素剔除
        pattern = re.compile(r'[一-龥]+')
        filterdata = re.findall(pattern, friend['Signature'])
        write_txt_file('signatures.txt', ''.join(filterdata))

    # 读取文件
    content = read_txt_file('signatures.txt')
    segment = jieba.lcut(content)
    words_df = pd.DataFrame({'segment': segment})

    # 读取stopwords
    stopwords = pd.read_csv("stopwords.txt", index_col=False, quoting=3, sep=" ", names=['stopword'], encoding='utf-8')
    words_df = words_df[~words_df.segment.isin(stopwords.stopword)]
    # print(words_df)

    words_stat = words_df.groupby(by=['segment'])['segment'].agg({"计数": numpy.size})
    words_stat = words_stat.reset_index().sort_values(by=["计数"], ascending=False)

    # 设置词云属性
    color_mask = imread('background.jpg')
    font_path = '/Users/lawrence/Library/Fonts/Arial Unicode.ttf'
    wordcloud = WordCloud(font_path=font_path,  # 设置字体可以显示中文
                          background_color="white",  # 背景颜色
                          max_words=100,  # 词云显示的最大词数
                          mask=color_mask,  # 设置背景图片
                          max_font_size=100,  # 字体最大值
                          random_state=42,
                          width=1000, height=860, margin=2,
                          # 设置图片默认的大小,但是如果使用背景图片的话,                                                   # 那么保存的图片大小将会按照其大小保存,margin为词语边缘距离
                          )

    # 生成词云, 可以用generate输入全部文本,也可以我们计算好词频后使用generate_from_frequencies函数
    word_frequence = {x[0]: x[1] for x in words_stat.head(100).values}
    # print(word_frequence)
    word_frequence_dict = {}
    for key in word_frequence:
        word_frequence_dict[key] = word_frequence[key]

    wordcloud.generate_from_frequencies(word_frequence_dict)
    # 从背景图片生成颜色值
    image_colors = ImageColorGenerator(color_mask)
    # 重新上色
    wordcloud.recolor(color_func=image_colors)
    # 保存图片
    wordcloud.to_file('output.png')
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()

# 头像拼图
def friendImg(friends):
    user = 'images'
    if os.path.exists(user) == False:
        os.mkdir(user)
    # 爬取微信好友头像图片，下载保存到本地
    num = 1
    for i in friends:
        img = itchat.get_head_img(userName=i["UserName"])
        fileImage = open(user + "/" + str(num) + ".jpg", 'wb')
        fileImage.write(img)
        fileImage.close()
        num += 1
    pics = listdir(user)

    # 微信好友个数
    numPic = len(pics)
    print(numPic)
    # 微信好友头像缩小后，每个头像的大小
    eachsize = int(math.sqrt(float(640 * 640) / numPic))
    print(eachsize)
    # 每行头像的个数
    numline = int(640 / eachsize)
    toImage = Image.new('RGB', (640, 640))
    print(numline)
    x = 0
    y = 0
    for i in pics:
        # 打开图片
        try:
            img = Image.open(user + "/" + i)
        except IOError:
            print("Error: 没有找到文件或读取文件失败" + i)
        else:
            # 缩小图片
            img = img.resize((eachsize, eachsize), Image.ANTIALIAS)
            # 拼接图片
            toImage.paste(img, (x * eachsize, y * eachsize))
            x += 1
            if x == numline:
                x = 0
                y += 1
        # 保存图片
        toImage.save(user + ".jpg")
        # 并发送到手机
        itchat.send_image(user + ".jpg", 'filehelper')

###
def main():

    friends = login()
    # 性别
    sex_ana(friends)
    # csv信息
    city_ana(friends)
    # 签名图
    singauter(friends)
    #头像
    # friendImg(friends)

if __name__ == '__main__':
    main()
#登录
