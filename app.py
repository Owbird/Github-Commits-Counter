from bs4 import BeautifulSoup
from fastapi import FastAPI, Query, Response
from datetime import datetime, timedelta
from requests import get

app = FastAPI()


def get_total_commits(username: str) -> int:
    try:

        today = datetime.now()

        start_date = today.replace(day=1)

        next_month = start_date.replace(month=start_date.month % 12 + 1, day=1)

        end_date = next_month - timedelta(days=1)

        start_date_formatted = start_date.strftime('%Y-%m-%d')
        end_date_formatted = end_date.strftime('%Y-%m-%d')

        url = f"https://github.com/{username}?tab=overview&from={start_date_formatted}&to={end_date_formatted}"

        response = get(url)

        soup = BeautifulSoup(response.text, "html.parser")

        total_days = (end_date - start_date).days

        print(total_days)

        date = start_date

        contributions = []

        for _ in range(total_days + 1):
            contributions.extend(soup.find_all(
                attrs={"data-date": date.strftime("%Y-%m-%d")}))
            date += timedelta(days=1)

        total_commits = sum(int(contribution.text.split(" ")[
            0]) for contribution in contributions if contribution.text.split(" ")[0] != "No")

        return total_commits
    except Exception as e:
        return 0


def get_badge(commits: int):
    url = f"https://img.shields.io/badge/Total_Commits_This_Month-{commits}-green"

    response = get(url)

    return response.text


@app.get("/")
def root(user: str = Query(description="Github username")):

    total_commits = get_total_commits(user)

    badge = get_badge(total_commits)

    return Response(badge, media_type="image/svg+xml")
