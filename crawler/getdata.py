import requests
import time
from bs4 import BeautifulSoup as bs

def wirtecsv(strs):
    with open('data.csv', 'a+') as ff:
        ff.write(strs)

def getinfo(single_soup):

    # 整个页面的data Elements
    total_div = single_soup.find_all('div',class_="content__list--item--main")
    for house in total_div:
        try:
            #房屋名称
            house_title = house.find('a',class_="twoline").text.split(" ")[10].replace('整租·','')
            #房屋户型
            house_type = house.find('a',class_="twoline").text.split(" ")[11]
            #房屋格局（复式、跃层等等）
            house_aspect = house.find('a',class_="twoline").text.split(" ")[12]
            #房屋行政区
            house_district = house.find_all('a',target="_blank")[1].text
            #房屋面积
            house_area = house.find('p',class_="content__list--item--des").text.split("/")[1].replace(" ","").replace('\n', '').replace('㎡','')
            #房屋朝向（东南西北）
            house_aspect_2 = house.find('p',class_="content__list--item--des").text.split("/")[2].replace(" ","").replace('\n', '')
            #房屋楼层
            house_floor = house.find('p',class_="content__list--item--des").text.split("/")[4].replace(" ","").replace('\n', '')
            #价格Price
            house_price = house.find('span',class_="content__list--item-price").text.replace(' 元/月','')
            # 汇总
            list1 = [house_title, house_type, house_aspect, house_district,
                     house_area, house_aspect_2,house_floor,house_price]

            print(list1)
            strs=f"{house_title}@@{house_type}@@{house_aspect}@@{house_district}@@{house_area}@@{house_aspect_2}@@{house_floor}@@{house_price}\n"
            strs=strs.replace(",",";").replace("@@",",")
            wirtecsv(strs)
            #house_info.append(list1)
        except (IndexError,AttributeError,AttributeError,AttributeError,AttributeError):
            pass
    #return house_info

if __name__ == '__main__':
    house_info = []
    areas=["luohuqu","futianqu","nanshanqu","yantianqu","baoanqu","longgangqu","longhuaqu","guangmingqu","pingshanqu","dapengxinqu"]
    #nums=[5389,8741,8474,709,6201,9732,5840,671,472,139]
    pagenums=[100,100,100,24,100,100,100,23,16,5]
    for i in range(10):
        for j in range(pagenums[i]):
            single_url = f"https://sz.zu.ke.com/zufang/{areas[i]}/pg{j}/#contentList"
            responce = requests.get(single_url)
            soup = bs(responce.text, 'html.parser')
            getinfo(soup)