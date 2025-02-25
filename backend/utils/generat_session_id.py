import uuid

def generate_session_ids(num_ids=30):
    session_ids = []
    for _ in range(num_ids):
        session_id = str(uuid.uuid4())
        session_ids.append(f'"session_id": "{session_id}"')
    return session_ids

if __name__ == "__main__":
    session_ids = generate_session_ids()
    for session_id in session_ids:
        print(session_id) 