import requests
from lxml import html
from toolz import pipe
import json


def parse_html(html_string):
    return html.fromstring(" ".join(html_string.split()))


def get_number_of_pages():
    return pipe(requests.get("http://jobs.ge/").text
                , parse_html
                , lambda x: x.cssselect(".pagebox")
                , len) + 1


# print(get_number_of_pages())
# regular_entries = parsed_html.cssselect(".regularEntries")[0][0] #vip gancxadebebic aqaa

data = []
#
for page in range(1, get_number_of_pages() + 1):
    # http://jobs.ge/?page=
    specific_page = requests.get("http://jobs.ge/?page=" + str(page)).text
    parsed_html = parse_html(specific_page)
    regular_entries = parsed_html.cssselect(".regularEntries")[0][0]  # vip gancxadebebic aqaa
    for gancxadeba in regular_entries:
        template = {"link": "",
                    "განცხადების სახელი": gancxadeba[1].text_content(),
                    "მომწოდებლის ლოგო": "",
                    "მომწოდებელი": gancxadeba[3].text_content(),
                    "გამოქვეყნდა": gancxadeba[4].text_content(),
                    "ვადა": gancxadeba[5].text_content()}

        try:
            template["მომწოდებლის ლოგო"] = gancxadeba[2][0][0].attrib["src"]
        except:
            pass

        try:
            template["link"] = gancxadeba[1][0].attrib["href"]
        except:
            pass
        data.append(template)
    # print(len(regular_entries))

with open('data.json', 'w') as fp:
    json.dump(data, fp, ensure_ascii=False)
