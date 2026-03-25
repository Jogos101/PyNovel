
class OperationFactory:
    def __init__(self, fluxo, operation):
        self.fluxo = fluxo
        self.operation = operation

    def get_fluxo(self):
        match self.operation:
            case 'CREATE':
                self.fluxo.create_epub()
            case 'UPDATE':
                self.fluxo.update_epub()
            case _:
                raise ValueError("Não foi possível identificar a operação.")