# GitHub Commits Counter

This application generates a badge showing the total number of commits made for the current month on a user's GitHub profile.

## Description

The application is built using Python and FastAPI, leveraging BeautifulSoup for web scraping, [Shields.io](https://shields.io/) for badges, to extract GitHub contribution information for a specified user in the current month.

## Usage

To use this application, access the API endpoint `https://github-commits-counter.vercel.app/` with a query parameter `user` specifying the GitHub username.

Example:

```http
GET https://github-commits-counter.vercel.app/?user=owbird
```

![Month Commits](https://github-commits-counter.vercel.app/?user=owbird)

The response will be an SVG image from [Shields.io](https://shields.io/) displaying the total commits made by the specified user in the current month.
