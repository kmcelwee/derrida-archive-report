import pandas as pd
import re
from urllib.parse import unquote

df_prod = pd.read_json('derrida-prod.jl', lines=True)
df_archive = pd.read_json('derrida-archive.jl', lines=True)

def is_archive_url(url):
    # Remove external links and non-derrida-collection links from archive_urls
    return ('http://localhost:8080/derrida/20210928203330' in url and
            'derridas-margins.princeton.edu' in url)

def sort_query(url):
    # Sort the HTML query for better equivilancy tracking
    if '?' in url:
        path, query = url.split('?')
        query = '&'.join(sorted(query.split('&')))
        return path + '?' + query
    else:
        return url

def standardize_url(url):
    # Strip localhost prefix from archive_urls (only relevant for archive urls)
    url = re.sub(r'http://localhost:8080/derrida/20210928203330(.*?)/', '', url)

    # Standardize HTML queries
    url = sort_query(url)

    # Handle URL encoding
    url = unquote(url)

    # Ensure that trailing slashes and https/https don't prevent comparisons
    return url.replace('https://', '').replace('http://', '').replace('http:/', '') \
        .replace('https:/', '').strip('/')

# Only include relevant archive links
df_archive = df_archive[df_archive['url'].apply(is_archive_url)]

df_archive['url_raw'] = df_archive['url'].copy()
df_prod['url_raw'] = df_prod['url'].copy()
df_archive['url'] = df_archive['url'].apply(standardize_url)
df_prod['url'] = df_prod['url'].apply(standardize_url)

df_prod['url'].to_csv('standardized-production-urls.txt', index=False, header=False, sep=';')
df_archive['url'].to_csv('standardized-archive-urls.txt', index=False, header=False, sep=';')

prod_urls = set(df_prod['url'])
archive_urls = set(df_archive['url'])


print('Links in prod but not in the archive:')
for url in sorted(list(prod_urls - archive_urls)):
    print('\t' + url)


print('Links in the archive but not in prod:')
for url in sorted(list(archive_urls - prod_urls)):
     print('\t' + url)