"""Lab 2 / Task 3: simple model-based classroom energy agent."""
class RoomController:
    def __init__(self):
        self.last_command = None

    def decide(self, temperature, occupied):
        if not isinstance(temperature, (int, float)):
            raise TypeError('Temperature must be numeric')
        if not occupied:
            desired = 'ECO'
        elif temperature > 26:
            desired = 'COOL'
        elif temperature < 20:
            desired = 'WARM'
        else:
            desired = 'IDLE'
        changed = desired != self.last_command
        self.last_command = desired
        return desired, ('SEND' if changed else 'NO COMMAND')

if __name__ == '__main__':
    readings = [(28,True),(28,True),(26,True),(20,True),(18,True),(24,False),(24,False),(27,True)]
    agent = RoomController()
    for index, (temp, present) in enumerate(readings, start=1):
        mode, action = agent.decide(temp, present)
        print(f'{index}: temp={temp}, occupied={present}, mode={mode}, action={action}')
    assert RoomController().decide(26, True)[0] == 'IDLE'
