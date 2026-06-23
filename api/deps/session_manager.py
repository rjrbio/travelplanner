import uuid

class SessionManager:
    sessions = {}

    @staticmethod
    def create_session():
        session_id = str(uuid.uuid4())
        SessionManager.sessions[session_id] = []
        return session_id

    @staticmethod
    def append_message(session_id, role, message):
        SessionManager.sessions[session_id].append({
            "role": role,
            "message": message
        })

    @staticmethod
    def get_history(session_id):
        return SessionManager.sessions.get(session_id, [])

    @staticmethod
    def reset(session_id):
        SessionManager.sessions[session_id] = []

    @staticmethod
    def delete(session_id):
        SessionManager.sessions.pop(session_id, None)
