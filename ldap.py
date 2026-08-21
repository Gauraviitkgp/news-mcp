from ldap3 import Server, Connection, ALL, SUBTREE
from ldap3.core.exceptions import LDAPBindError, LDAPException


def authenticate_user(username: str, password: str) -> bool:
    """
    Authenticate a user against an LDAP server using a simple bind.
    """
    server = Server("ldap://ldap.example.com:389", get_info=ALL)

    # Construct the DN (Distinguished Name) for the bind.
    # Adjust this to match your directory's structure.
    user_dn = f"uid={username},ou=users,dc=example,dc=com"

    try:
        conn = Connection(server, user=user_dn, password=password, auto_bind=True)
        conn.unbind()
        return True
    except LDAPBindError:
        # Invalid credentials
        return False
    except LDAPException as e:
        print(f"LDAP error: {e}")
        return False


if __name__ == "__main__":
    ok = authenticate_user("jdoe", "supersecret")
    print("Authenticated!" if ok else "Authentication failed.")
