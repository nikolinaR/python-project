import re
import requests
from cleanco import basename
from jinja2 import Template


def get_companies_name():
    """
    A get request to 'data' endpoint to retrieve the list of companies.
    :return: list of companies
    """
    response = requests.get("http://127.0.0.1:5000/data")
    data = response.json()
    return [row[1] for row in data]


def clean_company_name(company_names):
    """
    Cleans the company names by removing unwanted suffixes and characters and capitalizing first letter
    :param company_names: a list of company names
    :return: a list of cleaned company names
    """
    company_names = [basename(name) for name in company_names]
    unwanted_strings = ["Inc", "Ltd", "LLC", "Corp"]
    for i in range(len(company_names)):
        for unwanted in unwanted_strings:
            company_names[i] = company_names[i].replace(unwanted, "")
    company_names = [name.title() for name in company_names]
    return [re.sub(r'[,\(\)\"-]|-[^-]+-', '', item) for item in company_names]


def new_data():
    """
    creating a list of dictionary with cleaned company data
    :return: html with cleaned company names
    """
    company_names = get_companies_name()
    cleaned_names = clean_company_name(company_names)
    response = requests.get("http://127.0.0.1:5000/data")
    data = response.json()
    compnames1 = []
    for i, row in enumerate(data):
        comp_dict = {"id": row[0], "name": cleaned_names[i], "iso": row[2], "city": row[3], "nace": row[4],
                     "website": row[5]}
        compnames1.append(comp_dict)
    template = Template(open("index.html").read())
    html = template.render(compnames1=compnames1[:100])
    return html


html = new_data()
with open("output1.html", "w") as f:
    f.write(html)

# print(new_data())
url = "http://127.0.0.1:5000/save"
data = new_data()
headers = {"Content-type": "application/json"}
response = requests.post(url, json=data, headers=headers)
print(response.json())












