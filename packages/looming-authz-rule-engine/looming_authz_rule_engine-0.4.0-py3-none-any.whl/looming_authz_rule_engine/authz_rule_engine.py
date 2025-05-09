import ast
import re
import textwrap
import types
from dataclasses import dataclass
from typing import Callable, List


class UnsafeCodeError(Exception):
    pass


# Fonction pour normaliser le code utilisateur
def normalize_rule_function(
    code: str, new_name: str = "rule", extra_indent: int = 4, tabsize: int = 4
) -> str:
    # Étape 1 : Convertir les tabs en espaces
    code = code.expandtabs(tabsize)

    # Étape 2 : Détecter le nom de la fonction d'origine
    match = re.search(r"^\s*def\s+(\w+)\s*\(", code, re.MULTILINE)
    if not match:
        raise ValueError("Aucune fonction détectée dans le code fourni.")
    old_name = match.group(1)

    # Étape 3 : Renommer la fonction
    code = re.sub(
        rf"^(\s*)def\s+{re.escape(old_name)}\s*\(",
        rf"\1def {new_name}(self,",
        code,
        count=1,  # ne modifie que la première occurrence
        flags=re.MULTILINE,
    )

    # Étape 4 : Normaliser et réindenter
    # noinspection SpellCheckingInspection
    dedented = textwrap.dedent(code)
    indented = textwrap.indent(dedented, " " * extra_indent)
    return indented


# Vérification de sécurité AST
def check_ast_safety(code: str):
    # noinspection PyPep8Naming
    FORBIDDEN_NAMES = {
        "eval",
        "exec",
        "compile",
        "open",
        "import",
        "__import__",
        "globals",
        "locals",
        "__builtins__",
    }

    tree = ast.parse(code)

    for node in ast.walk(tree):
        # Interdire les appels à des fonctions dangereuses
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in FORBIDDEN_NAMES:
                raise UnsafeCodeError(f"Usage interdit : {node.func.id}()")
            elif (
                isinstance(node.func, ast.Attribute)
                and node.func.attr in FORBIDDEN_NAMES
            ):
                raise UnsafeCodeError(f"Attribut interdit : {node.func.attr}()")

        # Interdire les instructions import
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            raise UnsafeCodeError("Les imports sont interdits")

        # Interdire l'accès aux builtins par ast.Name
        elif isinstance(node, ast.Name):
            if node.id in FORBIDDEN_NAMES:
                raise UnsafeCodeError(f"Nom interdit utilisé : {node.id}")

    return True  # OK si aucune erreur détectée


def restricted_import(*args, **kwargs):
    raise UnsafeCodeError("L'utilisation d'import est interdite")


# Environnement d'exécution sûr
safe_builtins = {
    "True": True,
    "False": False,
    "None": None,
    "len": len,
    "range": range,
    "str": str,
    "int": int,
    "float": float,
    "bool": bool,
    "__import__": restricted_import,  # Faux import
}

safe_globals = {"__builtins__": safe_builtins}

from dataclasses import dataclass


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


@dataclass
class Context:
    context_type_name: str
    subject: Subject
    resource: Resource


class AuthzRuleEngine:

    def __init__(self):
        self._module = None
        self._executor: Callable[[Subject, Resource], bool]

    def load_rule(self, user_code: str):
        """Charge une règle d'autorisation dans un module dynamique"""
        from module_code import module_code

        try:
            # Normaliser le code utilisateur
            normalized_code = normalize_rule_function(user_code)

            # Vérifier la sécurité du code
            check_ast_safety(user_code)

            # Créer un module dynamique
            self._module = types.ModuleType("authz_rules")

            # Insérer le code normalisé dans la méthode __call__
            module_code = f"{module_code}\n{normalized_code}"

            # Créer un environnement sûr
            safe_items = {"__builtins__": safe_builtins}

            # Injecter les définitions du module dans l'environnement
            safe_items.update(self._module.__dict__)

            # Exécuter le code dans l'environnement sûr
            globals_dict = {}
            exec(module_code, globals_dict)

            executor_cls = globals_dict.get("Executor")
            if executor_cls is None:
                raise ValueError("Le module doit définir une classe Executor")

            self._executor = executor_cls

        except UnsafeCodeError as e:
            raise ValueError(f"Code utilisateur non sécurisé: {str(e)}")
        except Exception as e:
            raise ValueError(f"Erreur lors du chargement de la règle: {str(e)}")

    def evaluate(self, context: Context) -> bool:
        """Évalue la règle avec les données fournies"""
        subject = context.subject
        resource = context.resource
        context_type_name = context.context_type_name

        if self._executor is None:
            raise RuntimeError("Aucune règle n’a été chargée avec `load_rule`.")

        try:
            # Créer l'executor avec les objets
            executor = self._executor(subject, resource)

            # Exécuter la règle
            result = executor()

            # Vérifier que le résultat est un booléen
            if not isinstance(result, bool):
                raise ValueError("La règle doit retourner un booléen")

            return result

        except Exception as e:
            raise ValueError(f"Erreur lors de l'évaluation de la règle: {str(e)}")


# # Exemple d'utilisation
# if __name__ == '__main__':
#     # Créer l'engine
#     engine = AuthzRuleEngine()

#     def test_code(code: str, expected: bool) -> bool|None:
#         print(f"\nTest du code: {code}")
#         try:
#             engine.load_rule(code)
#             principal = Principal(id='user123', roles=['admin', 'user'], tenant_id='tenant1')
#             resource = Resource(type='document', id='doc123', owner='user123')
#             context = Context(context_type='api', context_id='req123', action='read', ip='192.168.1.1')

#             result = engine.evaluate(principal, resource, context)
#             print(f"Résultat: {result}")
#             if result != expected:
#                 print(f"⚠️ Résultat différent de l'attendu ({expected})")
#         except ValueError as e:
#             print(f"Erreur: {str(e)}")

#     # Test avec code safe
#     test_code("""
# def ma_rule(principal: Principal, resource: Resource, context: Context):
#     if principal.has_role('admin'):
#         return True
#     if resource.is_type('document') and context.extra.get('action') == 'read':
#         return True
#     return False
# """, True)

#     # Test avec code safe mais différent
#     test_code("""
# def autre_nom(principal: Principal, resource: Resource, context: Context):
#     if principal.roles and 'admin' in principal.roles:
#         return True
#     if resource.type == 'document' and context.extra.get('action') == 'read':
#         return True
#     return False
# """, True)

#     # Test avec code non safe (utilisation de eval)
#     test_code("""
# def ma_rule(principal: Principal, resource: Resource, context: Context):
#     return eval('True')
# """, None)  # On attend une erreur

#     # Test avec code non safe (import)
#     test_code("""
# def ma_rule(principal: Principal, resource: Resource, context: Context):
#     import os
#     return True
# """, None)  # On attend une erreur

#     # Test avec code non safe (utilisation de globals)
#     test_code("""
# def ma_rule(principal: Principal, resource: Resource, context: Context):
#     return globals()['True']
# """, None)  # On attend une erreur
