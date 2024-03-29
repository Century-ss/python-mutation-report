<details><summary>Mutation Test Result　　🎉 11　　⏰ 0　　🤔 0　　🙁 7　　🔇 0</summary>

<br>

Legend for output:
🎉 Killed mutants.   The goal is for everything to end up in this bucket.
⏰ Timeout.          Test suite took 10 times as long as the baseline so were killed.
🤔 Suspicious.       Tests took a long time, but not long enough to be fatal.
🙁 Survived.         This means your tests need to be expanded.
🔇 Skipped.          Skipped.


<h1>Mutation testing report</h1>Killed 11 out of 18 mutants<table><thead><tr><th>File</th><th>Total</th><th>Killed</th><th>% killed</th><th>Survived</th></tr></thead><tr><td>backend/pipenv-project/src/domain/book.py</td><td>3</td><td>0</td><td>0.00</td><td>3</td><tr><td>backend/pipenv-project/src/fizz_buzz.py</td><td>15</td><td>11</td><td>73.33</td><td>4</td></tr></tr></table>

<details><summary>List of test used for mutation</summary>

- backend/pipenv-project/tests/model/test_book.py
- backend/pipenv-project/tests/test_fizz_buzz.py
</details>

※ ⏰Timeout, 🤔Suspicious and 🔇Skipped are not shown in the table.
<br>
※ 🔇Skipped are not shown in the list of mutants

<details><summary>backend/pipenv-project/src/domain/book.py</summary>

Killed 0 out of 3 mutants
## Survived
Survived mutation testing. These mutants show holes in your test suite.
### Line number:3
```
--- backend/pipenv-project/src/domain/book.py
+++ backend/pipenv-project/src/domain/book.py
@@ -1,6 +1,6 @@
 class Book:
     def __init__(self, title: str, author: str) -> None:
-        self.title = title
+        self.title = None
         self.author = author
 
     def get_info(self) -> str:
```
### Line number:4
```
--- backend/pipenv-project/src/domain/book.py
+++ backend/pipenv-project/src/domain/book.py
@@ -1,7 +1,7 @@
 class Book:
     def __init__(self, title: str, author: str) -> None:
         self.title = title
-        self.author = author
+        self.author = None
 
     def get_info(self) -> str:
         return f"{self.title} by {self.author}"
```
### Line number:7
```
--- backend/pipenv-project/src/domain/book.py
+++ backend/pipenv-project/src/domain/book.py
@@ -4,7 +4,7 @@
         self.author = author
 
     def get_info(self) -> str:
-        return f"{self.title} by {self.author}"
+        return f"XX{self.title} by {self.author}XX"
 
 
 ###
```
</details>

<details><summary>backend/pipenv-project/src/fizz_buzz.py</summary>

Killed 11 out of 15 mutants
## Survived
Survived mutation testing. These mutants show holes in your test suite.
### Line number:2
```
--- backend/pipenv-project/src/fizz_buzz.py
+++ backend/pipenv-project/src/fizz_buzz.py
@@ -1,5 +1,5 @@
 def fizz_buzz(n):
-    if n % 15 == 0:
+    if n / 15 == 0:
         return "fizz buzz"
 
     if n % 3 == 0:
```
### Line number:2
```
--- backend/pipenv-project/src/fizz_buzz.py
+++ backend/pipenv-project/src/fizz_buzz.py
@@ -1,5 +1,5 @@
 def fizz_buzz(n):
-    if n % 15 == 0:
+    if n % 16 == 0:
         return "fizz buzz"
 
     if n % 3 == 0:
```
### Line number:2
```
--- backend/pipenv-project/src/fizz_buzz.py
+++ backend/pipenv-project/src/fizz_buzz.py
@@ -1,5 +1,5 @@
 def fizz_buzz(n):
-    if n % 15 == 0:
+    if n % 15 == 1:
         return "fizz buzz"
 
     if n % 3 == 0:
```
### Line number:3
```
--- backend/pipenv-project/src/fizz_buzz.py
+++ backend/pipenv-project/src/fizz_buzz.py
@@ -1,6 +1,6 @@
 def fizz_buzz(n):
     if n % 15 == 0:
-        return "fizz buzz"
+        return "XXfizz buzzXX"
 
     if n % 3 == 0:
         return "fizz"
```
</details>

</details>
