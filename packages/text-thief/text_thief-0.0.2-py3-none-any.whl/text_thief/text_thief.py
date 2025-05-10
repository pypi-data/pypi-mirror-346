import re

import concurrent.futures as fu

from concurrent.futures import ThreadPoolExecutor, Future

from bs4 import BeautifulSoup

from link_thief.link_thief import LinkType, Url, _get_page, crawl_website, filter_by_type

CHARS_TO_REMOVE="\\`*_{}[]()>#+-.!$" 

class TextProcced:
    """
    Class wich will contains all text transformations and conversions
    """
    all_words = list()
    unique_words = set()
    tags = dict()

    def __init__(self, _all_words, _unique_words, _tags):
        self.all_words = _all_words
        self.unique_words = _unique_words
        self.tags = _tags


def get_only_unique_words(text: str) -> set[str]:
    """
    Will return only unique words in a list
    ...
    Attributes
    __________
    text: str
        A raw text without HTML or other markup
    
    Returns
    _______
        A set of unique words
    """
    all_words = get_all_words(text)
    words_only_uniques = set(all_words)
    return words_only_uniques

def get_all_words(text: str) -> list[str]:
    """
    Procced the raw text and return a list of the all founded words
    ...
    Attributes
    __________
    text: str
        A row text to procced
    
    Returns
    _______
        A list of words
    """
    return re.sub("[^\w]", " ",  text).split()

def get_words_as_a_tags(text: str) -> dict[str,int]:
    """
    Create a dict with words as an keys and number of occurence as a values
    ...
    Attributes
    __________
    text: str
        A row text to procced
    
    Returns
    _______
        A dict with words as an keys and number of occurence as a values
    """
    tags = {}
    all_words = get_all_words(text)
    unique_words = get_only_unique_words(text)
    for word in all_words:
        if word in unique_words:
            if tags.get(word):
                tags.update({word: tags[word] + 1})
            else:
                tags.update({word: 1})
    return tags

def procced_text(text: str) -> TextProcced:
    """
    Will perform all known operations and conversions on text to return special object TextProcced
    ...
    Attributes
    __________
    text: str
        A row text to procced
    
    Returns
    _______
    A TextProcced object
    """
    all_words = get_all_words(text)
    unique_words = get_only_unique_words(text)
    tags = get_words_as_a_tags(text)
    
    return TextProcced(all_words, unique_words, tags)

def get_page_text(url: str | Url, css_selector: str = 'body') -> str:
    """
    Get the text content of the target element on the page
    ...
    Attributes
    __________
    url: str | Url
        An webpage address to scrape links from
    css_selector: str
        An css selector to be used to find target part of page, default 'body'
    
    Returns
    _______
        A raw text of page
    """
    text = ""
    status_code, page = _get_page(url)
    if status_code == 200:
        soup = BeautifulSoup(page, 'lxml')
        page_part_soup = soup.select(css_selector) 
        for part in page_part_soup:
            text += part.text

    return text

def get_page_text_list(urls: list[str] | list[Url], css_selector: str = 'body') ->  str:
    """
    Get the text content of the target element in the list of pages
    ...
    Attributes
    __________
    urls: list[str] | list[Url]
        A list of webpages to crawl
    css_selector: str
        An css selector to be used to find target part of page, default 'body'

    Returns
    _______
        A raw text of list of pages 
    """
    text = ""
    pool: list[Future] = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        for url in urls:
            pool.append(executor.submit(get_page_text, url, css_selector))
        
        for process in  fu.as_completed(pool):
            p_text = process.result()
            text += p_text
            #all_words += p_all_words
            #unique_words.update(p_unique_words)
            #tags |= p_tags


    return text

def get_page_text_website(entry_website_url: str, css_selector: str = 'body') -> str:
    """
    To crawl and obtain all text from the website
    ...
    Attributes
    __________
    entry_website_url: str
        An entry website URL to start the crawling process with
    css_selector: str
        An css selector to be used to find target part of page, default 'body'

    
    Returns
    _______
        A raw text of a whole website
    """

    links = crawl_website(entry_website_url)
    internal_links = filter_by_type(links, LinkType.INTERNAL)
    return get_page_text_list(internal_links, css_selector)