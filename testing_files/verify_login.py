import sqlite3

def check_login(email):
    print(f"Testing login for: {email}")
    
    # Simulate the UI logic
    if email == "admin@example.com":
        print("  -> Success: Admin exception triggered.")
        return True

    try:
        conn = sqlite3.connect('data/telecom.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM customers WHERE email = ?", (email,))
        user = cursor.fetchone()
        
        conn.close()
        
        if user:
            print("  -> Success: User found in database.")
            return True
        else:
            print("  -> Failed: User not found in database.")
            return False
            
    except Exception as e:
        print(f"  -> Error: {e}")
        return False

# Test cases
print("--- Verification Started ---")
valid_email = "siva@example.com"
invalid_email = "fake_user@example.com"
admin_email = "admin@example.com"

print("\nTest 1: Valid User")
result_valid = check_login(valid_email)

print("\nTest 2: Invalid User")
result_invalid = check_login(invalid_email)

print("\nTest 3: Admin Exception")
result_admin = check_login(admin_email)

if result_valid and not result_invalid and result_admin:
    print("\n--- Verification PASSED: Logic is correct. ---")
else:
    print("\n--- Verification FAILED: Logic is incorrect. ---")
