# TDI-Project
This dataset consists of two parts: The infomation over 1 million books/ebooks/multimedia items scraped from a Chinese e-commerce website ('item_info_books.csv') and the matching reader comments scraped from a social-network website ('books_db.csv') from Dec. 2018 to February 2019. Here is a detailed description about the first half of the datasets. More book information is on the way...

## 'item_info_books.csv'
'skuId' is the primary key. Each skuId corresponds to one item for sale on the website. Note that some columns only apply for ebooks or DVD/CDs.
### Columns: 
 - **'BookName'**: Name of the book (in Chinese utf-8), not cleaned
 - **'Author'**: Name of the author/ authors, not cleaned
 - **'店铺'**: Name of the e-store
 - **'ISBN'**: International Standard Book Number (10 or 13 digits starting from 978)
 - **'商品编码'**:
 - **'包装'**: Hardcover, softcover,
 - **'出版时间'**: Publication date
 - **'Cate0','Cate1','Cate2'**: Three-level categorization identification number on the website
 - **'CateN0','CateN1','CateN2'**: Three-level categorization identification name on the website
 - **'skuId'**: Primary key, item ID for sale
 - **'skuId_father'**: The item ID that sends ad links to the current item
 - **'venderId'**: Id of the vendor
 - **'shopId'**: Id of the e-store
 - **'isEbook'**: categorical, whether a book is a paper book or ebook
 - **'ScrapeTime'**: Time when the data is scraped
 - **'is7ToReturn'**: categorical, whether a book can be returned within 7 day's purchase
 - **'averageScore'**: Average rating from the buyers (scale 0-5)
 - **'commentCount'**: Number of comments from the buyers
 - **'goodCount','generalCount','poorCount','afterCount','showCount'**:
                     Number of goodratings/median ratings/poor ratings/ratings after use/displayed ratings
 - **'版次'**: Book version
 - **'开本'**: Size of the book (8, 16 etc.)
 - **'用纸'**: Paper quality
 - **'页数'**: Number of book pages
 - **'套装数量'**: Number of books in a set
 - **'字数'**: Number of characters in the book
 - **'SoldOversea-7'**: categorical, can be sold oversea
 - **'YushouStepType-0'**: categorical, pre-sale or not
 - **'品牌'**: Brand
 - **'外文名称'**: English name of the book
 - **'正文语种'**: Language of the text
 - **'IsNewGoods'**: categorical, new or used
 - **'商品编号'**: Item id in the shop
 - **'介质'**: Material
 - **'碟数'**: Number of discs
 - **'ISRC'**: International Standard Recording Code
 - **'出版社'**: Publisher
 - **'配音语言'**: Subtitle language
 - **'字幕语言'**: Subtitle language
 - **'音频格式'**: Audio format
 - **'地区'**: Area of origin
 - **'画面色彩'**: Color bits of the movie
 - **'文件大小'**: Size of the ebook file
 - **'文件格式'**: Format of the ebook file
 - **'商品名称'**: Name of the item ()
 - **'商品毛重'**: Net weight of the item
 - **'商品产地'**: Area of Origin of the item
 
 ## 'book_db.csv'
 'ISBN' is the primary key.
 ### Columns:
 - **'Error'**: Categorical, if ISBN is not registered
 - **'alt'**: URL of the book
 - **'author', 'author_intro'**: Author names and brief introduction of the book
 - **'translator'**: Translator
 - **'binding'**: Hardcover or softcover
 - **'catalog'**: Book catalog in string
 - **'ebook_price'**: Price of the ebook
 - **'ebook_url'**: URL of the ebook
 - **'id'**: Item Id on the website
 - **'imageurl'**: URL of the book cover
 - **'isbn10','isbn13'**: International standard book number (10-digits or 13-digits)
 - **'maxrating','minrating',avgrating'**: Maximum rating, minimum rating, average rating (set to 10 and 0 if no raters)
 - **'numRaters'**: Number of raters
 - **'origin_title'**: Book title in its origin language
 - **'pages'**: Number of pages of the book
 - **'price'**: Claimed price of the book
 - **'pubdate'**: Publication date
 - **'publisher'**: Publisher
 - **'series'**: A dictionary of the father series
 - **'title'**: title of the book
 - **'subtitle'**: Subtitle of the book
 - **'summary'**: Brief summary of the book
 - **'tag(x)'**: Book tags assigned by readers
 - **'tagcount(x)'**: Number of readers that acknowleged this book tag
 
