import csv

def generate_csv(result, filename):
    csv_path = f"reports/{filename}_report.csv"

    with open(csv_path, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["Log File Analysis Report"])
        writer.writerow([])

        writer.writerow(["Total Log Entries", result["total_lines"]])
        writer.writerow(["Failed Login Attempts", result["failed_logins"]])
        writer.writerow(["Threat Level", result["threat"]])

        writer.writerow([])
        writer.writerow(["Detected IP", "Requests"])

        for ip, count in result["ip_count"].items():
            writer.writerow([ip, count])

    return csv_path