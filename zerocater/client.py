import json
import httplib2
import re


class ZeroCaterClient(object):
    def __init__(self, username=None, password=None, token=None):
        self._base_url = 'https://zerocater.com/api/v3'
        self._http_client = httplib2.Http()

        self.urls()
        if token:
            self._token = token
        elif username and password:
            self._get_token(username, password)
        else:
            raise Exception('You must supply either a token, or username and password.')
        self.get_user()
        self.get_meals_url()

    def __repr__(self):
        return '<ZeroCater Client: %s>' % (self.name,)

    def _build_url(self, url, **kwargs):
        url = re.sub(r'\{\?.+\}', '', url) # Take out optional GET params
        for kwarg in kwargs.iterkeys():
            # Replace all kwargs
            url = url.replace('{%s}' % (kwarg), kwargs[kwarg])
        return '%s' % (url,)

    @property
    def urls(self):
        if hasattr(self, '_urls'):
            return self._urls
        url = self._base_url
        resp, content = self._http_client.request(url, 'GET')
        url_dict = json.loads(content)
        self._urls = url_dict
        return url_dict

    def _get_token(self, username, password):
        url = self.urls['token_url']
        h = httplib2.Http('.cache')
        h.add_credentials(username, password)
        resp, content = h.request(url)
        content_dict = json.loads(content)
        self._token = content_dict['token']

    def _build_request(self, url, method='GET', body=None, headers=None, **kwargs):
        if not headers:
            headers = {}
        url = self._build_url(url, **kwargs)
        headers['Authorization'] = 'Token %s' % (self._token,)
        return self._http_client.request(url, method, body=body, headers=headers)

    def get_user(self):
        resp, content = self._build_request(self.urls['current_user_url'])
        user_dict = json.loads(content)
        self.company_url = user_dict['company_url']
        self.name = user_dict['name']
        return user_dict

    def get_meals_url(self):
        resp, json_content = self._build_request(self.company_url)
        content = json.loads(json_content)
        self.meals_url = content['meals_url']
        return content

    def get_companies(self):
        url = self.urls['companies_url']
        resp, json_content = self._build_request(url)
        content = json.loads(json_content)
        return content

    def get_company(self, short_mangled_id):
        url = self.urls['company_url']
        resp, json_content = self._build_request(url, short_mangled_id=short_mangled_id)
        content = json.loads(json_content)
        return content

    def get_company_meals(self, short_mangled_id):
        url = self.urls['meals_url']
        resp, json_content = self._build_request(url, short_mangled_id=short_mangled_id)
        content = json.loads(json_content)
        return content

    def get_meal(self, short_mangled_id, meal_id):
        url = self.urls['meals_url']
        resp, json_content = self._build_request(url, short_mangled_id=short_mangled_id, meal_id=meal_id)
        content = json.loads(json_content)
        return content

    def get_user_meals(self):
        url = self.meals_url
        resp, json_content = self._build_request(url)
        content = json.loads(json_content)
        return content
