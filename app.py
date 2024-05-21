from fastapi import FastAPI, Query, Response
from datetime import datetime, timedelta
from requests import get, post
from os import getenv
from dotenv import load_dotenv

app = FastAPI()


def get_total_commits(username: str, range: str) -> int:
    try:

        load_dotenv()

        today = datetime.now()

        if range == "today":
            start_date = today.replace(
                hour=0, minute=0, second=0)
            end_date = today.replace(
                hour=23, minute=59, second=59)
        elif range == "last_7_days":
            end_date = today.replace(
                hour=23, minute=59, second=59)
            start_date = end_date - timedelta(days=7)
        else:
            start_date = today.replace(day=1)
            next_month = start_date.replace(
                month=start_date.month % 12 + 1, day=1)
            end_date = next_month - timedelta(days=1)

        start_date_formatted = start_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        end_date_formatted = end_date.strftime('%Y-%m-%dT%H:%M:%SZ')

        url = "https://api.github.com/graphql"

        query = f"""
                query {{
                    user(login: "{username}") {{
                        contributionsCollection(
                        from: "{start_date_formatted}",
                        to: "{end_date_formatted}") {{
                            contributionCalendar {{
                                totalContributions
                                }}
                            }}
                        }}
                }}
        """

        headers = {"Authorization": f"Bearer {getenv('GH_KEY')}"}

        response = post(url,
                        headers=headers,
                        json={"query": query})

        data = response.json()

        return (
            data["data"]["user"]["contributionsCollection"]
            ["contributionCalendar"]["totalContributions"]
        )
    except Exception as e:
        print(e)
        return 0


def get_badge(commits: int, range: str):
    url = "https://img.shields.io/badge"

    if range == "today":
        label = "today"
    elif range == "last_7_days":
        label = "last_7_days"
    else:
        label = "This_Month"

    response = get(f"{url}/Total_Commits_{label}-{commits}-green")

    return response.text


@app.get("/")
def root(user: str = Query(description="Github username"),
         range: str = Query(default="this_month", description="Date range")):

    total_commits = get_total_commits(user, range.lower())

    badge = get_badge(total_commits, range.lower())

    return Response(badge, media_type="image/svg+xml")
