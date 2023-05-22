# Journey-Planner-Model
### Coursework Version
Journey Planner Model application for the London Underground System made based of the London Undergound Data.xlsx file.\
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
