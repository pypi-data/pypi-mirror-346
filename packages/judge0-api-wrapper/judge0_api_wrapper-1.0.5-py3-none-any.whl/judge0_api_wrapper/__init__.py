import requests
from furl import furl
from .exceptions import *
import time

class Judge0:
    def __init__(self, Judge0_ip: str, X_Auth_Token: str, X_Auth_User: str):
        self.__judge0_ip = furl(Judge0_ip)
        self.__session: requests.Session = requests.session()
        self.__session.headers['X-Auth-Token'] = X_Auth_Token
        self.__session.headers['X-Auth-User'] = X_Auth_User
        self.__check_tokens()
        self.__init_languages_dict()

    def __check_tokens(self):
        """
        The method checks if the given tokens are valid. If invalid, it raises a requests.HTTPError exception; otherwise, it returns None. 
        """
        authn_response = self.__session.post(self.__judge0_ip / 'authenticate')
        authn_response.raise_for_status()
        authz_reponse = self.__session.post(self.__judge0_ip / 'authorize')
        authz_reponse.raise_for_status()

    def __init_languages_dict(self):
        languages_list = self.__session.get(self.__judge0_ip / 'languages').json()
        self.__languages = {item['id']: item['name'] for item in languages_list}

    @property
    def languages(self):
        "The method returns a dict of available languages"
        return self.__languages

    def submit_code(self, source_code: str, language_id: int, stdin: str | None = None, compile_timeout: int | None = None, run_timeout: int | None = None, check_timeout: int | None = None, memory_limit: int | None = None, base64_encoded: bool = True):
        if self.languages.get(language_id) is None:
            raise LanguageNotFound('Unknown language id. Use languages property to get a dict of available languages')
        
        data = {
            'source_code': source_code,
            'language_id': language_id
        }
        #print(self.__session.get('http://5.35.80.93:2358/config_info').json())
        if stdin is not None:
            data['stdin'] = stdin
        if compile_timeout:
            data['compile_timeout'] = compile_timeout
        if run_timeout:
            data['run_timeout'] = run_timeout
        if check_timeout:
            data['check_timeout'] = check_timeout
        if memory_limit:
            data['memory_limit'] = memory_limit * 1000 # minimal value is 2048

        response = self.__session.post(self.__judge0_ip / 'submissions', json=data, params={'base64_encoded': "true" if base64_encoded else "false"})
        response.raise_for_status()
        token = response.json().get('token')
        return token
    
    def submit_file(self, source_code: str, language_id: int, stdin: str | None = None, compile_timeout: int | None = None, run_timeout: int | None = None, check_timeout: int | None = None):
        raise NotImplementedError

    def get_info(self, token: str):
        response = self.__session.get(self.__judge0_ip / 'submissions' / token)
        response.raise_for_status()
        return response.json()
    
    def get_status(self, token: str) -> dict[int, str]:
        response = self.__session.get(self.__judge0_ip / 'submissions' / token)
        response.raise_for_status()
        return response.json().get('status')
    
    def wait_for_completion(self, token: str, poll_interval: int = 1):
        while 1:
            if self.get_status(token).get('id') in [1, 2]:
                time.sleep(poll_interval)
                continue
            break
    
    def get_result(self, token: str, wait: bool = False, poll_interval: int = 1):
        if wait:
            self.wait_for_completion(token, poll_interval)
        if self.get_status(token).get('id') in [1, 2]:
            raise NotProcessed
        return self.get_info(token)