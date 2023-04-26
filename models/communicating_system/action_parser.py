from z3 import Int, Bool, String, Real
from models.communicating_system.action import Action


class ActionParser:

    def parse(self, action_string):
        communication, message = self._split_action(action_string)
        sender, receiver = self._parse_communication(communication)
        tag, payload = self._parse_message(message)

        message = Action.Message(tag, payload)
        return Action(sender, receiver, message)

    def _split_action(self, action_string):
        participants, message = action_string.split(':')
        return participants.strip(), message.strip()

    # Asumimos que los participants son representados SOLOS con un char. Ej:'wv!', 'pq?'
    def _parse_communication(self, communication):
        sender, receiver = communication.split('->')
        return sender.strip(), receiver.strip()

    def _parse_message(self, message):
        open_payload_index = message.find('(')
        end_payload_index = message.find(')')

        tag = message[0:open_payload_index]
        payload_string = message[open_payload_index+1:end_payload_index]
        payload = []
        if payload_string != '':
            payload = [self._parse_variable(variable_string) for variable_string in payload_string.split(',')]

        return tag, payload

    def _parse_variable(self, variable_string):
        variable_string = variable_string.strip()
        sort, name = variable_string.split(' ')

        if sort == 'int':
            return Int(name)
        elif sort == 'bool':
            return Bool(name)
        elif sort == 'string':
            return String(name)
