# Définir les classes dans le module dynamique
module_code = """
from dataclasses import dataclass
from typing import  List

class Executor:

    # Classes pour les objets injectés
    @dataclass
    class ResourceAttribute:
        key: str
        value: str
        
    
    @dataclass
    class Resource:
        resource_type_name: str
        resource_id: str
        attributes: List[ResourceAttribute]
    
    
    @dataclass
    class SubjectAttribute:
        key: str
        value: str
    
    
    @dataclass
    class Subject:
        subject_type_name: str
        subject_id: str
        attributes: List[SubjectAttribute]
    
            
    def __init__(
        self,
        subject: Subject, 
        resource: Resource,
    ):
        self.subject = subject
        self.resource = resource

    def __call__(self):
        return self.rule(self.subject, self.resource)


"""
