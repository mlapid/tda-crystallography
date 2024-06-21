from collections import UserList

from Atom import Atom


class AtomList(UserList):

    def __contains__(self, atom: Atom) -> bool:
        for item in self:
            if atom == item:
                return True
        return False

    def append(self, atom: Atom) -> None:
        if not isinstance(atom, Atom):
            raise TypeError("AtomList can only append Atom objects")
        if atom not in self:
            super().append(atom)
        else:
            # print(f"{atom} is already in the list")
            return
