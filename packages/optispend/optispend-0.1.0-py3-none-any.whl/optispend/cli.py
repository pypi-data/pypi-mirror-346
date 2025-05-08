import boto3
import argparse
import numpy as np
from datetime import datetime, timedelta, timezone
from botocore.exceptions import NoCredentialsError, ProfileNotFound, ClientError

def main():
    parser = argparse.ArgumentParser(description="OptiSpend – Multi-Cloud Savings Plan Estimator")
    parser.add_argument("--profile", help="AWS CLI profile (optional if using env vars)")
    parser.add_argument("--commitment", type=float, help="Manual commitment %, e.g. 0.8 for 80%%")
    parser.add_argument("--optimize", action="store_true", help="Run optimized commitment simulation")
    args = parser.parse_args()

    DAYS = 14

    try:
        if args.profile:
            print(f"🔐 Using profile: {args.profile}")
            session = boto3.Session(profile_name=args.profile)
        else:
            print("🔐 Using environment-based credentials")
            session = boto3.Session()
        client = session.client("ce", region_name="us-east-1")
    except (NoCredentialsError, ProfileNotFound) as e:
        print(f"❌ Failed to initialize AWS session: {e}")
        exit(1)

    now = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
    end = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    start = (now - timedelta(days=DAYS)).strftime("%Y-%m-%dT%H:%M:%SZ")

    print(f"🔍 [OptiSpend] Fetching hourly usage from {start} to {end} for all linked accounts...")

    results = []
    token = None

    try:
        while True:
            kwargs = {
                "TimePeriod": {"Start": start, "End": end},
                "Granularity": "HOURLY",
                "Metrics": ["UnblendedCost"],
                "GroupBy": [{"Type": "DIMENSION", "Key": "LINKED_ACCOUNT"}]
            }

            if token:
                kwargs["NextPageToken"] = token

            response = client.get_cost_and_usage(**kwargs)

            for result_by_time in response["ResultsByTime"]:
                total = sum(float(g["Metrics"]["UnblendedCost"]["Amount"]) for g in result_by_time["Groups"])
                results.append(total)

            token = response.get("NextPageToken")
            if not token:
                break
    except ClientError as e:
        print(f"❌ AWS API error: {e}")
        exit(1)

    filtered = [r for r in results if r > 0]

    if not filtered:
        print("⚠️ No billable hours found. Cannot calculate recommendations.")
        exit(1)

    min_hourly = min(filtered)
    avg_hourly = sum(filtered) / len(filtered)
    std_dev = np.std(filtered)
    cov = std_dev / avg_hourly
    monthly_projection = lambda h: round(h * 24 * 30, 2)

    if args.optimize:
        print("\n📊 [OptiSpend] Optimizing commitment recommendations...\n")
        levels = [0.5, 0.65, 0.75, 0.8, 0.9]
        print(f"{'Commitment %':<15} {'Hourly Commit':<15} {'Projected Monthly Cost'}")
        for level in levels:
            hourly = round(min_hourly * level, 2)
            monthly = monthly_projection(hourly)
            print(f"{int(level * 100):<15}% ${hourly:<14.2f} ${monthly:,.2f}")
        print()
        return

    commit = args.commitment if args.commitment else 0.50
    suggested = round(min_hourly * commit, 2)
    monthly_cost = monthly_projection(suggested)

    print(f"\n🧾 [OptiSpend] Savings Plan Recommendation ({int(commit * 100)}% of min hourly):")
    print(f"- Minimum Hourly Spend:           ${min_hourly:.2f}")
    print(f"- Average Hourly Spend:           ${avg_hourly:.2f}")
    print(f"- Std Dev (Volatility):           ${std_dev:.2f} ({cov:.2%} COV)")
    print(f"- Suggested Commitment:           ${suggested:.2f}/hour")
    print(f"- Projected Monthly Cost:         ${monthly_cost:,.2f}\n")
