from sourcefiles import SQLite


x = SQLite()

print(*x.get_user_by_status(1))