from fastapi import FastAPI, Query, Response
from datetime import datetime, timedelta
from requests import get, post
from os import getenv
from dotenv import load_dotenv

app = FastAPI()


def get_total_commits(username: str) -> int:
    try:

        load_dotenv()

        today = datetime.now()

        start_date = today.replace(day=1)

        next_month = start_date.replace(month=start_date.month % 12 + 1, day=1)

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

        headers = {"Authorization": f"Bearer {getenv("GH_KEY")}"}

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


def get_badge(commits: int):
    url = f"https://img.shields.io/badge/Total_Commits_This_Month-{
        commits}-green"

    response = get(url)

    return response.text


@app.get("/")
def root(user: str = Query(description="Github username")):

    total_commits = get_total_commits(user)

    badge = get_badge(total_commits)

    return Response(badge, media_type="image/svg+xml")
