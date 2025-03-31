import pyodbc
from typing import Optional, Dict, Any, List

class EmployeeCRUD:
    """Professional Employee CRUD Operations for SQL Server"""
    
    def __init__(self):
        self.conn_str = (
            'DRIVER={SQL Server};'
            'SERVER=tcp:mcruebs04.isad.isadroot.ex.ac.uk;'
            'DATABASE=BEMM459_GroupW;'
            'UID=GroupW;'
            'PWD=YhdF813+Kr'
        )

    def _get_connection(self):
        """Establish database connection with error handling"""
        try:
            return pyodbc.connect(self.conn_str)
        except pyodbc.Error as e:
            raise DatabaseError(f"Connection failed: {str(e)}")

    # CREATE
    def create_employee(self, employee_data: Dict[str, Any]) -> bool:
        """Insert a new employee record"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO [EmployeeDatas].[EMPLOYEE] 
                    (employeeID, firstName, lastName, email, hireDate, departmentID, billRate, atRiskStatus)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, 
                employee_data['employeeID'],
                employee_data['firstName'],
                employee_data['lastName'],
                employee_data['email'],
                employee_data['hireDate'],
                employee_data.get('departmentID'),
                employee_data['billRate'],
                employee_data['atRiskStatus'])
                conn.commit()
                return True
        except pyodbc.Error as e:
            conn.rollback()
            raise DatabaseError(f"Create operation failed: {str(e)}")

    # READ 
    def get_employee(self, employee_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve a single employee by ID"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM [EmployeeDatas].[EMPLOYEE] 
                    WHERE employeeID = ?
                """, employee_id)
                
                row = cursor.fetchone()
                if row:
                    columns = [col[0] for col in cursor.description]
                    return dict(zip(columns, row))
                return None
        except pyodbc.Error as e:
            raise DatabaseError(f"Read operation failed: {str(e)}")

    # READ (Get all employees)
    def get_all_employees(self) -> List[Dict[str, Any]]:
        """Retrieve all employee records"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM [EmployeeDatas].[EMPLOYEE]")
                rows = cursor.fetchall()
                columns = [col[0] for col in cursor.description]
                return [dict(zip(columns, row)) for row in rows]
        except pyodbc.Error as e:
            raise DatabaseError(f"Bulk read failed: {str(e)}")

    # UPDATE
    def update_employee(self, employee_id: int, update_data: Dict[str, Any]) -> bool:
        """Update existing employee record"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Dynamically build SET clause
                set_clause = ", ".join([f"{k} = ?" for k in update_data.keys()])
                values = list(update_data.values())
                values.append(employee_id)
                
                cursor.execute(f"""
                    UPDATE [EmployeeDatas].[EMPLOYEE]
                    SET {set_clause}
                    WHERE employeeID = ?
                """, *values)
                
                conn.commit()
                return cursor.rowcount > 0
        except pyodbc.Error as e:
            conn.rollback()
            raise DatabaseError(f"Update operation failed: {str(e)}")

    # DELETE
    def delete_employee(self, employee_id: int) -> bool:
        """Remove an employee record"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    DELETE FROM [EmployeeDatas].[EMPLOYEE]
                    WHERE employeeID = ?
                """, employee_id)
                conn.commit()
                return cursor.rowcount > 0
        except pyodbc.Error as e:
            conn.rollback()
            raise DatabaseError(f"Delete operation failed: {str(e)}")

class DatabaseError(Exception):
    """Custom database exception class"""
    pass

# Example Usage
if __name__ == "__main__":
    db = EmployeeCRUD()
    
    try:
        # Test CREATE
        new_emp = {
            'employeeID': 51,
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
            'hireDate': '2023-01-15',
            'departmentID': 2,
            'billRate': 85.50,
            'atRiskStatus': 0
        }
        
        if db.create_employee(new_emp):
            print("Employee created successfully")
        
        # Test READ (single)
        employee = db.get_employee(51)
        print(f"Retrieved employee: {employee}")
        
        # Test UPDATE
        update_data = {
            'firstName': 'Jonathan',
            'billRate': 90.00,
            'atRiskStatus': 1
        }
        if db.update_employee(51, update_data):
            print("Employee updated successfully")
            print(f"Updated record: {db.get_employee(51)}")
        
        # Test READ (all)
        all_employees = db.get_all_employees()
        print(f"Total employees: {len(all_employees)}")
        
        # Test DELETE
        if db.delete_employee(51):
            print("Employee deleted successfully")
        
    except DatabaseError as e:
        print(f"Database operation error: {e}")
        
        
        
        
        
