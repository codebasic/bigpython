# coding: utf-8
import importlib

import requests
import pandas as pd
from bs4 import BeautifulSoup

class Html(BeautifulSoup):
    def __init__(self, html):
        parser = 'lxml' if importlib.find_loader('lxml') else 'html.parser'
        super().__init__(html, parser, from_encoding='utf-8')

    def get_text(self, selector='p'):
        elements = self.select(selector)
        text = ''
        for e in elements:
            text += e.text
            text += '\n'

        return text

    def extract_tables(self, selector):
        table_elements = self.select(selector)
        table_frames = pd.read_html(str(table_elements))
        return table_frames[0] if len(table_frames) == 1 else table_frames
