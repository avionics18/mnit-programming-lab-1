q = "Select name, age FROM student"

projection_cols = q[q.upper().find("SELECT") + len("SELECT"):q.upper().find("FROM"):].strip()

print(projection_cols)