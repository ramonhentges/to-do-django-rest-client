from cerberus import Validator as CerberusValidator, TypeDefinition
import todo.domain.models.list as list
import re

emailRegex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


class Validator(CerberusValidator):
    def _validate_is_odd(self, constraint, field, value):
        if constraint is True and not bool(value & 1):
            self._error(field, "Must be an odd number")

    def _validate_is_email(self, constraint, field, value):
        if constraint == 'required' or value != "":
            if re.fullmatch(emailRegex, value) is None:
                self._error(field, "Must be an email")


list_type = TypeDefinition('list', (list.ListModel,), ())

Validator.types_mapping['list'] = list_type
