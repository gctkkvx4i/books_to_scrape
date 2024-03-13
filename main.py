import requests
from parsel import Selector
import json

def save_to_html(response, filename='books'):
    with open(f'{filename}.html', 'w', encoding='utf-8') as file:
        file.write(response.text)

def parse(selector):
    data = []
    position = 1

    while True:
        books = selector.css('.col-xs-6.col-sm-4.col-md-3.col-lg-3')

        for book in books:
            image = book.css('a img::attr(src)').get()
            rating = ''
            if book.css('.star-rating.One::text').get():
                rating = '1/5'
            elif book.css('.star-rating.Two::text').get():
                rating = '2/5'
            elif book.css('.star-rating.Three::text').get():
                rating = '3/5'
            elif book.css('.star-rating.Four::text').get():
                rating = '4/5'
            elif book.css('.star-rating.Five::text').get():
                rating = '5/5'
            name_of_book = book.css('h3 a::attr(title)').get()
            link = 'https://books.toscrape.com/' + book.css('h3 a::attr(href)').get()
            price = book.css('.price_color::text').get()
            stock = ''
            if book.css('.instock.availability::text').get():
                stock = '✔ In stock'
            elif book.css('.instock.unavailable::text').get():
                stock = 'Unavailable'

            data.append({
                'position': position,
                'image': image,
                'title': name_of_book,
                'rating': rating,
                'price': '£' + price[2:],
                'stock': stock,
                'link': link
            })
            position += 1

        next_page = selector.css('li.next a::attr(href)').get()
        print('Next page:', next_page)
        if next_page:
            response = requests.get(url='https://books.toscrape.com/' + next_page)
            selector = Selector(response.text)
        else:
            break

    return data

def main():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 '
                      'Safari/537.36'
    }

    url = 'https://books.toscrape.com/'
    response = requests.get(url=url, headers=headers)
    save_to_html(response=response)

    selector = Selector(response.text)
    books_to_scrape_data = parse(selector)
    print(json.dumps(books_to_scrape_data, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
