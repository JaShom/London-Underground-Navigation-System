# London Underground Navigation System
### Coursework Version
Previously known as Journey Planner Model, the London Underground Navigation system is an application built to find the shortest path based on the London Undergound Data.xlsx file.\
Utilises Doubly Linked List and Dijkstra's Algorithm due to university coursework requirements.\
A larger dataset will make the run time slow as its **O(n<sup>2</sup>)**.
###### Requirements (with libraries):
-  Python 3x
    - pandas - 2.0.1
    - rest of the libraries are in-built, just install them if they aren't present

### Improved Version
Same as the coursework version, however, it is faster. Doubly Linked List was replaced with a HashMap, allowing a **O(1)** search. Reducing the runtime of the entire algorithm to **O(n \* log n).**\
Requirements remain the same.
###### Changes:
+  Title: ~~London Underground Route Planner~~ -> *"London Underground Navigation System"*
+  Data Structure: ~~Doubly Linked List~~ -> *HashMaps*
+  New class added for possible new features
