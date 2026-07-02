import json
import re
import time

def slow(logs, users):
    result_slow = {}
    for user in users:
        result_slow[user] = []
        for log in logs:
            if user in log["message"] and log["level"] == "ERROR":
                result_slow[user].append(log)
    return result_slow

def fast(logs, users):
    result_fast = {user: [] for user in users}
    users_set = set(users)  
    
    for log in logs:
        if log["level"] == "ERROR":
            message = log["message"]
            if "user " in message:
                parts = message.split()
                i = parts.index("user")
                user = parts[i + 1]
                if user in users_set:
                    result_fast[user].append(log)
    
    return result_fast

with open("1_log/logs.json", "r", encoding="utf-8") as f:
    logs = json.load(f)

users = ["alice", "bob", "charlie", "diana", "eve", "frank", "grace", "henry"]

start = time.time()
result_slow = slow(logs, users)
time_slow = time.time() - start

fast_start = time.time()
result_fast = fast(logs, users)
time_fast = time.time() - fast_start

print(result_slow == result_fast)

print(time_slow)
print(time_fast)