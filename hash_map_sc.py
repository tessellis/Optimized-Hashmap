# Name: Tess Ellis
# OSU Email: elliste@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 12/05/24
# Description: Min Heap Implementation - Linked lists and chaining 

# <-- Notes -->
# To accommodate multiple keys, linked lists can be used to store the individual keys that map to the same entry. The linked lists are commonly referred to as buckets or chains, and this technique of collision resolution is known as chaining. When a collision occurs, the new element is simply added to the collection at its corresponding hash index. Linked lists are a popular choice for maintaining the buckets.

# Inserting into a hash map with chaining collision resolution looks like:
#       Size: 5    Keys: {3, 6, 9}   Hash function: h(key) = key % 3
#       h(3) = 3 % 5 = 0    -->    Insert at 0      bucket 0: [3]
#       h(6) = 6 % 5 = 0    -->    Insert at 0      bucket 0: [3, 6]
#       h(9) = 9 % 5 = 0    -->    Insert at 0      bucket 0: [3, 6, 9]

#       
# We're just inserting at the end when colliding (much easier than open addressing I think). 
# 
# Remove would be the same but we would (drum roll please) remove a value after finding its bucket instead of adding a value :D

from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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

        Note: If the current load factor of the table is greater than or equal to 1.0, the table must be resized to double its current capacity
        """
        # check if our load factor
        if self.table_load() >= 1:
            # resize to double capacity if needed
            self.resize_table(self._capacity * 2)

        # calculate hash to get bucket index
        index = self._hash_function(key) % self._capacity

        # get bucket value is in
        bucket = self._buckets.get_at_index(index)

        # check if values need to be replaced
        node = bucket.contains(key)
        if node is not None:
            # replace if needed
            node.value = value
            return
        
        # add value to the bucket
        bucket.insert(key, value)
        # update our size
        self._size += 1



    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the underlying table. All existing key/value pairs must be put into the new table, meaning the hash table links must be rehashed

        Note: If new_capacity is 1 or more, make sure it is a prime number. If not, change it to the next highest prime number
        """
        # checking if capcity is not smaller 1 (invalid)
        if new_capacity < 1:
            return
        
        # store the old bucket data
        oldData = self._buckets

        # update capacity
        self._capacity = new_capacity
        # if value is already prime
        if not self._is_prime(new_capacity):
            # we don't update capacity
            self._capacity = self._next_prime(new_capacity)
        # clear buckets
        self.clear()

        # loop through old data
        for i in range(oldData.length()):
            for item in oldData.get_at_index(i):
                # reinsert into new data
                self.put(item.key, item.value)


    def table_load(self) -> float:
        """
        Returns the current hash table load factor

        Note: The load factor of a hash table is the average number of elements in each bucket: 𝝺=n/m (where 𝝺 Is the load factor, n is the total number of elements stored in the table, m is the number of buckets)
        """
        return self.get_size() / self.get_capacity()

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table
        """
        # initialize count
        count = 0
        # loop through buckets
        for i in range(self.get_capacity()):
            # if empty bucket found
            if self._buckets.get_at_index(i).length() == 0:
                # increase count
                count += 1

        return count

    def get(self, key: str):
        """
        Returns the value associated with the given key. If the key is not in the hash map, the method returns None

        Note: Similar to put but just not adding anything
        """
        # calculate hash to get bucket index
        index = self._hash_function(key) % self._capacity

        # find bucket
        bucket = self._buckets.get_at_index(index)

        # get value form bucket
        item = bucket.contains(key)

        # return value is exists and None if not
        if item is None:
            return None
        return item.value 

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, otherwise it returns False. An empty hash map does not contain any keys
        """
        # get value and return True if None
        return self.get(key) is not None

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map. If the key is not in the hash map, the method does nothing (no exception needs to be raised)

        Notes: Again, similar to put but removing instead of adding
        """
        # calculate hash to find bucket
        index = self._hash_function(key) % self._capacity

        # get bucket
        bucket = self._buckets.get_at_index(index)
        # remove if item exists
        if bucket.remove(key):
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a key/value pair stored in the hash map. The order of the keys in the dynamic array does not matter
        """
        keysAndValues = DynamicArray()

        # loop through buckets
        for i in range(self.get_capacity()):
            bucket = self._buckets.get_at_index(i)

            # loop through items in bucket
            for item in bucket:
                # append to array
                keysAndValues.append((item.key, item.value))

        # return array with keys and values
        return keysAndValues

    def clear(self) -> None:
        """
        Clears the contents of the hash map. It does not change the underlying hash table capacity
        """
        # reset bucket data (emtying)
        self._buckets = DynamicArray()
        # reset size to 0 (emptying)
        self._size = 0

        # resetting buckets
        for _ in range(self.get_capacity()):
            self._buckets.append(LinkedList())


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Return a tuple containing, in this order, a dynamic array comprising the mode (most frequently occurring) value(s) of the given array, and an integer representing the highest frequency of occurrence for the mode value(s).

    Note: If there is more than one value with the highest frequency, all values at that frequency should be included in the array being returned (the order does not matter). If there is only one mode, the dynamic array will only contain that value.

    Complexity: 0(N)
    """
    # using the instance of seperate chaining hashmap
    map = HashMap()

    # loop through dynamic array
    for i in range(da.length()):
        key = da.get_at_index(i)
        num = 1
        # if we find value
        if map.contains_key(key):
            # add to our count
            num = map.get(key) + 1
            # put key, num
        map.put(key, num)
    
    mode = DynamicArray()
    max = -1
    map_values = map.get_keys_and_values()

    # loop through mapped values
    for i in range(map_values.length()):
        item = map_values.get_at_index(i)
        # if new max is found
        if item[1] > max:
            mode = DynamicArray()
            # update max
            max = item[1]
        if item[1] == max:
            # append item
            mode.append(item[0])

    return mode, max


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
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

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
    m = HashMap(53, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
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

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
