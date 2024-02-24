## Multi Agent POC

This is a proof of concept for a multi agent architecture. It simulates a developer(gpt-3.5-turbo) and code reviewer(gpt-3.5-turbo-0125) working together. The input box allows you to input code into the textbox. The developer will write the code and the code reviewer will suggest improvements and the iteration will continue. 



### Running the application

Requires Python, preferably 3.10 or higher

1. Create a python virtual environment with conda or venv (optional)

```bash
    conda create -n multi-agent -y python=3.10 pip
    conda activate multi-agent
```

2. Add your openai key to the streamlit secrets

Create the .streamlit folder and a file called secrets.toml, and add the key

```bash
    mkdir .streamlit
    touch .streamlit/secrets.toml
```

In the secrets.toml file put a line

```OPENAI_API_KEY = "api key goes here"```

3. Install Requirements

```bash
    pip install -r requirements.txt
```

4. Run it

With logging to a file

```bash
streamlit run multi_agent.py --logger.level=info 2>'app.log'
```

or log to terminal

```bash
streamlit run multi_agent.py
```

### Example Conversations

- [React Form](./example_conversations/multi_agent%20·%20Streamlit%20Form.pdf)
- [Python Data](./example_conversations/multi_agent%20·%20Python%20data.pdf)

### Screenshot

![Multi Agent](Multiagent.png?raw=true "Multi Agent")
