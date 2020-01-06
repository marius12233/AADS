# Copyright 2013, Michael H. Goldwasser
#
# Developed for use with the book:
#
#    Data Structures and Algorithms in Python
#    Michael T. Goodrich, Roberto Tamassia, and Michael H. Goldwasser
#    John Wiley & Sons, 2013
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from .doubly_linked_base import _DoublyLinkedBase

class PositionalList(_DoublyLinkedBase):
  """A sequential container of elements allowing positional access."""

  #-------------------------- nested Position class --------------------------
  class Position:
    """An abstraction representing the location of a single element.

    Note that two position instaces may represent the same inherent
    location in the list.  Therefore, users should always rely on
    syntax 'p == q' rather than 'p is q' when testing equivalence of
    positions.
    """

    def __init__(self, container, node):
      """Constructor should not be invoked by user."""
      self._container = container
      self._node = node

    def element(self):
      """Return the element stored at this Position."""
      return self._node._element

    def __eq__(self, other):
      """Return True if other is a Position representing the same location."""
      return type(other) is type(self) and other._node is self._node

    def __ne__(self, other):
      """Return True if other does not represent the same location."""
      return not (self == other)               # opposite of __eq__

  #------------------------------- utility methods -------------------------------
  def _validate(self, p):
    """Return position's node, or raise appropriate error if invalid."""
    if not isinstance(p, self.Position):
      raise TypeError('p must be proper Position type else is', type(p))
    if p._container is not self:
      #raise ValueError('p does not belong to this container')
      pass
    if p._node._next is None:                  # convention for deprecated nodes
      raise ValueError('p is no longer valid')
    return p._node

  def _make_position(self, node):
    """Return Position instance for given node (or None if sentinel)."""
    if node is self._header or node is self._trailer:
      return None                              # boundary violation
    else:
      return self.Position(self, node)         # legitimate position

  #------------------------------- accessors -------------------------------
  def first(self):
    """Return the first Position in the list (or None if list is empty)."""
    return self._make_position(self._header._next)

  def last(self):
    """Return the last Position in the list (or None if list is empty)."""
    return self._make_position(self._trailer._prev)

  def before(self, p):
    """Return the Position just before Position p (or None if p is first)."""
    node = self._validate(p)
    return self._make_position(node._prev)

  def after(self, p):
    """Return the Position just after Position p (or None if p is last)."""
    node = self._validate(p)
    return self._make_position(node._next)

  def __iter__(self):
    """Generate a forward iteration of the elements of the list."""
    cursor = self.first()
    while cursor is not None:
      yield cursor
      cursor = self.after(cursor)

  #------------------------------- mutators -------------------------------
  # override inherited version to return Position, rather than Node
  def _insert_between(self, e, predecessor, successor,parent=None):
    """Add element between existing nodes and return new Position."""
    node = super()._insert_between(e, predecessor, successor,parent)
    return self._make_position(node)

  def add_first(self, e):
    """Insert element e at the front of the list and return new Position."""
    return self._insert_between(e, self._header, self._header._next)

  def add_last(self, e):
    """Insert element e at the back of the list and return new Position."""
    return self._insert_between(e, self._trailer._prev, self._trailer)

  def add_before(self, parent, p, e):
    """Insert element e into list before Position p and return new Position."""
    original = self._validate(p)
    print('Chiamata per: ')
    print(parent.key())
    return self._insert_between(e, original._prev, original, parent)

  def add_after(self, parent, p, e):
    """Insert element e into list after Position p and return new Position."""
    original = self._validate(p)
    return self._insert_between(e, original, original._next, parent)

  def delete(self, p):
    """Remove and return the element at Position p."""
    original = self._validate(p)
    return self._delete_node(original)  # inherited method returns element

  def replace(self, p, e):
    """Replace the element at Position p with e.

    Return the element formerly at Position p.
    """
    original = self._validate(p)
    old_value = original._element       # temporarily store old element
    original._element = e               # replace with new element
    return old_value                    # return the old element value

  def _computeMedianAdd(self,leaf,node):
    super()._computeMedianAdd(leaf,node)

  def _computeMedianRemove(self,leaf):
    super()._computeMedianRemove(leaf)

#splitto la lista in modo da ottenere due liste, di cui la prima ha head=head della lista e la seconda ha head=mediano per eccesso
#sappiamo che l'overflow lo otteniamo per una lista pari perchè b è dispari ed è uguale a 7
  def splitMedian(self):

    l1=PositionalList()
    l2=PositionalList()

    l1._size=self._size//2
    l1._header._next=self._header._next
    l1._trailer._prev=self._median._prev
    self._header._next._prev = l1._header
    self._median._prev._next = l1._trailer
    l1._median=l1._trailer._prev._prev
    l1._medianKey=l1._median._parent.key()

    l2._size=self._size//2
    l2._header._next=self._median
    l2._trailer._prev=self._trailer._prev
    self._median._prev = l2._header
    self._trailer._prev._next = l2._trailer
    l2._median=l2._trailer._prev._prev
    l2._medianKey=l2._median._parent.key()

    return l1,l2


if __name__=="__main__":
  l = PositionalList()
