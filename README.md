# OpenAI bot

* Uses the [webex_bot](https://github.com/fbradyirl/webex_bot) library to pass through conversations with OpenAI.

To use:

```sh
export WEBEX_TEAMS_ACCESS_TOKEN=XXX
export OPENAI_API_KEY=XXX
export WEBEX_EMAIL=<your email>

# Recommended to first create and use a virtual environment before running the following:
pip install -r requirements.txt
python app.py
```