# Name: Timothy Birmingham
# OSU Email: birmingt@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment 6: HashMap
# Due Date: 6/6/2024
# Description: A separate chaining Hash Map implemented with a Dynamic Array, for each bucket, and a Linked List,
# at each bucket. The Hash Map has put, resize_table, table_load, empty_buckets, get, contains_key, remove,
# get_keys_and_values, and clear methods. The find_mode method is constructed outside the HashMap class.

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

    def put(self, key: str, value: object) -> None:
        """
        Adds or updates the passed key/value pair in the hash map. If the passed key is in the hash map, then
        the value associated with that key is updated. Otherwise, a new key/value pair is created.

        Note that when the load factor is >= 1.0 the table is resized to double its capacity rounded to the
        next closest prime integer value.

        :param key: The key the value will be associated with
        :param value: The value the key will be associated with
        """
        # Capture the load factor and test if the table needs to be resized
        load_factor = self.table_load()
        if load_factor >= 1.0:
            self.resize_table(self._capacity * 2)
        # Find the index to insert the key using the hash function
        key_hash = self._hash_function(key)
        key_index = key_hash % self._capacity
        # Check if the passed key is already in the hashmap. If so update that keys value.
        # Otherwise, insert the key at the hashed index and increment the size of the hash map.
        if self.contains_key(key):
            for linked_list_node in self._buckets[key_index]:
                if linked_list_node.key == key:
                    linked_list_node.value = value
        else:
            self._buckets.get_at_index(key_index).insert(key, value)
            self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the underlying dynamic array and rehashes the elements from the old DA into the
        new DA.

        :param new_capacity: The new capacity for the dynamic array. This will be rounded to the next highest
        prime integer.
        """
        # If the new capacity is less than 1, do nothing.
        if new_capacity < 1:
            return None
        # If not create a deep copy of the Hash Map's current Dynamic Array.
        temp_da = DynamicArray()
        for element in range(self._buckets.length()):
            temp_da.append(self._buckets[element])
        # Capture the old capacity and determine the new capacity. The capacity must be prime.
        old_capacity = self._capacity
        if self._is_prime(new_capacity):
            self._capacity = new_capacity
        else:
            self._capacity = self._next_prime(new_capacity)
        # Reset the Hash Map's dynamic array to the new capacity. Re-insert the elements from the original DA into
        # the newly sized DA using the put method.
        self.clear()
        for linked_list in range(old_capacity):
            if temp_da[linked_list].length() > 0:
                for current_node in temp_da[linked_list]:
                    self.put(current_node.key, current_node.value)

    def table_load(self) -> float:
        """
        Returns the current Hash Map's load factor as a float.

        :return: Current Hash Map's load factor as a float.
        """
        return self._size/self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the Hash Map as an integer.

        :return: The number of empty buckets
        """
        # Count how many buckets contain a linked list of length >= 1. Subtract the total number of used buckets
        # from the total number of available buckets and return.
        used_buckets = 0
        for element in range(self._buckets.length()):
            if self._buckets[element].length() >= 1:
                used_buckets += 1
        return self._buckets.length() - used_buckets

    def get(self, key: str):
        """
        Returns the value associated with the passed key. If the key is not in the Hash Map the method returns None.

        :param key: The key that will be searched for and whose associated value will be returned.

        :return: The value of the key or None if the key is not found.
        """
        # Determine the index associated with the key using the hash function.
        key_hash = self._hash_function(key)
        key_index = key_hash % self._buckets.length()
        # Iterate through the linked list at the key's bucket. If the key is found, return its value, otherwise
        # return None.
        for current_node in self._buckets[key_index]:
            if current_node.key == key:
                return current_node.value
        return None

    def contains_key(self, key: str) -> bool:
        """
        Searches the Hash Map for a given key and returns True if the key is found. Otherwise, it returns False.

        :param key: The key the method will search the Hash Map for

        :return: True if the key is found, otherwise false.
        """
        # Determine the index associated with the key using the hash function.
        key_hash = self._hash_function(key)
        key_index = key_hash % self._buckets.length()
        # If the bucket does not contain any linked lists with a size greater than 0, return False. Otherwise,
        # use the linked lists contains function to search the linked list for the key. Return True if found,
        # otherwise False.
        if self._buckets[key_index].length() < 1:
            return False
        if self._buckets[key_index].contains(key):
            return True
        return False

    def remove(self, key: str) -> None:
        """
        Removes the key and associated value from the Hash Map. If the key is not in the Hash Map, the
        method does nothing.

        :param key: The key to be removed
        """
        # Determine the index associated with the key using the hash function. Iterate through the linked list at that
        # index. If the key is found, remove the key and reduce the size of the Hash Map by 1.
        key_hash = self._hash_function(key)
        key_index = key_hash % (self._buckets.length())
        for current_node in self._buckets[key_index]:
            if current_node.key == key:
                removed = self._buckets[key_index].remove(key)
                if removed:
                    self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        In no particular order, this method returns all key/value pairs as tuples in a Dynamic Array.

        :return: A Dynamic Array containing all key/value pairs as tuples.
        """
        # Create a dynamic array to store the tuples. Iterate through the Hash Map, if the bucket contains a linked
        # list with a size > 0, iterate through the linked lists adding the key value pairs as tuples.
        key_value_da = DynamicArray()
        for linked_list in range(self._capacity):
            if self._buckets[linked_list].length() > 0:
                for current_node in self._buckets[linked_list]:
                    append_tuple = (current_node.key, current_node.value)
                    key_value_da.append(append_tuple)
        return key_value_da

    def clear(self) -> None:
        """
        Clears the contents of the Hash Map while maintaining the Hash Map's capacity. Resets the Hash Map's
        size to 0.
        """
        # Set buckets to a new blank Dynamic Array. Append new linked lists into the DA to meet the existing capacity.
        # Update the Hash Map's size to 0.
        self._buckets = DynamicArray()
        for linked_list in range(self._capacity):
            self._buckets.append(LinkedList())
        self._size = 0


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Find_mode is passed a dynamic array and returns a tuple containing a dynamic array with the mode/s and
    its/their frequency.

    :param da: The dynamic array whose mode will be determined.
    :return: A tuple containing a Dynamic Array with all mode keys and an integer of their frequency.
    """
    # Build a hash map out of the provided DA. If the key is already in the Hash Map, increment its frequency by 1.
    map = HashMap()
    for element in range(da.length()):
        if map.contains_key(da[element]):
            map.put(da[element], map.get(da[element]) + 1)
        else:
            map.put(da[element], 1)
    # Capture the key/value pairs in the Hash Map. Create a DA for the key's that are the mode and set the current
    # mode counter to 0.
    keys_values_da = map.get_keys_and_values()
    mode_da = DynamicArray()
    current_mode = 0
    # Iterate through the key/value pairs. If the key's frequency is > than the current mode, it is now the new mode.
    # If the key's frequency is == to the mode, add it to the mode DA. Otherwise, continue to the next element.
    for element in range(keys_values_da.length()):
        if keys_values_da[element][1] > current_mode:
            mode_da = DynamicArray()
            mode_da.append(keys_values_da[element][0])
            current_mode = keys_values_da[element][1]
        elif keys_values_da[element][1] == current_mode:
            mode_da.append(keys_values_da[element][0])
    return mode_da, current_mode

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

    print("\nPDF - GRADESCOPE")
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    m = HashMap(10, hash_function_1)
    insert_list = [(614, 766), (463, 498), (157, 600), (310, 767), (763, 635), (396, -672), (378, -892), (47, -196),
                   (341, 566), (739, 579), (541, -185), (363, -70)]
    for i in insert_list:
        m.put('key' + str(i[0]), i[1])
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
