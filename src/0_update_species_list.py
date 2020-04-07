#!/usr/bin/env python3
import requests

response = requests.get('https://docs.google.com/spreadsheets/d/1-7FY-B_BpU72A045EeEuExea6FtMs8q-Urn9-R6-TWk/export?format=tsv')

print(response.text)
