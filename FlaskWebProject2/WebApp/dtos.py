
class managersDTO:
    def __init__(self, id, name, email, password):
        self.id=id
        self.name=name
        self.email=email
        self.password=password


class tasksDTO:
    def __init__(self, id, name, description, project_id, user_id, deadline):
        self.id=id
        self.name=name
        self.description=description
        self.project_id=project_id
        self.user_id=user_id
        self.deadline=deadline
        
class developersDTO:
    def __init__(self, id, name, email):
            self.id=id
            self.name=name
            self.email=email
            
class project_developersDTO:
        def __init__ (self, developer_id, project_id):
                self.developer_id=developer_id
                self.project_id=project_id

class projectDTO:
    def __init__(self, name, type_id, description):
        self.name = name
        self.type_id = type_id
        self.description = description
        
class project_typesDTO:
    def __init__(self, id, name):
         self.id=id
         self.name = name