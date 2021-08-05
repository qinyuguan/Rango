import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django

django.setup()
from rango.models import Category, Page, BookDetail
import json

import requests
from lxml import etree


class ProductIndex:
    title = ""
    url = ""

    def __init__(self, text, url):
        self.title = text
        self.url = url


def download_html():
    main_page_url = 'https://uk.bookshop.org/books?page='
    base_url = 'https://uk.bookshop.org/'
    all_product_indies = []
    all_product_info = []

    for i in range(1, 401):
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
        with open("./downloaded/" + index.url.replace('/', '_') + '.html', 'w') as f:
            f.write(response.text)


if __name__ == '__main__':
    print('Starting Rango population script...')
    # download_html()
    # populate()
    base_url = 'https://uk.bookshop.org/'
    for file in os.listdir(r"./downloaded"):
        with open("./downloaded/" + file, 'r') as f:
            try:
                html = etree.HTML(f.read())
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

                descriptions = html.xpath("//div[@itemprop=\"description\"]")
                if len(descriptions) != 0:
                    descriptions[0].tail = None
                    desc = etree.tostring(descriptions[0], pretty_print=True, method='html', with_tail=False).decode(
                        'utf-8').split('<div class="mb-8">')[0]
                else:
                    desc = ""
                book = BookDetail.objects.get_or_create(title=title, author=author, img=img, publisher=publisher,
                                                        publish_date=publish_date, price=price, language=language,
                                                        book_type=book_type, ISBN=ISBN, desc=desc, category=categories)[
                    0]
                book.save()
            except Exception as exc:
                print("error occured when fetch:  ", file)
                print(exc)

    # build the category table
    category_set = set()
    for book in BookDetail.objects.order_by('title'):
        for cate in book.category.split(';'):
            category_set.add(cate)
    for cate in category_set:
        try:
            category = Category.objects.get_or_create(name=cate)[0]
            category.save()
        except:
            pass

    # match catrgories
    for book in BookDetail.objects.order_by('title'):
        for cate in book.category.split(';'):
            try:
                category = Category.objects.filter(name=cate)[0]
                book.categories.add(category)
                book.save()
            except:
                pass
