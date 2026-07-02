import random
from datetime import datetime, timedelta
import json

def generate_logs(count):
    levels = ["INFO", "INFO", "INFO", "WARNING", "WARNING", "ERROR", "DEBUG", "CRITICAL"]
    
    messages = {
        "INFO": [
            "User {user} logged in from IP {ip}",
            "User {user} logged out",
            "Request processed successfully in {time}ms",
            "File uploaded: {filename}",
            "Email sent to {user}@company.com",
            "Database query completed in {time}ms",
            "Session started for user {user}",
            "API endpoint /users accessed",
            "Configuration loaded successfully",
            "Cache refreshed for module {module}"
        ],
        "WARNING": [
            "High memory usage detected: {percent}%",
            "Slow query detected: {time}ms",
            "User {user} attempted unauthorized access",
            "Deprecated API version used by client {ip}",
            "Cache miss for key: user_{user}",
            "Rate limit approaching for IP {ip}",
            "Disk space low: {percent}% used",
            "Connection pool nearly exhausted"
        ],
        "ERROR": [
            "Database connection failed: timeout after {time}s",
            "File not found: /uploads/{filename}",
            "Authentication failed for user {user}",
            "Payment processing error for order #{order}",
            "External API returned status 500",
            "Failed to send email from user {user}",
            "Invalid JSON in request body from IP {ip}",
            "Permission denied: user {user} lacks admin role"
        ],
        "CRITICAL": [
            "Out of memory: killing process",
            "Database server unreachable",
            "Security breach detected from IP {ip}",
            "Data corruption in table users",
            "Service crashed unexpectedly"
        ],
        "DEBUG": [
            "Entering function process_request()",
            "Variable state: user_id={user}, session={session}",
            "SQL query: SELECT * FROM users WHERE id={user}",
            "Headers received: {headers}",
            "Memory allocation: {time}ms"
        ]
    }
    
    users = ["alice", "bob", "charlie", "diana", "eve", "frank", "grace", "henry"]
    ips = ["192.168.1." + str(i) for i in range(1, 50)]
    filenames = ["report.pdf", "photo.jpg", "document.docx", "data.csv", "backup.zip"]
    modules = ["auth", "cache", "payment", "storage", "analytics"]
    headers = ["Content-Type: application/json", "User-Agent: Mozilla/5.0"]
    
    logs = []
    base_time = datetime.now()
    
    for i in range(count):
        level = random.choice(levels)
        template = random.choice(messages[level])
        
        message = template.format(
            user=random.choice(users),
            ip=random.choice(ips),
            time=random.randint(10, 5000),
            filename=random.choice(filenames),
            module=random.choice(modules),
            percent=random.randint(70, 99),
            order=random.randint(10000, 99999),
            session=random.randint(1000, 9999),
            headers=random.choice(headers)
        )
        
        log = {
            "id": i + 1,
            "timestamp": (base_time + timedelta(seconds=i)).strftime("%Y-%m-%d %H:%M:%S"),
            "level": level,
            "message": message
        }
        logs.append(log)
    
    return logs

logs = generate_logs(50000)

with open("1_log/logs.json", "w", encoding="utf-8") as f:
    json.dump(logs, f, ensure_ascii=False, indent=2)