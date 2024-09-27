import sqlite3 as sq

class Database:
    def __init__(self, db_file):
        self.connection = sq.connect(db_file)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)).fetchmany(1)
            return bool(len(result))

    def add_user(self, user_id, nickname):
        with self.connection:
            return self.cursor.execute("INSERT INTO users (user_id, nick) VALUES (?, ?)", (user_id, nickname,))
        
    def set_name(self, user_id, name):
        with self.connection:
            return self.cursor.execute("UPDATE users SET name = ? WHERE user_id = ?", (name, user_id,))
    
    def set_age(self, user_id, age):
        with self.connection:
            return self.cursor.execute("UPDATE users SET age = ? WHERE user_id = ?", (age, user_id,))

    def get_users(self):
        with self.connection:
            return self.cursor.execute("SELECT user_id FROM users").fetchall()
    
    def get_user_name(self, user_id):
        return self.cursor.execute("SELECT name FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        
    def get_registered_users(self):
        with self.connection:
            return self.cursor.execute("SELECT user_id FROM users WHERE name != NULL AND age != NULL").fetchall()
    
    def get_name(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT name FROM users WHERE user_id = ?", (user_id,)).fetchone()
    
    def get_age(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT age FROM users WHERE user_id = ?", (user_id,)).fetchone()
        
    def set_waiting(self, id, waiting):
        with self.connection:
            return self.cursor.execute(f"UPDATE admins SET {waiting} = 1 WHERE id = ?", (id,)) 
    
    def cancel_waiting(self, id):
        with self.connection:
            self.cursor.execute("UPDATE admins SET waiting = 0 WHERE id = ?", (id,))
            self.cursor.execute("UPDATE admins SET waiting_mentor_add = 0 WHERE id = ?", (id,))
            self.cursor.execute("UPDATE admins SET waiting_mentor_del = 0 WHERE id = ?", (id,))
    
    def get_waiting(self, id):
        with self.connection:
            return self.cursor.execute("SELECT * FROM admins WHERE id = ?", (id,)).fetchone()

    def add_mentor(self, nick, name):
        with self.connection:
            return self.cursor.execute("INSERT INTO mentors (nick, name) VALUES (?, ?)", (nick, name,))

    def del_mentor(self, nick):
        with self.connection:
            return self.cursor.execute("DELETE FROM mentors WHERE nick=?", (nick,))

    def assign_mentor(self, user_id, mentor_nick, mentor_name):
        with self.connection:
            return self.cursor.execute("INSERT INTO users (mentor_data) VALUES (?)", (f'{mentor_nick} {mentor_name}',))

    def get_assigned_mentor(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT mentor_data FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    
    def get_current_mentor(self):
         with self.connection:
            current_nick = self.cursor.execute("SELECT nick FROM current_mentor WHERE id = 1").fetchone()[0]
            current_name = self.cursor.execute("SELECT name FROM current_mentor WHERE id = 1").fetchone()[0]
            return [current_nick, current_name]

    def get_current_mentor_id(self):
        with self.connection:
            current_nick = self.cursor.execute("SELECT nick FROM current_mentor WHERE id = 1").fetchone()[0]
            return self.cursor.execute("SELECT id FROM users WHERE nick=?", (current_nick,)).fetchone()[0]
            
    def change_current_mentor(self):
        with self.connection:
            current_nick = self.get_current_mentor()[0]
            nicks_all = self.cursor.execute("SELECT nick FROM mentors").fetchall()
            names_all = self.cursor.execute("SELECT name FROM mentors").fetchall()
            nicks = [row[0] for row in nicks_all]
            names = [row[0] for row in names_all]
            current_id = 0
            for i in range(len(nicks)):
                if nicks[i] == current_nick:
                    current_id += i
                    current_id += 1
                    break
            if current_id == len(nicks):
                current_id = 0
            self.cursor.execute("DELETE FROM current_mentor WHERE nick=?", (current_nick,))
            return self.cursor.execute("INSERT INTO current_mentor (id, nick, name) VALUES (?, ?, ?)", (1, nicks[current_id], names[current_id],))
            

db = Database('database.db')
if db.connection:
    print('The data base has been successfully connected')
else:
    print('Failed to connect to data base')
