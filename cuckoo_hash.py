# explanations for member functions are provided in requirements.py
# each file that uses a cuckoo hash should import it from this file.
import random as rand
from typing import List


class CuckooHash:
    def __init__(self, init_size: int):
        self.__num_rehashes = 0
        self.CYCLE_THRESHOLD = 10

        self.table_size = init_size
        self.tables = [[None] * init_size for _ in range(2)]

    def hash_func(self, key: int, table_id: int) -> int:
        key = int(str(key) + str(self.__num_rehashes) + str(table_id))
        rand.seed(key)
        return rand.randint(0, self.table_size - 1)

    def get_table_contents(self) -> List[List[int]]:
        return self.tables

    # you should *NOT* change any of the existing code above this line
    # you may however define additional instance variables inside the __init__ method.

    def insert(self, key: int) -> bool:

        t = 0
        count = 0
        v = self.hash_func(key, t)

        if self.lookup(key):  # if lookup returns true - key already in the table.
            return False

        while count <= self.CYCLE_THRESHOLD:  # keep going till reaches cycle threshhold, then it breaks out and rehash
            temp = self.tables[t][v]  # saving what's already in there in a temp variable
            self.tables[t][v] = key  # kicking it out and replacing with new key.
            if temp == None:  # checking if there was nothing - we are done inserting
                return True
            t = 1 - t  # changes tables from 0 to 1
            count += 1  # keeps count of cyles to compare to CYCLE_COUNT
            key = temp  # resets key variable for next iteration
            v = self.hash_func(key, t)  # hash the new key
        print("We in a cycle")
        return False


    def lookup(self, key: int) -> bool:
        # Look in both places: H0[h0(k)], H1[h1(k)]
        for t in range(2):
            loc = self.hash_func(key, t)  # gets index of key for tables

            if self.tables[t][loc] == key:
                return True
            else:
                # print(key, " is in our table!")
                return False

    def delete(self, key: int) -> None:
        # Look in both places, clear if found.
        # basically using same code as insert, but when found delete it by replacing it with None.

        for t in range(2):
            loc = self.hash_func(key, t)  # gets index of key for tables

            if self.tables[t][loc] == key:
                self.tables[t][loc] = None
                print(key, " has been deleted!")
            else:
                print(key, " is not in our table!")

    def rehash(self, new_table_size: int) -> None:
        old_table_size = self.table_size
        self.__num_rehashes += 1; self.table_size = new_table_size  # do not modify this line
        temp_table = []

        for t in range(2):                          #copy elements to new tabling by using new hash
            for i in range(old_table_size):
                key = self.tables[t][i]   #out of index fix - use old table size.
                if key == None:
                    continue
                else:
                    temp_table.append(key)
        #print(temp_table)

        self.tables = [[None] * new_table_size  for _ in range(2)]
        for i in range(len(temp_table)):
            key = temp_table[i]
            self.insert(key)

# feel free to define new methods in addition to the above
# fill in the definitions of each required member function (above),
# and for any additional member functions you define
#
# hash_table = CuckooHash(10)
#
# for i in range(30):
#     hash_table.insert(i)
# hash_table.rehash(250)
#
#
# # print(hash_table.lookup(13))
# print(hash_table.get_table_contents())
# # hash_table.delete(10)
# # print(hash_table.get_table_contents())



