code = '''
Server.py:
import Pyro5.api

@Pyro5.api.expose
class StringService:
    def concatenate(self, s1, s2):
        return s1 + s2

def main():
    daemon = Pyro5.api.Daemon()                      
    uri = daemon.register(StringService)             
    print("Server is ready. Object URI =", uri)     
    daemon.requestLoop()                             

if __name__ == "__main__":
    main()

Client.py:

import Pyro5.api


uri = input("Enter the server URI ( eg. PYRO:obj.....): ")
string_service = Pyro5.api.Proxy(uri)     


s1 = input("Enter first string: ")
s2 = input("Enter second string: ")

result = string_service.concatenate(s1, s2)
print("Concatenated result from server:", result)
'''
print(code)