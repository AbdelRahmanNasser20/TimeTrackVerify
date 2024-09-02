import re

# Define the regex pattern
PATTERN = r"((\w+ [\w-]+\.? \(\w+ (\d?\.\d{1,2})\))|(Moe))( & (\w+ [\w-]+\.? \(\w+ (\d?\.\d{1,2})\)|Moe))* @ .+"

PATTERN = r"(Moe(\s\(\w\s\d\.\d\))?|(\w+\s[\w-]+\.?\s\(\w+\s\d\.\d\)))(\s&\s(Moe(\s\(\w\s\d\.\d\))?|(\w+\s[\w-]+\.?\s\(\w+\s\d\.\d\))))*\s@\s.+"


# List of subjects to check
Wrong_subjects = [
'Moe & Daniel L. (S 7.0) & Valery G. (M 4.0) & Valery G. (S 3.0) & Neel J. (E 4.0) & William Y. (S 3.0) @ PANDA CAMP', 
'Moe (M) & Neel J. (M 4.0) & Daniel L. (S 7.0) & Valery G. (S 4.0) & William Y. (S 3.0) @ PANDA CAMP', 
' Antonio L. (M 7.5) & Eric S. (S 7.0) & Vihan P. (S 7.0)  & Emran S. (S 4.0) & Mamadou D. (S 3.0) @ PANDA CAMP', 
'Antonio L. (M 7.5) & Eric S. (S 7.0) & Vihan P. (S 4.0)  & Emran S. (S 7.0) & Mamadou D. (S 3.0) @ PANDA CAMP', 
' Antonio L. (M 7.5) & Eric S. (S 7.0) & Vihan P. (S 7.0)  & Emran S. (S 4.0) & Mamadou D. (S 3.0) @ PANDA CAMP', 
' Antonio L. (M 7.5) & Eric S. (S 7.0) & Vihan P. (S 7.0)  & Emran S. (S 4.0) & Mamadou D. (S 3.0) @ PANDA CAMP', 
'Moe (M) & Eric S. (S 7.5) & Valery G. (S 7.5) & Daniel M. (S 7.5) & Neel J. (S 3.5) & Neel J. (M 4.0) & Vihan P. (S 3.0) & Amy T. (S 3.5) @ PANDA CAMP', 
'Moe (M) & Eric S. (S 7.0) & Valery G. (S 7.0) & Daniel M. (S 7.0) & Neel J. (M 6.0) & Vihan P. (S 3.0) @ PANDA CAMP', 
'Moe (M) & Eric S. (S 7.0) & Valery G. (S 7.0) & Daniel M. (S 7.0) & Neel J. (M 7.5) & Amy T. (S 3.0) @ PANDA CAMP', 
'Angelina R. (M 9.0) & Shreyas B. (S 8.0) & Aleeza S. (S 8.0) & Shayaan P. (S 8.0) & .0) & Matthew D. (I 8.0) & Ava B. (I 8.0) @ Camp']

GPT_fixed_subjects = [
    "Moe & Daniel L. (S 7.0) & Valery G. (M 4.0) & Valery G. (S 3.0) & Neel J. (E 4.0) & William Y. (S 3.0) @ PANDA CAMP",
    "Moe & Neel J. (M 4.0) & Daniel L. (S 7.0) & Valery G. (S 4.0) & William Y. (S 3.0) @ PANDA CAMP",
    "Antonio L. (M 7.5) & Eric S. (S 7.0) & Vihan P. (S 7.0) & Emran S. (S 4.0) & Mamadou D. (S 3.0) @ PANDA CAMP",
    "Antonio L. (M 7.5) & Eric S. (S 7.0) & Vihan P. (S 4.0) & Emran S. (S 7.0) & Mamadou D. (S 3.0) @ PANDA CAMP",
    "Antonio L. (M 7.5) & Eric S. (S 7.0) & Vihan P. (S 7.0) & Emran S. (S 4.0) & Mamadou D. (S 3.0) @ PANDA CAMP",
    "Antonio L. (M 7.5) & Eric S. (S 7.0) & Vihan P. (S 7.0) & Emran S. (S 4.0) & Mamadou D. (S 3.0) @ PANDA CAMP",
    "Moe & Eric S. (S 7.5) & Valery G. (S 7.5) & Daniel M. (S 7.5) & Neel J. (S 3.5) & Neel J. (M 4.0) & Vihan P. (S 3.0) & Amy T. (S 3.5) @ PANDA CAMP",
    "Moe & Eric S. (S 7.0) & Valery G. (S 7.0) & Daniel M. (S 7.0) & Neel J. (M 6.0) & Vihan P. (S 3.0) @ PANDA CAMP",
    "Moe & Eric S. (S 7.0) & Valery G. (S 7.0) & Daniel M. (S 7.0) & Neel J. (M 7.5) & Amy T. (S 3.0) @ PANDA CAMP",
    "Angelina R. (M 9.0) & Shreyas B. (S 8.0) & Aleeza S. (S 8.0) & Shayaan P. (S 8.0) & .0) & Matthew D. (I 8.0) & Ava B. (I 8.0) @ Camp"
]

My_fix_correct = [
'Daniel L. (S 7.0) & Valery G. (M 4.0) & Valery G. (S 3.0) & Neel J. (E 4.0) & William Y. (S 3.0) @ PANDA CAMP', 
'Neel J. (M 4.0) & Daniel L. (S 7.0) & Valery G. (S 4.0) & William Y. (S 3.0) @ PANDA CAMP', 
'Antonio L. (M 7.5) & Eric S. (S 7.0) & Vihan P. (S 7.0) & Emran S. (S 4.0) & Mamadou D. (S 3.0) @ PANDA CAMP', # leading space between ant and &
'Antonio L. (M 7.5) & Eric S. (S 7.0) & Vihan P. (S 4.0) & Emran S. (S 7.0) & Mamadou D. (S 3.0) @ PANDA CAMP', # leading space between ant and &
'Antonio L. (M 7.5) & Eric S. (S 7.0) & Vihan P. (S 7.0) & Emran S. (S 4.0) & Mamadou D. (S 3.0) @ PANDA CAMP', # leading space between ant and &
'Antonio L. (M 7.5) & Eric S. (S 7.0) & Vihan P. (S 7.0) & Emran S. (S 4.0) & Mamadou D. (S 3.0) @ PANDA CAMP', 
'Eric S. (S 7.5) & Valery G. (S 7.5) & Daniel M. (S 7.5) & Neel J. (S 3.5) & Neel J. (M 4.0) & Vihan P. (S 3.0) & Amy T. (S 3.5) @ PANDA CAMP', 
'Eric S. (S 7.0) & Valery G. (S 7.0) & Daniel M. (S 7.0) & Neel J. (M 6.0) & Vihan P. (S 3.0) @ PANDA CAMP', 
'Eric S. (S 7.0) & Valery G. (S 7.0) & Daniel M. (S 7.0) & Neel J. (M 7.5) & Amy T. (S 3.0) @ PANDA CAMP', 
'Angelina R. (M 9.0) & Shreyas B. (S 8.0) & Aleeza S. (S 8.0) & Shayaan P. (S 8.0) & Matthew D. (I 8.0) & Ava B. (I 8.0) @ Camp'
]

invalid_entries = []
# Iterate through each subject and check if it matches the pattern
for i, subject in enumerate(GPT_fixed_subjects):
    if re.match(PATTERN, subject):
        print(f"Subject at index {i} matches the pattern.")
    else:
        invalid_entries.append(subject)
        print(f"Subject at index {i} does NOT match the pattern: {subject}")

# print(invalid_entries)