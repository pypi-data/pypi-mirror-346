# chainecho

Python API Client for https://chainecho.me


## Install

```
pip install chainecho
```

## Usage

```python
import chainecho
```

Get latest news and categories by calling chainecho API:


```python

api_key = os.getenv("API_KEY")
api = chainecho.API(api_key)

news = api.getLatestNews(limit=20)
print(news)

categories = api.getCategories()
print(categories)

```


News response format is as the following:


| Field           | Type    | Description               |
| --------------- | ------- | ------------------------- |
| `id`            | integer | Unique ID                 |
| `ntype`         | string  | News Type                 |
| `nid`           | integer | News ID                   |
| `guid`          | string  | News GUID                 |
| `published_on`  | string  | Published Date            |
| `image_url`     | string  | News Thumbnail URI        |
| `title`         | string  | News Title                |
| `url`           | string  | News URI                  |
| `source_id`     | integer | Source ID                 |
| `body`          | string  | Summary Content           |
| `keywords`      | string  | Keywords                  |
| `lang`          | string  | Language                  |
| `category`      | string  | Categories                |

