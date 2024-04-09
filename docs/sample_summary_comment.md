<details><summary>Mutation Test Result　　🎉 8　　⏰ 0　　🤔 0　　🙁 4　　🔇 12</summary>

<br>

Legend for output:
🎉 Killed mutants.   The goal is for everything to end up in this bucket.
⏰ Timeout.          Test suite took 10 times as long as the baseline so were killed.
🤔 Suspicious.       Tests took a long time, but not long enough to be fatal.
🙁 Survived.         This means your tests need to be expanded.
🔇 Skipped.          Skipped.


<table border="1"><tr><th>File</th><th>🎉 Killed</th><th>🙁 Survived</th><th>% killed/(killed + survived)</th></tr><tr><td>pipenv-project/src/calculator.py</td><td>0</td><td>0</td><td>-</td></tr><tr><td>pipenv-project/src/domain/book.py</td><td>2</td><td>0</td><td>100.00</td></tr><tr><td>pipenv-project/src/fizz_buzz.py</td><td>6</td><td>4</td><td>60.00</td></tr></table>

<details><summary>List of tests used for mutation</summary>

- pipenv-project/tests/test_calculator.py
- pipenv-project/tests/model/test_book.py
- pipenv-project/tests/test_fizz_buzz.py
</details>


<br>
※ 🙁 Survived, ⏰Timeout, 🤔Suspicious are shown below.

<details><summary>pipenv-project/src/fizz_buzz.py</summary>

## Survived
Survived mutation testing. These mutants show holes in your test suite.
### Line number:2
```python
@@ -1,5 +1,5 @@
 def fizz_buzz(n):
-    if n % 15 == 0:  #
+    if n / 15 == 0:  #
         return "fizz buzz"  #
 
     if n % 3 == 0:
```
### Line number:2
```python
@@ -1,5 +1,5 @@
 def fizz_buzz(n):
-    if n % 15 == 0:  #
+    if n % 16 == 0:  #
         return "fizz buzz"  #
 
     if n % 3 == 0:
```
### Line number:2
```python
@@ -1,5 +1,5 @@
 def fizz_buzz(n):
-    if n % 15 == 0:  #
+    if n % 15 == 1:  #
         return "fizz buzz"  #
 
     if n % 3 == 0:
```
### Line number:3
```python
@@ -1,6 +1,6 @@
 def fizz_buzz(n):
     if n % 15 == 0:  #
-        return "fizz buzz"  #
+        return "XXfizz buzzXX"  #
 
     if n % 3 == 0:
         return "fizz"
```
</details>

</details>