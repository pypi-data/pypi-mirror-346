# TODO We might rename it to GenericCrud

from abc import ABC, abstractmethod

DEFAULT_SQL_SELECT_LIMIT = 100


class GenericCrudAbstract(ABC):

    # @property
    # @abstractmethod
    # def version(self):
    #     pass  # Abstract property, must be implemented by subclasses

    @abstractmethod
    def insert(self, *, schema_name: str = None, table_name: str = None,
               data_dict: dict = None,
               ignore_duplicate: bool = False, commit_changes: bool = True
               ) -> int:
        pass
