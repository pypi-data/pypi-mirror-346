#!/usr/bin/env python3

import json
import requests

class CMDBAPI(object):
    """Класс взаимодействия с API CMDB.
   
    Примеры вызова:
    #   print(cmdb.api_request(api_type='get',api_method='exampleauth'))
    #   print(cmdb.api_request('get','exampleauth'))
    #   print(cmdb.get.exampleauth())

    """    
    def __init__(self, api_host=None, api_user=None,api_password=None,api_token=None,bearer_token=None, api_timeout=10):
        self.token=False
        self.api_host=api_host
        self.api_timeout=int(api_timeout)
        
        if bearer_token:
            result=bearer_token
        else:
            if api_token:
                self.api_token=api_token
                login_data={"key": api_token}
                rapi=requests.post(self.api_host+'/auth/service', data=json.dumps(login_data),headers={'Content-Type': 'application/json'},timeout=self.api_timeout)
            else:
                self.api_user=api_user
                self.api_password=api_password
                login_data={"login": api_user,"password": api_password}
                rapi=requests.post(self.api_host+'/auth/quick', data=json.dumps(login_data),headers={'Content-Type': 'application/json'},timeout=self.api_timeout)

            result=None
            try:
                rapi.raise_for_status()
                result=rapi.text
                    
            except requests.HTTPError as expt:
                raise requests.HTTPError('API request failed with error. ErrorCode: {}. Response: {}'.format(expt.response.status_code,rapi.text))
      
        self.token=result

    def __getattr__(self, attr):
        return CMDBAPIObject(attr,self)

    def api_request(self, api_type='get', api_method='', api_prefix='/v1/', **params):
        """Метод для выполнения запроса к API.
        :param api_type: название запроса (put, get, post, etc.)
        :param api_method: название метода из списка функций API
        :param params: параметры соответствующего метода API
        :return: данные в формате JSON
        """
        try:
            rapi = None
            if api_method=='auth/default':
                login_data={"login": self.api_user,"password": self.api_password}            
                rapi=requests.post(f"{self.api_host}/auth/default", data=json.dumps(login_data),headers={'Content-Type': 'application/json'},timeout=self.api_timeout)
            elif api_type=='post':
                rapi = requests.post(self.api_host+api_prefix+api_method, verify=False, json=params,headers={'Authorization': 'Bearer '+self.token,'Content-Type': 'application/json'}, timeout=self.api_timeout)
            elif api_type=='put':
                rapi = requests.put(self.api_host+api_prefix+api_method, verify=False, json=params,headers={'Authorization': 'Bearer '+self.token,'Content-Type': 'application/json'}, timeout=self.api_timeout)
            elif api_type=='delete':
                rapi = requests.delete(self.api_host+api_prefix+api_method, verify=False, json=params,headers={'Authorization': 'Bearer '+self.token,'Content-Type': 'application/json'}, timeout=self.api_timeout)
            else:
                rapi = requests.get(self.api_host+api_prefix+api_method, verify=False, params=params,headers={'Authorization': 'Bearer '+self.token,'Content-Type': 'application/json'}, timeout=self.api_timeout)
            rapi.raise_for_status()
            return json.loads(rapi.text)
        except (requests.RequestException, requests.ConnectionError) as e:
            if rapi:
                raise CMDBRequestException(f"{e}. URL: {rapi.url}. Headers: {rapi.headers}") from None
            else:
                raise CMDBRequestException(f"{e}") from None
        except (json.JSONDecodeError,requests.HTTPError) as e:
                raise CMDBResponceException(f"Status_code: {e.response.status_code}. URL: {rapi.url}. Headers: {rapi.request.headers} Response: {rapi.text}") from None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.token=False
        self.api_timeout=False
        self.api_host=False
        self.api_user=False
        self.api_password=False

class CMDBRequestException(Exception):
    pass

class CMDBResponceException(Exception):
    pass

class CMDBAPIObject:
    """Динамически вычисляемые объекты CMDB API.

    """
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent

    def __getattr__(self, attr):
        """Динамически создаем методы объекта CMDB API.

        """
        def wrapper(*args, **kw):
            return self.parent.api_request(api_type=self.name, api_method='{}'.format(str(attr)), api_prefix='/v1/', **kw)
        return wrapper
 


