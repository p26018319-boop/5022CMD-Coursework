"""
hash_table.py
A generic hash table using OPEN ADDRESSING with LINEAR PROBING.

The table knows nothing about pharmacies. It stores any (key, value) pair,
so it can be reused in other programs (abstraction / reusability).
"""

# Possible states of a slot
EMPTY = 0       # never used; a probe sequence can stop here
OCCUPIED = 1    # holds a live key/value pair
DELETED = 2     # "tombstone": used to hold a pair that was removed


class Slot:
    """One slot (bucket) of the hash table."""

    __slots__ = ("key", "value", "state")

    def __init__(self):
        self.key = None
        self.value = None
        self.state = EMPTY


class HashTable:
    """Hash table with open addressing and linear probing.

    Probe sequence for a key:  (h(key) + i) mod capacity,  i = 0, 1, 2, ...
    """

    def __init__(self, capacity=53):
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        self.capacity = capacity
        self.size = 0                                   # number of live items
        self.slots = [Slot() for _ in range(capacity)]

    # ---------------------------------------------------------- hash function
    def _hash(self, key):
        """Map a key to a starting slot index.

        int keys   -> key mod capacity
        other keys -> polynomial rolling hash of str(key). Python's built-in
                      hash() is randomised per run for strings, so it is not
                      used; this keeps results repeatable.
        """
        if isinstance(key, int):
            return key % self.capacity
        h = 0
        for ch in str(key):
            h = (h * 31 + ord(ch)) % self.capacity
        return h

    # ---------------------------------------------------------------- insert
    def insert(self, key, value):
        """Insert or update a pair. Returns the slot index used.

        Raises OverflowError if the table is full.
        """
        start = self._hash(key)
        first_free = None                      # first reusable (deleted) slot
        for i in range(self.capacity):
            idx = (start + i) % self.capacity  # linear probing
            slot = self.slots[idx]
            if slot.state == OCCUPIED:
                if slot.key == key:            # key exists -> update value
                    slot.value = value
                    return idx
            elif slot.state == DELETED:
                if first_free is None:
                    first_free = idx           # remember, but keep looking
            else:                              # EMPTY: key is definitely absent
                target = first_free if first_free is not None else idx
                self._place(target, key, value)
                return target
        # Probed the entire table without meeting an EMPTY slot
        if first_free is not None:
            self._place(first_free, key, value)
            return first_free
        raise OverflowError("Hash table is full")

    def _place(self, idx, key, value):
        slot = self.slots[idx]
        slot.key, slot.value, slot.state = key, value, OCCUPIED
        self.size += 1

    # ---------------------------------------------------------------- search
    def _find_index(self, key):
        """Return the slot index holding key, or -1 if absent."""
        start = self._hash(key)
        for i in range(self.capacity):
            idx = (start + i) % self.capacity
            slot = self.slots[idx]
            if slot.state == EMPTY:            # chain ends -> not present
                return -1
            if slot.state == OCCUPIED and slot.key == key:
                return idx                     # skip DELETED, keep probing
        return -1

    def search(self, key):
        """Return the value for key, or None if not found."""
        idx = self._find_index(key)
        return None if idx == -1 else self.slots[idx].value

    def slot_of(self, key):
        """Return the slot index of key (or -1). Useful for display/debugging."""
        return self._find_index(key)

    # ---------------------------------------------------------------- delete
    def delete(self, key):
        """Remove key. Returns True if removed, False if it was not present."""
        idx = self._find_index(key)
        if idx == -1:
            return False
        slot = self.slots[idx]
        slot.key, slot.value, slot.state = None, None, DELETED  # tombstone
        self.size -= 1
        return True

    # ------------------------------------------------------------- utilities
    def is_full(self):
        return self.size >= self.capacity

    def load_factor(self):
        return self.size / self.capacity

    def __len__(self):
        return self.size

    def items(self):
        """Yield every live (key, value) pair."""
        for slot in self.slots:
            if slot.state == OCCUPIED:
                yield slot.key, slot.value
