import re
from urllib.parse import urlparse, parse_qs

class FeatureExtractor:
    SUSPECT_KEYWORDS = ['admin', 'login', 'config', 'debug', 'private', 'publico']

    def __init__(self, headers: dict, method: str, url: str, body: str = ''):
        self.headers = {k.lower(): v for k, v in headers.items()}
        self.method = method.upper()
        self.url = url
        self.body = body

    def extract(self):
        features = {}
        features['Accept'] = 'accept' in self.headers
        features['content-type'] = 'content-type' in self.headers
        conn_val = self.headers.get('connection', None)
        features['connection'] = 1.0 if conn_val else 0.0
        features['lenght'] = float(len(self.body))
        features['GET'] = self.method == 'GET'
        features['POST'] = self.method == 'POST'
        features['PUT'] = self.method == 'PUT'

        parsed = urlparse(self.url)
        path = parsed.path
        query = parsed.query

        features['path_length'] = float(len(path))
        features['path_depth'] = float(path.count('/'))
        features['has_admin'] = float(int(any('admin' in part.lower() for part in path.split('/'))))
        features['has_publico'] = float(int('publico' in path.lower()))
        features['query_length'] = float(len(query))
        params = parse_qs(query)
        features['num_params'] = float(len(params))
        features['has_query'] = float(int(bool(query)))
        features['query_suspect'] = float(int(any(k.lower() in query.lower() for k in self.SUSPECT_KEYWORDS)))
        return features
