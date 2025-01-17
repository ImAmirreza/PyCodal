import requests
import json
from setting import MAIN_HEADERS
import re
def arabic_to_english(arabic_num):
    mapping = {
        '۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4',
        '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9',"-":"-"
    }
    return ''.join(mapping[c] for c in arabic_num)

def get_html(url):
    """Makes a GET request to the specified URL and returns the HTML response."""
    return requests.get(url, headers=MAIN_HEADERS).text

def get_json(url):
    """Extracts a JSON string from the HTML response using a regular expression and parses it into a Python object."""
    html_source = get_html(url)
    pattern = r"var datasource = (.*?)</script>"
    match = re.search(pattern, html_source, re.DOTALL)
    if match:
        json_string = match.group(1).strip().replace(";","")
        try:
            data = json.loads(json_string)
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON: {e}")
            print(json_string)
            return None
    else:
        print("No match found.")
        return None
    return data