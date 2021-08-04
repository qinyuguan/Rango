import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django

django.setup()
from rango.models import Category, Page, BookDetail
import json

import requests
from lxml import etree


def populate():
    python_pages = [
        {'title': 'Official Python Tutorial',
         'url': 'http://docs.python.org/3/tutorial/',
         'views': 999},
        {'title': 'How to Think like a Computer Scientist',
         'url': 'http://www.greenteapress.com/thinkpython/',
         'views': 555},
        {'title': 'Learn Python in 10 Minutes',
         'url': 'http://www.korokithakis.net/tutorials/python/',
         'views': 888}]

    django_pages = [
        {'title': 'Official Django Tutorial',
         'url': 'https://docs.djangoproject.com/en/2.1/intro/tutorial01/',
         'views': 100},
        {'title': 'Django Rocks',
         'url': 'http://www.djangorocks.com/',
         'views': 100},
        {'title': 'How to Tango with Django',
         'url': 'http://www.tangowithdjango.com/',
         'views': 777}]

    other_pages = [
        {'title': 'Bottle',
         'url': 'http://bottlepy.org/docs/dev/',
         'views': 100},
        {'title': 'Flask',
         'url': 'http://flask.pocoo.org',
         'views': 666}]

    cats = {'Python': {'pages': python_pages},
            'Django': {'pages': django_pages},
            'Other Frameworks': {'pages': other_pages}}

    for cat, cat_data in cats.items():
        c = add_cat(cat)
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'], p['views'])
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')


def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title, views=views)[0]
    p.url = url
    p.views = views
    p.save()
    return p


def add_cat(name):
    views_num = 0
    lilkes_num = 0
    if name.lower() == 'Python'.lower():
        views_num = 128
        likes_num = 64
    elif name.lower() == 'Django'.lower():
        views_num = 64
        likes_num = 32
    else:
        views_num = 32
        likes_num = 16
    c = Category.objects.get_or_create(name=name, views=views_num, likes=likes_num)[0]
    c.save()
    return c


class ProductIndex:
    title = ""
    url = ""

    def __init__(self, text, url):
        self.title = text
        self.url = url


if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()
    # b = BookDetail.objects.get()
    main_page_url = 'https://uk.bookshop.org/books?page='
    base_url = 'https://uk.bookshop.org/'
    all_product_indies = []
    all_product_info = []

    for i in range(1, 101):
        list_url = main_page_url + str(i)
        print(list_url)
        response = requests.get(list_url, headers={
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Mobile Safari/537.36'})
        html = etree.HTML(response.text)
        books = html.xpath("//h2[@class='font-serif-bold lg:pt-4 leading-tight']/a")
        products = list(map(lambda url: ProductIndex(url.text, url.attrib['href']), books))
        all_product_indies += products

    all_product_indies = list(set(all_product_indies))
    for index in all_product_indies:
        print('url:\t' + base_url + index.url)
        response = requests.get(base_url + index.url, headers={
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Mobile Safari/537.36'})
        html = etree.HTML(response.text)
        try:
            title = html.xpath("//*[@id='content']/div[2]/div[2]/div[1]/h1")[0].text
            author = html.xpath("//*[@itemprop='author']//*[@itemprop='name']")[0].text
            img = html.xpath("//*[@id='content']/div[2]/div[2]/div[2]/div/a/img")[0].attrib['src'].split('?')[0]
            price = html.xpath("//div[@itemprop='offers']/b")[0].text
            publisher = html.xpath("//div[@itemprop=\"publisher\"]")[0].text
            publish_date = html.xpath("//div[@itemprop=\"datePublished\"]")[0].text
            language = html.xpath("//div[@itemprop=\"inLanguage\"]")[0].text
            book_type = html.xpath("//div[@itemprop=\"bookFormat\"]")[0].text
            ISBN = html.xpath("//div[@itemprop=\"isbn\"]")[0].text

            # TODO:- categories and comments
            categories = html.xpath("//*[@id='taxon-crumbs']//a")
            categories = ";".join(list(map(lambda url: url.text, categories)))

            # descriptions = html.xpath("//div[@itemprop=\"description\"]/p/*")
            # desc = list(filter(lambda x: x != None, map(lambda x: x.text, descriptions)))

            descriptions = html.xpath("//div[@itemprop=\"description\"]/p")
            if len(descriptions) != 0:
                desc = etree.tostring(descriptions[0], pretty_print=True, method='html').decode('utf-8')
            else:
                desc = ""
            book = BookDetail.objects.get_or_create(title=title, author=author, img=img, publisher=publisher,
                                                    publish_date=publish_date, price=price, language=language,
                                                    book_type=book_type, ISBN=ISBN, desc=desc)[0]
            book.save()
        except:
            print("error occured when fetch:  ", base_url + index.url)
