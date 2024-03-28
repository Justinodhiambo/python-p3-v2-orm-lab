import sqlite3

CONN = sqlite3.connect("company.db")
CURSOR = CONN.cursor()


class Review:
    def __init__(self, year, summary, employee_id):
        self.id = None
        self.year = year
        self.summary = summary
        self.employee_id = employee_id

    def __repr__(self):
        return f"<Review id={self.id}, year={self.year}, summary={self.summary}, employee_id={self.employee_id}>"

    @staticmethod
    def create_table():
        CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY,
                year INTEGER,
                summary TEXT,
                employee_id INTEGER,
                FOREIGN KEY (employee_id) REFERENCES employees(id)
            )
        """)
        CONN.commit()

    @staticmethod
    def drop_table():
        CURSOR.execute("DROP TABLE IF EXISTS reviews")
        CONN.commit()

    def save(self):
        if self.id:
            self.update()
        else:
            CURSOR.execute("""
                INSERT INTO reviews (year, summary, employee_id)
                VALUES (?, ?, ?)
            """, (self.year, self.summary, self.employee_id))
            CONN.commit()
            self.id = CURSOR.lastrowid

    @classmethod
    def create(cls, year, summary, employee_id):
        review = cls(year, summary, employee_id)
        review.save()
        return review

    @classmethod
    def instance_from_db(cls, row):
        review_id, year, summary, employee_id = row
        review = cls(year, summary, employee_id)
        review.id = review_id
        return review

    @classmethod
    def find_by_id(cls, review_id):
        CURSOR.execute("SELECT * FROM reviews WHERE id=?", (review_id,))
        row = CURSOR.fetchone()
        if row:
            return cls.instance_from_db(row)
        else:
            return None

    def update(self):
        CURSOR.execute("""
            UPDATE reviews
            SET year=?, summary=?, employee_id=?
            WHERE id=?
        """, (self.year, self.summary, self.employee_id, self.id))
        CONN.commit()

    def delete(self):
        CURSOR.execute("DELETE FROM reviews WHERE id=?", (self.id,))
        CONN.commit()
        self.id = None

    @classmethod
    def get_all(cls):
        CURSOR.execute("SELECT * FROM reviews")
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        if isinstance(value, int) and value >= 2000:
            self._year = value
        else:
            raise ValueError("Year must be an integer greater than or equal to 2000")

    @property
    def summary(self):
        return self._summary

    @summary.setter
    def summary(self, value):
        if isinstance(value, str) and value.strip():
            self._summary = value
        else:
            raise ValueError("Summary must be a non-empty string")

    @property
    def employee_id(self):
        return self._employee_id

    @employee_id.setter
    def employee_id(self, value):
        # You may need to add validation to ensure value is a valid employee_id
        self._employee_id = value


class Employee:
    def __init__(self, name, department_id):
        self.id = None
        self.name = name
        self.department_id = department_id

    def __repr__(self):
        return f"<Employee id={self.id}, name={self.name}, department_id={self.department_id}>"

    @staticmethod
    def create_table():
        CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                name TEXT,
                department_id INTEGER,
                FOREIGN KEY (department_id) REFERENCES departments(id)
            )
        """)
        CONN.commit()

    @staticmethod
    def drop_table():
        CURSOR.execute("DROP TABLE IF EXISTS employees")
        CONN.commit()

    def save(self):
        if self.id:
            self.update()
        else:
            CURSOR.execute("""
                INSERT INTO employees (name, department_id)
                VALUES (?, ?)
            """, (self.name, self.department_id))
            CONN.commit()
            self.id = CURSOR.lastrowid

    @classmethod
    def create(cls, name, department_id):
        employee = cls(name, department_id)
        employee.save()
        return employee

    @classmethod
    def instance_from_db(cls, row):
        employee_id, name, department_id = row
        employee = cls(name, department_id)
        employee.id = employee_id
        return employee

    @classmethod
    def find_by_id(cls, employee_id):
        CURSOR.execute("SELECT * FROM employees WHERE id=?", (employee_id,))
        row = CURSOR.fetchone()
        if row:
            return cls.instance_from_db(row)
        else:
            return None

    def update(self):
        CURSOR.execute("""
            UPDATE employees
            SET name=?, department_id=?
            WHERE id=?
        """, (self.name, self.department_id, self.id))
        CONN.commit()

    def delete(self):
        CURSOR.execute("DELETE FROM employees WHERE id=?", (self.id,))
        CONN.commit()
        self.id = None

    @classmethod
    def get_all(cls):
        CURSOR.execute("SELECT * FROM employees")
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]

    def reviews(self):
        CURSOR.execute("SELECT * FROM reviews WHERE employee_id=?", (self.id,))
        rows = CURSOR.fetchall()
        return [Review.instance_from_db(row) for row in rows]

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and value.strip():
            self._name = value
        else:
            raise ValueError("Name must be a non-empty string")

    @property
    def department_id(self):
        return self._department_id

    @department_id.setter
    def department_id(self, value):
        # You may need to add validation to ensure value is a valid department_id
        self._department_id = value

