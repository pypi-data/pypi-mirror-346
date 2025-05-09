import re

import concurrent.futures as fu

from concurrent.futures import ThreadPoolExecutor, Future

from bs4 import BeautifulSoup

from link_thief.link_thief import LinkType, Url, _get_page, crawl_website, filter_by_type

CHARS_TO_REMOVE="\\`*_{}[]()>#+-.!$" 

def _filter_unique_words_only(words: list) -> set[str]:
    words_only_uniques = set(words)
    return words_only_uniques

def _clean_up(text: str) -> list[str]:
    """
    Procced the raw text from page and return a list of the all founded words
    ...
    Attributes
    __________
    text: str
        A raw text without HTML or other markup
    
    Returns
    _______
        A list of words
    """
    return re.sub("[^\w]", " ",  text).split()

def _count_words(all_words: list, unique_words: set) -> dict[str,int]:
    """
    Create a dict with words as an keys and number of occurence as a values
    ...
    Attributes
    __________
    all_words: list
        A list of all words
    unique_words: set
        A list of unique words from 'all_words'
    
    Returns
    _______
        A dict with words as an keys and number of occurence as a values
    """
    tags = {}
    for word in all_words:
        if word in unique_words:
            if tags.get(word):
                tags.update({word: tags[word] + 1})
            else:
                tags.update({word: 1})
    return tags


def get_page_text(url: str | Url, css_selector: str = 'body') -> tuple[str, list, set, dict]:
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
        A tulpe of raw text of page, a list of all words on page, a set of unique words on page and dict of tags with numbers of occurence
    """
    text = ""
    all_words = []
    unique_words = []
    tags = {}
    status_code, page = _get_page(url)
    if status_code == 200:
        soup = BeautifulSoup(page, 'lxml')
        page_part_soup = soup.select(css_selector) 
        for part in page_part_soup:
            text += part.text

    
    all_words = _clean_up(text)
    unique_words = _filter_unique_words_only(all_words)
    tags = _count_words(all_words, unique_words)

    return text, all_words, unique_words, tags

def get_page_text_list(urls: list[str] | list[Url], css_selector: str = 'body') ->  tuple[str, list, set, dict]:
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
        A tulpe of raw text of list of pages, a list of all words in a list of pages, a set of unique words in a list of pages and dict of tags with numbers of occurence
    """
    text = ""
    all_words = []
    unique_words = set()
    tags = {}
    pool: list[Future] = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        for url in urls:
            pool.append(executor.submit(get_page_text, url, css_selector))
        
        for process in  fu.as_completed(pool):
            p_text, p_all_words, p_unique_words, p_tags = process.result()
            text += p_text
            all_words += p_all_words
            unique_words.update(p_unique_words)
            tags |= p_tags


    return text, all_words, unique_words, tags

def get_page_text_website(entry_website_url: str, css_selector: str = 'body') -> tuple[str, list, set, dict]:
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
        A tulpe of raw text on a website, a list of all words on a website, a set of unique words on a website and dict of tags with numbers of occurence
    """

    links = crawl_website(entry_website_url)
    internal_links = filter_by_type(links, LinkType.INTERNAL)
    return get_page_text_list(internal_links, css_selector)