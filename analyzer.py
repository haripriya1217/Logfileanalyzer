from datetime import datetime
import re
import matplotlib.pyplot as plt
def analyze_log(filepath):
    total_lines = 0
    failed_logins = 0
    # Find IPv4 addresses
    ip_pattern = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
    ip_count = {}
    brute_force_ips = []
    with open(filepath, "r", errors="ignore") as file:
        for line in file:
            total_lines += 1
            # Count IP addresses
            ips = re.findall(ip_pattern, line)
            for ip in ips:
                ip_count[ip] = ip_count.get(ip, 0) + 1
            # Count failed login attempts
            if "failed" in line.lower() or "invalid" in line.lower():
                failed_logins += 1
    # Detect brute-force attacks
    for ip, count in ip_count.items():
        if count >= 3:
            brute_force_ips.append(ip)
    # Create Bar Chart
    if ip_count:
        plt.figure(figsize=(8, 4))
        plt.bar(ip_count.keys(), ip_count.values(), color="red")
        plt.title("IP Address Activity")
        plt.xlabel("IP Address")
        plt.ylabel("Number of Requests")
        plt.xticks(rotation=30)
        plt.tight_layout()
        plt.savefig("static/images/chart.png")
        plt.close()
    # Create Pie Chart
    normal_requests = total_lines - failed_logins
    plt.figure(figsize=(5, 5))
    plt.pie(
        [failed_logins, normal_requests],
        labels=["Failed Logins", "Normal Requests"],
        autopct="%1.1f%%",
        startangle=90
    )
    plt.title("Login Activity Distribution")
    plt.savefig("static/images/pie.png")
    plt.close()
    # Determine threat level
    # Threat Level
    if failed_logins <= 2:
        threat = "🟢 LOW"
    elif failed_logins <= 5:
        threat = "🟠 MEDIUM"
    else:
        threat = "🔴 HIGH"
    return {
    "total_lines": total_lines,
    "failed_logins": failed_logins,
    "ip_count": ip_count,
    "brute_force_ips": brute_force_ips,
    "threat": threat,
    "analysis_time": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
}