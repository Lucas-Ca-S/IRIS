import util.block_mounter as block_mounter
from abc import ABC, abstractmethod

class InitParameter(ABC):
    
    @abstractmethod
    def mount_first_parameter(self):
        pass

class InputInitParameter(InitParameter):

    def __init__(self, input_type:str, name:str, action_id:str) -> None:
        self.input_type = input_type
        self.name = name
        self.action_id = action_id

    def mount_first_parameter(self):
        return block_mounter.mount_input(self.name, self.input_type, self.action_id)

class SelectInitParameter(InitParameter):

    def __init__(self, name:str, action_id:str, options:list, type="static_select") -> None:
        self.name = name
        self.action_id = action_id
        self.options = options
        self.type = type

    def mount_first_parameter(self):
        return block_mounter.mount_select(self.name, self.options, self.action_id, self.type)
    
class MultiSelectInitParameter(SelectInitParameter):

    def __init__(self, name: str, action_id: str, options: list) -> None:
        super().__init__(name, action_id, options)

    def mount_first_parameter(self):
        return block_mounter.mount_select(self.name, self.options, self.action_id, "multi_static_select")