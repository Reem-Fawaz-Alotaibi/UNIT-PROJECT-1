class UnknownPerson:
    def __init__(self, patient_id, age, gender, hair, eye, height, marks, date, location,status = "Not identified"):
        self.patient_id = patient_id    
        self.age = age                  
        self.gender = gender            
        self.hair = hair                
        self.eye = eye                  
        self.height = height           
        self.marks = marks              
        self.date = date                
        self.location = location  
        self.status = status
      

    def to_dict(self):
        return {
            "patient_id": self.patient_id,
            "age": self.age,
            "gender": self.gender,
            "hair": self.hair,
            "eye": self.eye,
            "height": self.height,
            "marks": self.marks,
            "date": self.date,
            "location": self.location,
            "status": self.status
        }