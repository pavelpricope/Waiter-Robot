import requests
from order import Order

class Database(object):

    def __init__(self):
        self.url = "http://f4f98f9a.ngrok.io"

    def update_people_count(self, table, people):
        pass#requests.post(url = self.url+"/table", data = {'name': table, 'people': people})
        

    def update_bottle_count(self, bottles):
        for b in bottles:
            pass#requests.post(url = self.url+"/product", data = {'name': b[0], 'quantity': b[1]})

    def update_trash(self, table, bottles):
        pass#requests.post(url = self.url+"/notifications", data = {'table': table, 'quantity': bottles})
            
    def get_new_orders(self):
        #r = requests.get(url = self.url+"/order") 
        data = {name: 'name', table: 'Table 4', order: 'Water', quantity: 1, _id: 1}#r.json() 
        orders = []
        for order in data:
            orders.append(Order(order["_id"], order["name"], order["table"], (order["order"],order["quantity"])))
            pass#requests.delete(url = self.url + "/order/" + order["_id"])
        return orders
        
