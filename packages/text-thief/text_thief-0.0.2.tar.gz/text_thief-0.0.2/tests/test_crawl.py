import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from src.text_thief.text_thief import get_page_text, get_page_text_list, get_page_text_website, procced_text, TextProcced


def test_crawl_page_not_url():
    text = get_page_text("some")
    res  = procced_text(text)
    print(text)
    assert len(text) == 0
    assert len(res.all_words) == 0
    assert len(res.unique_words) == 0
    assert len(res.tags) == 0

def test_crawl_page_whole_body():
    text = get_page_text("http://localhost:8000/scrapable/1/")
    res  = procced_text(text)
    print(text)
    assert len(text) == 1360
    assert len(res.all_words) == 214
    assert len(res.unique_words) == 139
    assert len(res.tags) == 139

def test_crawl_page_selector():
    text = get_page_text("http://localhost:8000/scrapable/1/", 'body>.to_select')
    res  = procced_text(text)
    print(text)
    assert len(text) == 963
    assert len(res.all_words) == 142
    assert len(res.unique_words) == 91
    assert len(res.tags) == 91

def test_crawl_page_list_whole_body():
    list = ["http://localhost:8000/scrapable/1/",
            "http://localhost:8000/scrapable/2/"]
    text = get_page_text_list(list)
    res  = procced_text(text)
    print(text)
    assert len(text) == 2484
    assert len(res.all_words) == 398
    assert len(res.unique_words) == 168
    assert len(res.tags) == 168

def test_crawl_page_list_selector_similar_on_both():
    list = ["http://localhost:8000/scrapable/1/",
            "http://localhost:8000/scrapable/2/"]
    text = get_page_text_list(list, 'body>.to_select')
    res  = procced_text(text)
    print(text)
    assert len(text) == 1694
    assert len(res.all_words) == 254
    assert len(res.unique_words) == 120
    assert len(res.tags) == 120

def test_crawl_page_list_selector_different_on_both():
    list = ["http://localhost:8000/scrapable/1/",
            "http://localhost:8000/scrapable/2/"]
    text = get_page_text_list(list, 'body>.to_select_diff')
    res  = procced_text(text)
    print(text)
    assert len(text) == 731
    assert len(res.all_words) == 112
    assert len(res.unique_words) == 75
    assert len(res.tags) == 75

def test_crawl_whole_website():
    text = get_page_text_website("http://localhost:8000/scrapable/1/")
    res  = procced_text(text)
    print(text)
    assert len(text) == 6488
    assert len(res.all_words) == 1040
    assert len(res.unique_words) == 203
    assert len(res.tags) == 203

def test_crawl_whole_website_by_selector():
    text = get_page_text_website("http://localhost:8000/scrapable/1/", 'h1')
    res  = procced_text(text)
    print(text)
    assert len(text) == 324
    assert len(res.all_words) == 60
    assert len(res.unique_words) == 8
    assert len(res.tags) == 8