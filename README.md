# OpenAI bot

> [!IMPORTANT]  
> This repository is only sporadically maintained.  Breaking API changes will be maintained on a best efforts basis.
>
> Collaborators are welcome, as are PRs for enhancements.
>
> Bug reports unrelated to API changes may not get the attention you want. 


![openai_bot](https://user-images.githubusercontent.com/254309/228500024-45f49d56-7c54-42cc-8a27-8e5b0c83a0ff.png)

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