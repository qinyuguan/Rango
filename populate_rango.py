import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django

django.setup()
from rango.models import Category, BookDetail
import json

import requests
from lxml import etree


# data class
# To save index info
class ProductIndex:
    title = ""
    url = ""

    def __init__(self, text, url):
        self.title = text
        self.url = url


def download_html():
    print("Trying to fetch data from the internet.")
    print("If you encounter any trouble in this step, you can unzip the downloaded.zip directly.")

    main_page_url = 'https://uk.bookshop.org/books?page='
    base_url = 'https://uk.bookshop.org/'
    all_product_indies = []

    # fetch the whole book list
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

    # save urls of every books
    for index in all_product_indies:
        print('url:\t' + base_url + index.url)
        response = requests.get(base_url + index.url, headers={
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Mobile Safari/537.36'})
        with open(file_folder + index.url.replace('/', '_') + '.html', 'w') as f:
            f.write(response.text)


if __name__ == '__main__':
    print('Starting Rango population script...')
    file_folder = "./downloaded/"
    # if the html folder doesn't exist, the script will download it.
    if not os.path.exists(file_folder):
        print('downloaded folder doesn\'t exist.')
        os.mkdir(file_folder)
        download_html()

    base_url = 'https://uk.bookshop.org/'

    # only add 500 files into our database
    count = 0
    for file in os.listdir(file_folder)[:1000]:
        with open(file_folder + file, 'r') as f:
            try:
                # extract information from html files
                html = etree.HTML(f.read())
                title = html.xpath("//*[@id='content']/div[2]/div[2]/div[1]/h1")[0].text
                author = html.xpath("//*[@itemprop='author']//*[@itemprop='name']")[0].text.strip()
                img = html.xpath("//*[@id='content']/div[2]/div[2]/div[2]/div/a/img")[0].attrib['src'].split('?')[0]
                price = html.xpath("//div[@itemprop='offers']/b")[0].text
                publisher = html.xpath("//div[@itemprop=\"publisher\"]")[0].text
                publish_date = html.xpath("//div[@itemprop=\"datePublished\"]")[0].text
                language = html.xpath("//div[@itemprop=\"inLanguage\"]")[0].text
                book_type = html.xpath("//div[@itemprop=\"bookFormat\"]")[0].text
                ISBN = html.xpath("//div[@itemprop=\"isbn\"]")[0].text

                categories = html.xpath("//*[@id='taxon-crumbs']//a")
                categories = ";".join(list(map(lambda url: url.text, categories)))

                # save the raw description part's html
                descriptions = html.xpath("//div[@itemprop=\"description\"]")
                if len(descriptions) != 0:
                    descriptions[0].tail = None
                    desc = etree.tostring(descriptions[0], pretty_print=True, method='html', with_tail=False).decode(
                        'utf-8').split('<div class="mb-8">')[0]
                else:
                    desc = ""

                # save data to database
                book = BookDetail.objects.get_or_create(title=title, author=author, img=img, publisher=publisher,
                                                        publish_date=publish_date, price=price, language=language,
                                                        book_type=book_type, ISBN=ISBN, desc=desc, category=categories)[
                    0]
                count += 1
                book.save()
            except Exception as exc:
                print("error occurred during processing:  ", file)
                print(exc)

    # build the category table
    category_set = set()
    category_count = 0
    for book in BookDetail.objects.order_by('title'):
        for cate in book.category.split(';'):
            category_set.add(cate)
    for cate in category_set:
        category_count += 1
        try:
            category = Category.objects.get_or_create(name=cate)[0]
            category.save()
        except:
            pass

    # match catrgories and books
    for book in BookDetail.objects.order_by('title'):
        for cate in book.category.split(';'):
            try:
                category = Category.objects.filter(name=cate)[0]
                book.categories.add(category)
                book.save()
            except:
                pass

    print('Added ' + str(count) + ' books in ' + str(category_count) + ' categories to database Successfully')
