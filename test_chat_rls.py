# verify_performance.py
from supabase_client import supabase
from auth import AuthManager

auth = AuthManager()
success, message, data = auth.login("chemba", "temp123456")

if not success:
    print("❌ Login failed")
    exit(1)

user_id = auth.get_current_user_id()

result = supabase().table("topic_performance").select("*").eq("user_id", user_id).execute()

print("Topic Performance Data:")
print("="*40)
for record in result.data:
    print(f"{record['topic_id']}:")
    print(f"  Attempts: {record['attempts']}")
    print(f"  Correct: {record['correct']}")
    print(f"  Accuracy: {(record['correct']/record['attempts']*100 if record['attempts'] > 0 else 0):.0f}%")
    print(f"  Hints used: {record['hints_used']}")
    print()