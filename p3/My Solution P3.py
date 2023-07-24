# project: p3
# submitter: kfharrison
# partner: none
# hours: 15

import pandas as pd
from collections import deque 
import time
import requests
from PIL import Image

class GraphSearcher:
    def __init__(self):
        self.visited = set()
        self.order = []

    def visit_and_get_children(self, node):
        """ Record the node value in self.order, and return its children
        param: node
        return: children of the given node
        """
        raise Exception("must be overridden in sub classes -- don't change me here!")
    
    def bfs_search(self, node):
        todo = deque([node])
        seen_before = {node}
       
        while todo:
            curr = todo.popleft() # pop from beginning
            children = self.visit_and_get_children(curr)
           
            for child in children:
                
                if not child in seen_before:
              
                    seen_before.add(child)
                    todo.append(child) # add to end

    def dfs_search(self, node):
        self.visited = set()
        self.order = []
        
        self.dfs_visit(node)
        
        
    def dfs_visit(self, node):
        # 1. if this node has already been visited, just `return` (no value necessary)
        if node in self.visited:
            return
        # 2. mark node as visited by adding it to the set
        if node not in self.visited:
            self.visited.add(node)
        # 3. call self.visit_and_get_children(node) to get the children
        #self.visit_and_get_children(node)
        # 4. in a loop, call dfs_visit on each of the children
        children = self.visit_and_get_children(node)
        for child in children:
            # print(self.order)
            self.dfs_visit(child)
                   




class MatrixSearcher(GraphSearcher):
    def __init__(self, df):
        super().__init__() # call constructor method of parent class
        self.df = df

    def visit_and_get_children(self, node):
        
        # TODO: Record the node value in self.order
        self.order.append(node)
        children = []
        # TODO: use `self.df` to determine what children the node has and append them
        #print(df)
        #print(node)
        #print(self.df.loc[node])
        for n, has_edge in self.df.loc[node].items():

            # print(has_edge)
            # print(node)
            if has_edge:
                children.append(n)
        return children

    
    
    
    
    
    
class FileSearcher(GraphSearcher):
    def __init__(self):
        super().__init__()
          
        
    def visit_and_get_children(self, node):

        f = open("file_nodes/"+ node)
        data = f.read()
        f.close()
        #print(data)
        children = []
        self.order.append(data.split("\n")[0])
        #print(data.split("\n")[0])
        for child in data.split("\n")[1].split(","):
            children.append(child)
        return children
            
    def concat_order(self):
        return ("").join(self.order)

    

class WebSearcher(GraphSearcher):
    def __init__(self, driver):
        super().__init__()
        self.tables = []
        self.driver = driver
       
    def visit_and_get_children(self, node_url):
        self.driver.get(node_url) #I don't know what this line is doing exactly but it's needed to set the inital url
        children = []
        
        for el in self.driver.find_elements("tag name", "a"):
            children.append(el.get_attribute("href"))
        self.order.append(node_url)
        pg_table = pd.read_html(self.driver.page_source)[0]
        self.tables.append(pg_table)
        
        return children
        
    
    def table(self): 
        return pd.concat(self.tables,ignore_index=True)
    
    
def reveal_secrets(driver, url, travellogz):
    list_travels = list(travellogz["clue"])
    password = "".join(str(el) for el in list_travels)
    2#
    driver.get(url)   
    3#
    text = driver.find_element("id", "password")
    go_btn = driver.find_element("id", "attempt-button")
    text.send_keys(password)
    go_btn.click()
 
    4# 
    time.sleep(3)
    
    
    
    
    # driver.save_screenshot("ss.png")
    # screenshot = Image.open('ss.png')
    # screenshot.show()
    #5
    loc_btn = driver.find_element("id", "securityBtn")
    loc_btn.click()
 
    resp = requests.get(url)
    status = resp.status_code
    time.sleep(7)
      
    
#     driver.save_screenshot("ss.png")
#     screenshot = Image.open('ss.png')
#     screenshot.show()


#6
    dumb_location = driver.find_element("id", "image").get_attribute("src")
    #print(dumb_location)

    url = dumb_location
    
    #copied/adapted from https://stackoverflow.com/questions/13137817/how-to-download-image-using-requests
    response = requests.get(url)
    if response.status_code == 200:
        with open("Current_Location.jpg", 'wb') as f:
            f.write(response.content)
            
            
#7            
            
    location = driver.find_element("id", "location")
    return location.text