import csv
import json

DATA_ADS = 'ad.csv'
JSON_ADS = 'ad.json'
DATA_CATEGORIES = 'category.csv'
JSON_CATEGORIES = 'category.json'
DATA_LOCATION = 'location.csv'
JSON_LOCATION = 'location.json'
DATA_USER = 'user.csv'
JSON_USER = 'user.json'


def convert_file(csv_file, json_file, model_name):
    result = []
    with open(csv_file, encoding='utf-8') as csv_f:
        for row in csv.DictReader(csv_f):
            to_add = {'model': model_name, 'pk': int(row['Id'] if 'Id' in row else row['id'])}
            if 'Id' in row:
                del row['Id']
            else:
                del row['id']
            if 'is_published' in row:
                if row['is_published'] == 'TRUE':
                    row['is_published'] = True
                else:
                    row['is_published'] = False
            to_add['fields'] = row
            result.append(to_add)
    with open(json_file, 'w', encoding='utf-8') as json_f:
        json_f.write(json.dumps(result, ensure_ascii=False))


convert_file(DATA_CATEGORIES, JSON_CATEGORIES, 'ads.categories')
convert_file(DATA_ADS, JSON_ADS, 'ads.ads')
convert_file(DATA_USER, JSON_USER, 'ads.user')
convert_file(DATA_LOCATION, JSON_LOCATION, 'ads.location')
