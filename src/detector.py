from collections import defaultdict


def analyze_logs(log_lines):

    failed_logins = defaultdict(int)
    port_scans = defaultdict(int)
    unknown_access = defaultdict(int)
    excessive_requests = defaultdict(int)

    for line in log_lines:

        parts = line.split()

        if len(parts) < 2:
            continue

        ip = parts[0]
        activity = parts[1]

        if activity == "LOGIN_FAILED":
            failed_logins[ip] += 1

        elif activity == "PORT_SCAN":
            port_scans[ip] += 1

        elif activity == "UNKNOWN_ACCESS":
            unknown_access[ip] += 1

        elif activity == "REQUEST":
            excessive_requests[ip] += 1

    alerts = []

    for ip, count in failed_logins.items():
        if count >= 3:
            alerts.append({
                "ip": ip,
                "type": "Brute Force Attempt",
                "risk": "HIGH",
                "count": count
            })

    for ip, count in port_scans.items():
        if count >= 2:
            alerts.append({
                "ip": ip,
                "type": "Port Scanning",
                "risk": "MEDIUM",
                "count": count
            })

    for ip, count in unknown_access.items():
        if count >= 2:
            alerts.append({
                "ip": ip,
                "type": "Unknown Access",
                "risk": "HIGH",
                "count": count
            })

    for ip, count in excessive_requests.items():
        if count >= 5:
            alerts.append({
                "ip": ip,
                "type": "Request Flooding",
                "risk": "MEDIUM",
                "count": count
            })

    return alerts