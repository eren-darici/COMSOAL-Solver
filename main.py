from solver import COMSOAL


comsoal = COMSOAL(data_path='odev-veri.xlsx', C=14)
assignments = comsoal.solve()
print(f"Assignments: {assignments}")
comsoal.evaluate(assignments)