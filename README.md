# Stock Analysis AI Chat Assistant **UNFINISHED
AI Chatbot powered with OpenAI Assistants API
## Description

This Chatbot utilizes OpenAI's powerful Assistant capabilities to give the user (me for now) personalized and relevant news. It gets relevant data by using the function calling tool get data from [News API](https://newsapi.org/) and [Finnhub API](https://finnhub.io/) and merges the two sources to offer meaningful suggestions on the data and investment plan.

**Key Elements:**

- **OpenAI Intergration**: This API is the backbone for engaging the user giving dynamic respones.
- **News API Intergration**: `get_news()` function is called using Assistants **Tools**; function calling, this parses data to return content of most popular articles for review.
- **Finnhub API** - fetches real-time and historically data for the Assistant to analyze.
- **User Interaction and Feedback** - allowing the user to enter values relevant to the API's and get answers relevant to the user.
- **Parsing URL data** - The AI model can't request url data and read it so the data has to be parsed into a readable form.




