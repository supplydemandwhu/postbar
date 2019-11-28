import scrapy
import os.path

class YstSpider(scrapy.Spider):
    name = "postbar"

    # start_urls = [
    #     "http://tieba.baidu.com/p/6172123300",
    # ]

    path = 'result\\'
    img = False
    onefile = False

    def start_requests(self):
        url = getattr(self, 'url', 'http://tieba.baidu.com/p/6172123300')
        self.path = getattr(self, 'path', 'result\\')
        self.img = getattr(self, 'img', False)
        if self.img is not False:
            self.img = True

        self.onefile = getattr(self, 'onefile', False)
        if self.onefile is not False:
            self.onefile = True
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        page = response.url.split("=")[-1]   #当前页号
        if page == response.url:
            page = 1
        else:
            page = int(page)

        if not os.path.exists(self.path):
            os.makedirs(self.path)
        file = self.path + 'page %2d.html' % page
        opt = 'wb'
        if self.onefile:
            file = self.path + 'page.html'
            opt = 'ab+'
        with open(file, opt) as f:
            for div in response.css('div.d_post_content'):
                f.write('<div>'.encode('utf-8'))

                # for img_url in div.css('img.BDE_Image::attr(src)').getall():
                #     yield scrapy.Request(img_url, self.parse_img)
                #     f.write( ('<img src="img\\%s">' % img_url.split('/')[-1] ).encode('utf-8'))
                #
                # for line in div.css('::text').getall():
                #     f.write((line + '<br>\n').encode('utf-8'))

                for item in div.css('img, ::text'):
                    if item.css('img').get() is not None:
                        if self.img:
                            img_url = item.css('img::attr(src)').get()
                            yield scrapy.Request(img_url, self.parse_img)
                            img_name = img_url.split('/')[-1].replace('?','_')
                            f.write(('<img src="img\\%s"> <br>\n' % img_name).encode('utf-8'))
                        else:
                            line = item.get()
                            f.write((line + ' <br>\n').encode('utf-8'))

                    # elif item.css('::text').get() is not None:
                    else:
                        line = item.get()
                        f.write((line + ' <br>\n').encode('utf-8'))
                        pass

                f.write('</div>'.encode('utf-8'))

                f.write('<div><br><br>==================================================================<br><br></div>'.encode('utf-8'))

        num = int(response.xpath('//*[@id="thread_theme_5"]/div[1]/ul/li[2]/span[2]/text()').get())  #总页数
        page += 1
        if page <= num:
            next_page = response.url.split('?')[0] + '?pn=' + str(page)
            yield response.follow(next_page, self.parse)

    def parse_img(self, response):
        img_path = self.path + 'img\\'

        if not os.path.exists(img_path):
            os.makedirs(img_path)

        img = response.url.split('/')[-1].replace('?','_')
        with open(img_path + img, 'wb') as f:
            f.write(response.body)