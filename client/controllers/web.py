import requests
from functools import partial

from client.controllers import Base, APIError

class Controller(Base):
    def _req(self, method, endpoint, *a, **kw):
        if hasattr(self, "token"):
            kw["headers"] = {"Authorization": f"Bearer {self.token}"}
        try:
            req = getattr(requests, method.lower(), "get").__call__(
                f"{self.apiurl}/{endpoint}", *a, **kw)
        except:
            raise APIError("ConnectionError", "Cannot connect to API")
        else:
            if req.status_code//100 == 2:
                return req
            else:
                data = req.json()
                raise APIError(data["type"], data["message"])
        
    
    def __init__(self, username, password, apiurl="http://127.0.0.1/api"):
        self.apiurl = apiurl
        req = self._req("get", "auth/login", 
                auth=(username, password))
                
        data = req.json()

        self.token = data["token"]
        self.username = username
    
    def get_pages(self):
        req = self._req("get", "stats/page")
        
        return req.json()
            
    def put_page(self, page):
        self._req("put", "stats/page", json=page)
        
    def change_pwd(self, pwd, new):
        self._req("put", "users/me", json={
            "opassword": pwd,
            "password": new
        })
    