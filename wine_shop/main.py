import argparse
import collections
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape

parser = argparse.ArgumentParser()
parser.add_argument('input_xlsx', help='Input excel file')
args = parser.parse_args()


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

excel_data_df = pd.read_excel(
    io=args.input_xlsx,
    sheet_name="Лист1",
    na_values=['N/A', 'NA'], keep_default_na=False
)
lists = excel_data_df.to_dict(orient='records')
dictionary = collections.defaultdict(list)
i = 1
for list in lists:
    dictionary[i].append(list)
    i += 1
rendered_page = template.render(lists=lists)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
