import requests
import re
from html.parser import HTMLParser
from urllib.parse import urlparse
import os, json
import tldextract

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

class ContentApi:

    def __init__(self, htmlstrip):
        self.htmlstrip = htmlstrip
        
    def get_article_page(self, param=""):
        api = 'http://api.cliqueinc.com'
        product_slug = '/content/posts'
        url = api + product_slug + param
        return requests.get(url)

    def go_deep_article(self, key):
        url = "/" + key
        return self.get_article_page(url)

    def get_deep_data(self, r):
        page_data = self.get_page_data(r)
        return page_data[0] if page_data is not None else None

    def get_page_data(self, response):
        data = json.loads(response.text)
        return data.get('docs')

    def check_response_code(self, response):
        code = response.status_code
        return True if code == requests.codes.ok else False

    def flatten_strings(self, text):
        for n, t in enumerate(text):
            if type(t) is not str:
                if type(t) is list:
                    t_len = len(t)
                    str_count = 0
                    for i in t:
                        if type(i) is str:
                            str_count += 1
                    if str_count == t_len:          
                        text[n] = " ".join(t)
        text = [x for x in text if x is not None]
        text = " ".join(text)
        return text

    def clean_text(self, input):
        input = input.strip()  # remove leading and trailing whitespace
        input = re.sub('\n+', " ", input) # substitute new line character with one space
        input = re.sub('\r+', " ", input) # substitute new line character with one space
        input = re.sub('\t+', " ", input)  # substitute tabs with one space
        input = re.sub(' +', " ", input)  # substitute multiple spaces with one space
        input = bytes(input, "UTF-8")  # encode to bytes
        input = input.decode("ascii", "ignore")  # decode to ascii
        input = input.lower()  # make lowercase for matching
        return input

    def strip_tags(self, html):
        s = self.htmlstrip()
        s.feed(html)
        return s.get_data()

    def cleaner(self, text):
        text = self.flatten_strings(text)
        text = self.strip_tags(text)
        text = self.clean_text(text)
        return text
        
    def get_article_data(self, article):
        dic = {}
        try:
            dic['aid'] = article.get('id')
            dic['key'] = article.get('key')
            dic['slug'] = article.get('slug')
            dic['site_id'] = article.get('site_id')
            dic['section'] = article.get('section')['name']
            dic['tag_slugs'] = article.get('tag_slugs')
            dic['title'] = article.get('title')
            dic['headline'] = article.get('headline')
            dic['publish_start'] = article.get('publish_start')
            return dic
        except:
            dic['aid'] = 'unknown'
            dic['key'] = 'unknown'
            dic['slug'] = 'unknown'
            dic['site_id'] = 'unknown'
            dic['section'] = 'unknown'
            dic['tag_slugs'] = 'unknown'
            dic['title'] = 'unknown'
            dic['headline'] = 'unknown'
            dic['publish_start'] = 'unknown'
            return dic

    def get_widget_data(self, article_data):
        
        corpus_dump = []
        
        # grab first level text
    #     title = article_data.get('title')
    #     titles = article_data.get('title_variations')
    #     headlines = article_data.get('headline_variations')
    #     meta_description = article_data.get('meta_description')
    #     tweets = article_data.get('tweet_text_variations')
    #     is_sponsored = article_data.get('is_sponsored')
    #     general_tags = article_data.get('general_tags')
    #     brand_tags = article_data.get('brand_tags')
    #     celebrity_tags = article_data.get('celebrity_tags')
    #     brand_tags = article_data.get('brand_tags')
        
    #     corpus_dump.append(title)
    #     corpus_dump.append(titles)
    #     corpus_dump.append(meta_description)
    #     corpus_dump.append(headlines)
    #     corpus_dump.append(tweets)
        
        #grab widget data
        widgets = article_data.get('widgets')
        w_len = 0
        t_len = 0
        p_len = 0
        i_len = 0
        cgd_len = 0
        g_len = 0
        if widgets:
            w_len = len(widgets)
            for w in widgets:
                if w['type'] == 'text':
                    fields = w.get('fields')
                    text_body = fields.get('body')
                    if text_body: 
                        corpus_dump.append(text_body)
                        t_len += 1
                elif w['type'] == 'product':
                    p_len += 1
                    product_fields = w.get('fields')
                    product_description = product_fields.get('description')
                    corpus_dump.append(product_description)
                elif w['type'] == 'image':
                    i_len += 1
    #                 image_caption = w['fields']['caption']
    #                 image_alt = w['fields']['alt_tag']
                    image_fields = w.get('fields')
                    image_description = image_fields.get('description')
    #                 corpus_dump.append(image_caption)
    #                 corpus_dump.append(image_alt)
                    corpus_dump.append(image_description)
                    #image_url = w['images']['url']
                elif w['type'] == 'gallery':
                    if w['template'] == "CGD-VSM":
                        cgd_len += 1
                    elif w['template'] == "default":
                        g_len += 1
        dic = {}
        dic['text']= corpus_dump
        dic['w_len'] = w_len
        dic['t_len'] = t_len
        dic['p_len'] = p_len
        dic['i_len'] = i_len
        dic['cgd_len'] = cgd_len
        dic['g_len'] = g_len
            
        return dic
    
    def checkurl(self, url):
        url = url.strip()
        www_pattern = re.compile("^(www\.)", flags=re.I)
        url = 'http://' + url if www_pattern.search(url) else url

        url_components = urlparse(url)
        url_parsed = tldextract.extract(url)

        if url_components.path == '': raise ValueError('Could not find article slug in {}'.format(url))
        
        subdomain = "www"

        if url_parsed.domain.lower() == 'whowhatwear':
            url_domain = url_parsed.domain 
        else:
            raise ValueError('Only accepting WhoWhatWear articles \n Could not find www.whowhatwear.com in {}'.format(url))
        
        url_path = url_components.path
        fs_pattern = re.compile("/$",flags=re.I)

        url_path = url_path[:-1] if fs_pattern.search(url_path) else url_path

        url = "{subdomain}.{domain}.com{path}".format(subdomain=subdomain,domain=url_domain, path=url_path)

        return url

    def get_article_text(self, article_url):
        try:
            article_url = self.checkurl(article_url)
            deep = self.go_deep_article(article_url)
            data = self.get_deep_data(deep)
            wgts = self.get_widget_data(data)
            txt = self.cleaner(wgts['text'])
            return txt
        except Exception as e: 
            print(e)