from abc import ABC, abstractmethod


class MOArchiveAbstract(ABC):
    @abstractmethod
    def add(self, f_vals, info=None):
        pass

    @abstractmethod
    def add_list(self, list_of_f_vals, infos=None):
        pass

    @abstractmethod
    def remove(self, f_vals):
        pass

    @abstractmethod
    def copy(self):
        pass

    @abstractmethod
    def infos(self):
        pass

    @abstractmethod
    def points(self):
        pass

    @abstractmethod
    def contributing_hypervolume(self, f_vals):
        pass

    @abstractmethod
    def distance_to_hypervolume_area(self, f_vals):
        pass

    @abstractmethod
    def distance_to_pareto_front(self, f_vals):
        pass

    @abstractmethod
    def hypervolume_improvement(self, f_vals):
        pass

    @abstractmethod
    def dominates(self, f_vals):
        pass

    @abstractmethod
    def dominators(self, f_vals):
        pass

    @abstractmethod
    def in_domain(self, f_vals):
        pass

    @property
    @abstractmethod
    def hypervolume(self):
        pass



