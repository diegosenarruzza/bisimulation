from z3 import Int, Bool, String, Real
from ..communicating_system.action import Action
import re

pattern = r'(?P<participant1>[A-Z][a-z0-9]*)\s*'\
          r'(?P<participant2>[A-Z][a-z0-9]*)\s*'\
          r'(?P<action>!|\?)\s*'\
          r'(?P<tag>\w+)\((?P<payload>.*)\)'


class ActionParser:

    def parse(self, action_string):
        match = re.match(pattern, action_string)

        if match:
            match = match.groupdict()
        else:
            raise Exception(f'Wrong action: {action_string}')

        payload = self._parse_payload(match['payload'])

        message = Action.Message(match['tag'], payload)

        return Action(match['participant1'], match['participant2'], match['action'], message)

    def _parse_payload(self, payload_string):
        if payload_string == '':
            return []

        payload = [re.split(r'\s+', var.strip()) for var in payload_string.split(',')]
        return [self._parse_variable(var[0], var[1]) for var in payload]

    def _parse_variable(self, sort, name):
        if sort == 'int':
            return Int(name)
        elif sort == 'bool':
            return Bool(name)
        elif sort == 'string':
            return String(name)

