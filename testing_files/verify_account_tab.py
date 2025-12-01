import sqlite3

def get_customer_details(email):
    print(f"Fetching details for: {email}")
    try:
        conn = sqlite3.connect('data/telecom.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM customers WHERE email = ?", (email,))
        user_data = cursor.fetchone()
        
        conn.close()
        
        if user_data:
            print("  -> Success: Customer found.")
            print(f"     Name: {user_data['name']}")
            print(f"     Phone: {user_data['phone_number']}")
            print(f"     Plan: {user_data['service_plan_id']}")
            return True
        else:
            print("  -> Failed: Customer not found.")
            return False
            
    except Exception as e:
        print(f"  -> Error: {e}")
        return False

# Test cases
print("--- Verification Started ---")
get_customer_details("siva@example.com")
get_customer_details("vikram.reddy@example.com")
get_customer_details("fake@example.com")
