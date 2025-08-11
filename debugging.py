# debugging.py
import inspect, data_structures.linked_list as llmod, io, os

print("MODULE FILE:", llmod.__file__)
with open(llmod.__file__, "r", encoding="utf-8") as f:
    src = f.read()
print("\n=== FILE START ===\n")
print(src[:2000])            # first 2000 chars
print("\n=== FILE END ===")
print("\nContains 'def search('? ->", 'def search(' in src)
print("Count 'class linkedList':", src.count('class linkedList'))
print("Any reassignments 'linkedList ='? ->", 'linkedList =' in src)
