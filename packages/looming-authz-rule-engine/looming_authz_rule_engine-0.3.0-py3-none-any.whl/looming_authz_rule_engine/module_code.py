# Définir les classes dans le module dynamique
module_code = """
from dataclasses import dataclass
from typing import  List

class Executor:

    # Classes pour les objets injectés
    @dataclass
    class Subject:
        subject_id: str
        subject_type_name: str
    
    
    @dataclass
    class Context:
        context_type_name: str
    
    
    @dataclass
    class UserAttribute:
        key: str
        value: str
            
    def __init__(
        self,
        subject: Subject, 
        context: Context, 
        user_attributes: List[UserAttribute]
    ):
        self.subject = subject
        self.context = context
        self.user_attributes = user_attributes

    def __call__(self):
        return self.rule(self.subject, self.context, self.user_attributes)



"""
