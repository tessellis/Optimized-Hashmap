# Name: Tess Ellis
# OSU Email: elliste@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 12/05/24
# Description: HashMap Implementation - Open addressing and probing

# <-- Notes -->
# The open addressing method for resolving collisions involves probing for an empty spot in the hash table array if a collision occurs. When using open addressing, all hashed elements are stored directly in the hash table array. The procedure for inserting an element in an open addressing-based hash table looks like this:

# Use the hash function to compute an initial index iinitial for the element.
# If the hash table array at index iinitial is empty, insert the element there and stop.
# Otherwise, compute the next index i in the probing sequence and repeat.

# This process of searching for an empty position is called probing. For this project, we're using Quadratic Probing:
# Quadratic probing:  i = iinitial + j^(2)             (where j = 1, 2, 3, …)

#       Size: 7    Keys: {10, 20, 30, 23}    Hash function: h(key) = key % 3
#       h(10) = 10 % 7 = 3    -->    Bucket is empty so   -->   Insert at 3   -->  bucket 3: [10]
#       h(20) = 20 % 7 = 6    -->    Bucket is empty so   -->   Insert at 6   -->  bucket 6: [20]
#       h(30) = 30 % 7 = 2    -->    Bucket is empty so   -->   Insert at 2   -->  bucket 7: [30]
#       h(23) = 23 % 7 = 2    -->    Bucket is NOT empty so  -->   Apply quadratic probing:
#       h(23) + 1^2 % 7 = 3   -->    Bucket is NOT empty so  -->   Continue:
#       h(23) + 2^2 % 7 = 6   -->    Bucket is NOT empty so  -->   Continue: 
#       h(23) + 3^2 % 7 = 4   -->    Bucket is empty so   -->   Insert at 4   -->  bucket 4: [23]
#


from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    # ALL METHODS should be kept in 0(1) runtime complexity

    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in the hash map. If the given key already exists in the hash map, its associated value must be replaced with the new value. If the given key is not in the hash map, a new key/value pair must be added

        Notes: If the current load factor of the table is greater than or equal to 0.5, the table must be resized to double its current capacity
        """
        # if table load is greater than half double table size
        if self.table_load() >= 0.5:
            # doube capacity
            self.resize_table(self.get_capacity() * 2)
        
        # get the key's hash and set step to 0
        hash = self._hash_function(key) % self.get_capacity()
        step = 0

        # loop through all buckets
        for step in range(self.get_capacity()):

            #  i = iinitial + j^(2)
            # calculate index with quadratic probing
            index = (hash + step * step) % self.get_capacity()
            
            # if we find an empty spot or a spot with a deleted value (is_tombstone)
            item = self._buckets.get_at_index(index)
            if item is None or \
                item.is_tombstone:
                # set the value at that spot to the item and increment the size
                self._buckets.set_at_index(index, HashEntry(key, value))
                self._size += 1
                return
            # else if same key is found update the value
            elif item.key == key:
                item.value = value
                return

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the underlying table. All active key/value pairs must be put into the new table, meaning all non-tombstone hash table links must be rehashed

        Notes: It should do nothing if new_capacity is not less than the current number of elements in the hash map. If new_capacity is valid, make sure it is a prime number; if not, change it to the next highest prime number
        """
        # checking if capcity is not smaller than current size (invalid)
        if new_capacity < self.get_size():
            return
        
        # store old bucket data
        oldData = self._buckets

        # update capacity and clear buckets
        self._capacity = new_capacity
        if not self._is_prime(new_capacity):
            self._capacity = self._next_prime(new_capacity)
        self.clear()

        # loop through old data and reinsert into new data
        for i in range(oldData.length()):
            item = oldData.get_at_index(i)
            if item is not None and not item.is_tombstone:
                self.put(item.key, item.value)

                

    def table_load(self) -> float:
        """
        Returns the current hash table load factor
        """
        # table laod = total num of elements / buckets
        return self.get_size() / self.get_capacity()

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table
        """
        count = 0
        # loop through buckets
        for i in range(self.get_capacity()):
            # if empty bucket found
            if self._buckets.get_at_index(i) is None:
                # increase count
                count += 1
        
        return count

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key. If the key is not in the hash map, the method returns None
        """
        # calculate hash
        hash = self._hash_function(key) % self.get_capacity()
        step = 0

        # loop through buckets
        for step in range(self.get_capacity()):
            # calculate index with quadratic probing
            index = (hash + step * step) % self.get_capacity()
            # get item index
            item = self._buckets.get_at_index(index)
            # return None if not found
            if item is None:
                return None
            # if key is found and item is not dead
            elif item.key == key and not item.is_tombstone:
                # return value associated with key
                return item.value

    def contains_key(self, key: str) -> bool:
        """
        returns True if the given key is in the hash map, otherwise it returns False. An empty hash map does not contain any keys
        """
        # get value and return True if None
        return self.get(key) is not None

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map. If the key is not in the hash map, the method does nothing (no exception needs to be raised)

        Notes: Same process as put but removing instead of putting
        """
        # calculate hash
        hash = self._hash_function(key) % self.get_capacity()
        step = 0

        # loop through buckets
        for step in range(self.get_capacity()):
            # calculate index with quadratic probing
            index = (hash + step * step) % self.get_capacity()
            # get item index
            item = self._buckets.get_at_index(index)
             # return None if not found
            if item is None:
                return
            # if key is found update size and "kill" the value/key
            elif item.key == key:
                self._size -= 1
                item.is_tombstone = True
                return

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a key/value pair stored in the hash map. The order of the keys in the dynamic array does not matter
        """
        keyValues = DynamicArray()
        # loop through buckets
        for i in range(self._capacity):
            # loop through items in bucket
            item = self._buckets.get_at_index(i)
            # if item exists and is not dead
            if item is not None and not item.is_tombstone:
                # add to our dyncamic array
                keyValues.append((item.key, item.value))
        return keyValues

    def clear(self) -> None:
        """
        Clears the contents of the hash map. It does not change the underlying hash table capacity
        """
        # reset bucket data (emptying)
        self._buckets = DynamicArray()
        # reset size
        self._size = 0
        # set bucket contents to None
        for _ in range(self._capacity):
            self._buckets.append(None)

    def __iter__(self):
        """
        Enables the hash map to iterate across itself (similiar to Encapsulation and Iterators exploration)
        """
        # initialize iter value
        self._iterVal = 0
        return self

    def __next__(self):
        """
        Return the next item in the hash map, based on the current location of the iterator

        Note: Only needs to iterate over active items
        """
        # if we've iterated to the end of the map
        if self._iterVal >= self._capacity:
            # stop
            raise StopIteration
        
        # while were still in the map
        while self._iterVal < self.get_capacity():
            # iterate through map
            item = self._buckets.get_at_index(self._iterVal)
            self._iterVal += 1
            # if next item exists and is not dead (only active items)
            if item is not None and not item.is_tombstone:
                # return the next item in map
                return item
        # stop when we've iterated through completely
        raise StopIteration


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - remove example 2")
    print("----------------------")
    m = HashMap(107, hash_function_1)
    keys = [
        ["key31", -971],
        ["key38", -500],
        ["key59", -567],
        ["key96", 348],
        ["key103", 16],
        ["key130", -922],
        ["key411", -576],
        ["key304", 39],
        ["key404", -597],
        ["key308", 229],
        ["key147", -756],
        ["key562", -131],
        ["key166", -356],
        ["key924", 669],
        ["key718", -13],
        ["key6", -425],
        ["key782", -375],
        ["key774", -424],
        ["key559", -564],
        ["key809", -158],
        ["key864", -841],
        ["key527", -148],
        ["key564", 309],
        ["key786", -727],
        ["key836", -889],
        ["key891", 754],
        ["key930", 402],
        ["key929", 748],
        ["key707", -511],
        ["key835", 291],
        ["key936", 266],
        ["key732", 464]
    ]

    for key in keys:
        m.put(key[0], key[1])

    print("Capacity:", m.get_capacity(), "Size:", m.get_size())
    print(m)

    m.remove("key562")
    print("Capacity:", m.get_capacity(), "Size:", m.get_size())
    print(m)

    m.remove("key924")
    print("Capacity:", m.get_capacity(), "Size:", m.get_size())
    print(m)

    m.remove("key6")
    print("Capacity:", m.get_capacity(), "Size:", m.get_size())
    print(m)

    m.remove("key147")
    print("Capacity:", m.get_capacity(), "Size:", m.get_size())
    print(m)

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
