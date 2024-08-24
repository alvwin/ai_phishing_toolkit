
# AI Phishing Toolkit
This is a proof of concept to demonstrate the AI generation of targeted phishing emails by scraping social media profiles.

## Installation (Windows)
1. Install [python](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/installation/)
2. clone the repository and enter the folder
    ```
    git clone https://github.com/alvwin/ai_phishing_toolkit
    ```
    ```
    cd ai_phishing_toolkit
    ```
3. create a [venv](https://docs.python.org/3/library/venv.html) (not necessary but good practice, skip to step 5 without venv)
    ```
    python -m venv env
    ```
4. Enter the venv
    ```
    .\env\Scripts\activate.ps1
    ```
5. install requirements
    ```
    pip install -r requirements.txt
    ```
6. If you want to use local AI models, install [ollama](https://ollama.com/download)
7. Install ollama models, the models used in the program are `llama3:latest` and `dolphin-mixtral:8x7b`
	```
	ollama pull llama3:latest
	```
	```
	ollama pull dolphin-mixtral:8x7b
	```
	To use other models you'd also have to update the code since these two models are hard-coded

## Set up
### Twitter
- Create a Twitter account
- Run the program once in interactive mode, enter your credentials.
### LinkedIn
- Create a LinkedIn account
- Get the `li_at` and `sessionid` cookies
- Run the program in interactive mode, enter the cookies

## Usage
For local AI, run `ollama serve`
### Interactive mode
Run the program with
```
python console_program.py
```
Follow instructions

### Batch mode
Run the program with flags
Example:
```
python console_program.py -ai "OpenAI GPT-3.5" -platform LinkedIn -uname user-name -output SMS -payload "Download Link" -api_key [OpenAI api key]
```
Available flags:
```
options:
  -h, --help            show this help message and exit
  -ai {OpenAI GPT-3.5,OpenAI GPT-4,Mistral (local),Llama3 (local)}
                        Select AI to use
  -platform {Twitter,LinkedIn}
                        Select platform to scrape user data from
  -list LIST            Target multiple users (provide file path with username list)
  -uname UNAME          Username of the single user to scrape
  -output {Email,SMS,Vishing script,Twitter DM,Twitter post,Twitter reply,Pretext}
                        Specify what to generate
  -payload {Login page,Attachment,Download Link,Else}
                        Specify type of payload
  -template TEMPLATE    Specify a template to use
  -api_key API_KEY      API key for the AI service
```
