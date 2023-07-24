# project: p7
# submitter: kfharrison
# partner: none
# hours: 10


import numpy
import sklearn.model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import cross_val_score
import pandas as pd

class UserPredictor:
   
    def __init__(self):
        model = LogisticRegression()
        self.model = model
        self.oh = OneHotEncoder()
        self.cols = ["age","past_purchase_amt", "gold", "silver", "bronze", "seconds_x","seconds_y"]

       
    def fit(self, users, logs, train_y):
        users = self.hottie_userkt(users,logs)
        self.model.fit(users[self.cols],train_y["y"]) # X , y:
       
    def predict(self,users,logs):
        users = self.hottie_userkt(users,logs)

        tf_prediction= self.model.predict(users[self.cols]) 
        new_y_pred = []

        for i in range(len(tf_prediction)):
            if tf_prediction[i] == False:
                new_y_pred.append(0)

            else:
                new_y_pred.append(1)

        return numpy.array(new_y_pred)

    def score_Nixie(self, users, y, logs):
        users = self.hottie_userkt(users, logs)
        
        scores = cross_val_score(self.model, users[self.cols], y["y"])
        print(f"AVG: {scores.mean()}, STD: {scores.std()}\n")
       
       
        return self.model.score(users[self.cols], y["y"])
       
   
    def hottie_userkt(self, users, logs):
        

        users1 = pd.DataFrame(self.oh.fit_transform(users[["badge"]]).toarray(), columns =self.oh.get_feature_names_out())
        users[["bronze","gold","silver"]] = users1[["badge_bronze", "badge_gold", "badge_silver"]]

        
        url_laptop = logs[logs["url"] == "/laptop.html"]
        group_laptop = url_laptop.groupby(['user_id',"url"])['seconds'].sum()


        url_tablet = logs[logs["url"] == "/tablet.html"]
        group_tablet = url_tablet.groupby(['user_id',"url"])['seconds'].sum()



        

        tablet_laptop= pd.merge(group_tablet,group_laptop, on='user_id',how="outer")
        tablet_laptop.fillna(0)



        logs_users = pd.merge(users,tablet_laptop, on='user_id',how="outer")
        logs_users.fillna(0)

        return logs_users.fillna(0)
        