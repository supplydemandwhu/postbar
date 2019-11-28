## 百度贴吧爬虫

### 简介

不遵守robots.txt，爬取百度贴吧指定主题帖某一页之后的所有页面

### 制作方法

##### 创建爬虫

```bash
scrapy startproject projectname
```

spiders\spidername_spider.py  爬虫

item.py -o 输出的数据

middlewares.py 

piplelines.py 

setting.py 配置（如：是否遵守robots.txt，是否使用cookies等）

middlewares.py 创建项目时自动生成的中间件

random_delay_middleware.py 随机延迟（中间件）

useragentmiddleware.py 不断改变用户代理（中间件）

##### 尝试选择器

```bash
scrapy shell "URL"
```

```python
#选择器 xpath
response.xpath('//title') #返回选择器
response.xpath('//title').extract() #返回选择器对应的文本
response.xpath('//title/text()').extract() #返回选择器内的文本
response.xpath('//title/text()').re('(\w+):') #对选择器内的文本进行正则表达式匹配
response.xpath('//ul/li/a/@href').extract() #链接url html标记的附带内容

#选择器 css
response.css('div.classname a') #class="classname"的div 中的a
response.css('div.classname a::text') #class="classname"的div 中的a之中的文本
response.css('img, ::text') #img或文本

```



##### 爬取

scrapy crawl spidername <-o <output.json|output.jl>> <-a key=val>

jl为若干行json内容，便于追加。

### 使用方法

scrapy crawl postbar <-a url=http://tieba.baidu.com/p/6172123300> <-a path=result\\> <-a onefile=false> <-a img=false>

#### url

指定爬取的起始页面，或是爬取http://tieba.baidu.com/p/6172123300

#### path

指定保存的相对位置，或是保存到result文件夹

#### onefile

是否输出到同一个html文件，还是一页一个文件

#### img

是否确实下载图片（违反百度robots.txt协议），还是只保存图片的链接



### 主要参考资料

[怎么用Python写爬虫抓取网页数据](https://www.cnblogs.com/aiandbigdata/p/10087000.html)

[Scrapy 1.8 documentation （英文）](https://docs.scrapy.org/en/latest/index.html)

[Scrapy 0.25 文档 （中文）](https://scrapy-chs.readthedocs.io/zh_CN/latest/index.html)

