import requests
import lxml.html
import csv
import multiprocessing as mp
#导入所需的库，部分可能需要自己手动安装库

url1 = "https://etherscan.io/contractsVerified/{}" 
#url1是一个含有合约地址的网页，括号中填入数字，表示页码，默认情况下，每一页含有25个合约地址
url2 = "https://etherscan.io/address/{}#code"
#url2是一个含有代码的网页，括号中填入具体的一个合约地址，可以从这个网页中获取爬取的代码

path = 'D:/etherscan/{}'  #存储文件的父目录

headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
        }
#模拟浏览器打开页面

#getNameList函数返回一页中25个合约地址的列表，具体效果见说明文档 说明1
def getNameList(url1):
    html1 = requests.get(url1,headers = headers).content  #得到url1的html
    selector = lxml.html.document_fromstring(html1)
    name_list = selector.xpath('//tbody/tr/td/a/text()')  #拿到合约地址名字的列表，列表长度为25（一页默认的合约个数）
    return name_list

#getEveryCode函数返回一个列表，该列表中只含一个对应合约代码的字符串，具体见说明文档中 说明2
def getEveryCode(url2):
    r2 = requests.get(url2,headers = headers).content
    selector = lxml.html.document_fromstring(r2)
    code = selector.xpath('//div[@id="dividcode"]/div[@class="mb-4"]/pre[@class="js-sourcecopyarea editor"]/text()')
    return code


#以上是爬虫的代码，接下来的是将爬取的内容存成txt文件的代码，不是必须的，可以根据自己想要的格式来存储


#writeFile函数是将合约代码写入文件的函数，文件名为合约的地址值，文件内容为对应的合约代码;
#dict为一个字典，key是合约的地址名，value是对应的代码
def writeFile(dict):
    if(len(dict) != 0):
        for eachName in dict:
            temp_path = path.format(eachName)
            with open(temp_path,"w+",encoding='utf-8') as f:
                f.write(dict[eachName])
                f.close()
    else:
        print("this dict is empty")
        

#测试：用第一页来进行测试
page = 1
test_url1 = url1.format(page)

test_nameList = getNameList(test_url1)

test_dict = {}
for eachName in test_nameList:
    test_url2 = url2.format(eachName)
    codeList = getEveryCode(test_url2)
    if(len(codeList) == 0):
        continue
    else:
        test_dict[eachName] = codeList[0]

writeFile(test_dict)

#测试结果见说明文档中 说明3
        

