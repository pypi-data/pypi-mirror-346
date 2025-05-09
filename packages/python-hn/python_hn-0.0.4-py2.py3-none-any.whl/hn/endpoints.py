from urllib.parse import urljoin

BASE_API_URL = 'https://hn.algolia.com/api/v1/'

SEARCH_BY_DATE = urljoin(BASE_API_URL, 'search_by_date')
ITEMS = urljoin(BASE_API_URL, 'items/{id}')
USERS = urljoin(BASE_API_URL, 'users/{id}')
