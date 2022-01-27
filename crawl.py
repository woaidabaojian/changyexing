import reqfun,random
import lxml,time
import sys
from lxml.html import tostring,html5parser
def getText(href,titleXpath,contentXpath,et=0):
    print("downing ",href)
    response=reqfun.myget(href)
    if response == None:
        if et<3:
            time.sleep(2)
            return getText(href, titleXpath, contentXpath,et+1)
        else:
            print('fail to downing {href} three times, response is None'.format(href=href))
            # sys.exit()
            return None,None
    response.encoding='utf8'
    # print(response.text)
    try:
        lt=lxml.etree.HTML(adjust(response.text))
        title=adjust(lt.xpath(titleXpath)[0])
        content=''.join(lt.xpath(contentXpath))
        # print([content])
        # return
        # content=lt.xpath(contentXpath)[0].xpath('string(.)')
    except Exception as e:
        print(e)
        if et<3:
            time.sleep(2)
            return getText(href, titleXpath, contentXpath,et+1)
        else:
            print('fail to downing {href} three times and exit the program'.format(href=href))
            sys.exit()
    content=adjust(content)
    return (None,content)
    # return (title,content)
    
def save(title,text,number,filePath):
    if title == None:
        if text is not None:
            with open(filePath,'a',encoding='utf8')as f:
                f.write(text)
            return
        else:
            return
    try:
        with open(filePath,'a',encoding='utf8')as f:
            f.write('\n'+title+'\n')
            f.write(text)
        print('save sucess'+str(number)+'  '+title)
    except Exception as e:
        print('error whiling saving',e,title,number)

def adjust(t):
    t=t.replace(r'<br>','\n\t')
    t=t.replace('\xa0\xa0\xa0\xa0','\t')
    t=t.replace('\r\n\r\n','\r\n')
    t=t.replace('\u3000','\r\n\t')
    # t=t.replace('\xa0','\n\n')
    return t

def download(source,index,hxp,txp,cxp,fp):
    a=reqfun.myget(source)
    a.encoding='utf8'
    b=lxml.etree.HTML(a.text)
    c=b.xpath(hxp)
    cc=[index+i.attrib['href'] for i in c]
    # print(cc)
    # print(len(cc),c[0].text,c[-1].text)
    num=0
    while num<len(cc):
        raw_url = cc[num][:-5]
        for i in range(1,4):
            if i == 1:
                save(*getText(raw_url+'_{}.html'.format(i),txp,cxp),num,fp)
            else:
                title,content = getText(raw_url+'_{}.html'.format(i),txp,cxp)
                if content is not None:
                    save(None,content,num,fp)
                else:
                    save(title,content,num,fp)

        num+=1
        time.sleep(random.randint(1,2))

for i in range(35,41):
    source=r'https://m.laidudu.com/book/60649/index_{}.html'.format(i)
    index=r'https://m.laidudu.com/'
    source_xpath = r'//div[@class="book_last"]/dl[2]/dd/a'
    title_xpath = r'//*[@id="chaptercontent"]/text()[1]'
    content_xpath = r'//*[@id="chaptercontent"]/text()'
    download(source,index,source_xpath,title_xpath,content_xpath,r'./crawl.txt')
# download(source,index,r'/html/body/div[2]/div[3]/dl/dd/a',r'/html/body/div[2]/div/div[1]/h1',r'//*[@id="XueLRw"]',r'D:\python\myCode\spider\星光捧入他掌心.txt')