### Running the application 
Requires Python, preferably 3.10 or higher

1. Create a python virtual environment with conda or venv (optional)

    conda create -n multi-agent -y python=3.10 pip
    conda activate multi-agent

2. Add your openai key to the streamlit secrets
Create the .streamlit folder and a file called secrets.toml, and add the key

    mkdir .streamlit
    touch .streamlit/secrets.toml

In the file put a line

    OPENAI_API_KEY = "api key goes here"

3. Install Requirements

    pip install -r requirements.txt

4. Run it

With logging to a file
```
streamlit run multi_agent.py --logger.level=info 2>'app.log'
```
or log to terminal

streamlit run multi_agent.py