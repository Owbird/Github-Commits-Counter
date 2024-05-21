# GitHub Commits Counter

This application generates a badge displaying the total number of commits made by a specified GitHub user over a given time range, such as `today`, `last_7_days`, or `this_month`.

## Description

The GitHub Commits Counter is a Python and FastAPI application that leverages [Shields.io](https://shields.io/) to create badges. These badges show GitHub contribution statistics for a specified user.

## Supported Time Ranges

The application supports the following time ranges for generating commit badges:

- `today`: Commits made today.
- `last_7_days`: Commits made in the last 7 days.
- `this_month`: Commits made in the current month.

## Usage

To use this application, access the API endpoint at `https://github-commits-counter.vercel.app/` with the query parameters `user` to specify the GitHub username and `range` to specify the time range.

### Example

To get the total commits for the user `owbird` in the current month, make the following request:

```http
GET https://github-commits-counter.vercel.app/?user=owbird&range=this_month
```

This will return an SVG image badge from [Shields.io](https://shields.io/) displaying the total commits made by the user  in the current month.

![Monthly Commits](https://github-commits-counter.vercel.app/?user=owbird&range=this_month)
