import abc

class DataSaver(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def save(data):
        raise NotImplementedError('please define save() method in order to use this base class')