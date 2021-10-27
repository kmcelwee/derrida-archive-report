# Compare scrape of live Derrida's Margins with its wayback archive

Use caliper to understand the gaps in our web archiving script.

## Crawling Production

On Oct 12, 2021, scraped Derrida's production (17 minutes)

```sh
scrapy crawl caliper -a url=https://derridas-margins.princeton.edu/ -o derrida-prod.jl
```

No errors were reported. There are 10,454 links in [`derrida-prod.jl`](derrida-prod.jl)

## Crawling the Archive

On Oct 13, 2021, scraped of the Wayback output from the 
[archived version of the site](https://github.com/Princeton-CDH/derridas-margins-archive/) run locally (6 minutes)

```sh
scrapy crawl caliper -a url=http://localhost:8080/derrida/20210928203330/https://derridas-margins.princeton.edu/ -o derrida-archive.jl
```

There are 21,018 links in [`derrida-archive.jl`](derrida-archive.jl)

The details about the errors that popped up when implementing this scrape are noted in
[local-crawl-report.md](local-crawl-report.md). But here are some key takeaways:

* Some static files were not included in the wayback archive. Do we care?
* Robots.txt was not included, but we're adding that in manually, so it shouldn't matter, correct?
* Some of author search queries are not included in our scrape and some even cause 404s on
production.

## Comparing the Archive with Production

The script [`prod-and-archive-comparison.py`](prod-and-archive-comparison.py)
 finds where the two sets do not intersect. It's output:

```
Links in prod but not in the archive:
    derridas-margins.princeton.edu/sitemap-book-gallery.xml
    derridas-margins.princeton.edu/sitemap-book-pages.xml
    derridas-margins.princeton.edu/sitemap-book-references.xml
    derridas-margins.princeton.edu/sitemap-books.xml
    derridas-margins.princeton.edu/sitemap-pages.xml
    derridas-margins.princeton.edu/sitemap.xml
Links in the archive but not in prod:
```

Hooray 🎉 sitemap is the only files where the two sets differ after standardizing.
(Look at the script for details on how the two lists were standardized.)

## Querying data

Use the `lines=True` kwarg to read in `jl` files:

```python
import pandas as pd

df_prod = pd.read_json('derrida-prod.jl', lines=True)
df_archive = pd.read_json('derrida-archive.jl', lines=True)
```
