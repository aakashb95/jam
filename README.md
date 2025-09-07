# 🚧 Job application monitoring system 🚧

### Problem statement: <br>
Jobs are applied via various portals, recruiters revert with a different email id of acceptance/rejection, status of each application becomes difficult to track and  your inbox is the only source of truth.

So, what if there is a program that you can run locally, that polls your gmail and maintains the list for you?

This project is an attempt at that.

## What you need
- Gmail API access enabled for your account with credentials. [Link](https://developers.google.com/workspace/gmail/api/quickstart/python)
- OpenAI API key for `gpt-5-nano` 

## TODO:
- [] Complete the pipeline and store in a database
- [] Compare domain and map HR/auto-responses to applied jobs
- [] Should be simple to run, `docker compose` and easy teardown
- [] Don't refetch same emails
- [] Local lightweight model for parsing for true local app

## Credits
Code borrowed from [this article](https://thepythoncode.com/article/use-gmail-api-in-python#Searching_for_Emails)


```<rant>```

It is 2025, spray and pray will not work and ideally there should be an excel sheet
with list of companies applied to. If the outreach is intentional, that list should be pretty small and easy to track manually.

But most of us don't do that. Easy Apply gives the sense of accomplishment and we forget the application in the giant pile of emails.

```</rant>```