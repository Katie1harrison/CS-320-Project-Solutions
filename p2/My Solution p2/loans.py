# import some_mod
# some_mod.py
# print("Hello from loans.py!")

# def hey():
#     print("Hey! you da bomb")


    
race_lookup = {
    "1": "American Indian or Alaska Native",
    "2": "Asian",
    "21": "Asian Indian",
    "22": "Chinese",
    "23": "Filipino",
    "24": "Japanese",
    "25": "Korean",
    "26": "Vietnamese",
    "27": "Other Asian",
    "3": "Black or African American",
    "4": "Native Hawaiian or Other Pacific Islander",
    "41": "Native Hawaiian",
    "42": "Guamanian or Chamorro",
    "43": "Samoan",
    "44": "Other Pacific Islander",
    "5": "White",
}

    
class Applicant:
    def __init__(self, age, race):
        
        self.age = age
        self.race = set()
        for r in race:
            if r not in race_lookup:
                continue
            self.race.add(race_lookup[r])
            
            
    def __repr__(self):
        ret_statement = f"Applicant('{self.age}', {sorted(list(self.race))})"
        return ret_statement
    
    def lower_age(self):
        return int(self.age.replace("<", "").replace(">", "").split("-")[0])
        
        
    def __lt__(self, other):
        return self.lower_age() < other.lower_age()
    
    
   
    

class Loan:
            
            
    
    def __init__(self, values):
        loan_plc = values["loan_amount"]
        prop_plc = values["property_value"]
        int_plc = values["interest_rate"]
        
        # for plc in [loan_plc,prop_plc,int_plc]:
        #     plc = plc.replace("Exempt", "-1").replace("NA", "-1")
        loan_plc = loan_plc.replace("Exempt", "-1").replace("NA", "-1")
        prop_plc = prop_plc.replace("Exempt", "-1").replace("NA", "-1")
        int_plc = int_plc.replace("Exempt", "-1").replace("NA", "-1")
          
                
            #print(plc)
        self.loan_amount = float(loan_plc)
        self.property_value = float(prop_plc)
        self.interest_rate = float(int_plc)
        
        self.applicants = [Applicant(values["applicant_age"], [values["applicant_race-"+ str(i)] for i in range(1,6)])]
        
        #print(Applicant, "this self")
        if values["co-applicant_age"] != "9999":
            self.applicants.append(Applicant(values["co-applicant_age"], [values["co-applicant_race-"+ str(i)] for i in range(1,6)]))
            
    def __str__(self):
       
        return ("<Loan: "+ str(self.interest_rate)+ "% on $" + str(self.property_value) + " with 1 applicant(s)>")
        
    def __repr__(self):
       
        return ("<Loan: "+ str(self.interest_rate)+ "% on $" + str(self.property_value) + " with 1 applicant(s)>")

    def yearly_amounts(self, yearly_payment):
        
        interest = abs(self.interest_rate)
        amt = abs(self.loan_amount)

        while amt > 0:
            yield amt
            amt = amt *((interest/100) + 1)
            amt = amt - yearly_payment

        
    
        
class Bank:
    def __init__(self, name):
        import json
        import zipfile
        from io import TextIOWrapper
        import csv

        f = open("banks.json")
        #data = f.read()
        data = json.load(f)
        #print(data)
        f.close()
        for bank in data:
            if bank["name"] == name:
                self.lei = bank["lei"]
                
                
        zf = zipfile.ZipFile("wi.zip")

        f = zf.open("wi.csv")
        reader = csv.DictReader(TextIOWrapper(f))
        self.bank_loans = []
        for row in reader:
            #print(row)
            if row['lei'] == self.lei:
                dict_to_loan = Loan(row)
                self.bank_loans.append(dict_to_loan)
            
        # except ValueError:
        #     pass # do nothing

        f.close()

        zf.close()
        
    def __len__(self):
        return len(self.bank_loans)
    
    
    
    def __getitem__(self,index):
        return self.bank_loans[index]
        
        