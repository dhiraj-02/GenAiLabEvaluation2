# GenAiLabEvaluation2

# Setup

- make sure python is installed

## First Time:

### in the root directory of project:

#### 1. create a new file .env file as in .env.example and add keys
    # Secrets  
    gemini_api_key=secret key 
    openai_api_key=secret key

    # Configs
    chosen_model={model to be used} #openai/gemini
    openai_version={versions of model} #gpt-4.1 
    gemini_version={version of model} #gemini-2.5-flash

#### 2. Create Virtual env

    python -m venv ./venv

    Any one: Activate virtual env
        Windows powershell: venv\Scripts\Activate.ps1
        Linux commandpromp: source venv/bin/activate

#### 3. Install dependencies

    pip install -r requirements.txt

#### 4. Run the project

    streamlit run app.py

## From next time onwards:

#### Any one: Activate virtual env

    powershell: venv\Scripts\Activate.ps1
        commandpromp: source venv/bin/activate

#### Run the project

    streamlit run ui.py


## Usage
###     Create question would have 
        1. Question name/identifier later to choose from
        2. Question Text - question description
        3. Answer scheme for the question
        4. number of modules - Each would take name and max marks for that module (note: only add which you want to evaluate independently)

###     Submit Task
        1. Select question will get preview
        2. select from available modules to evaluate
        3. give identifier for this task
        4. upload zip file of student solutions 
        5. You will get the folder with name {question-identifier}-{task-identifier} in Results directory here we can see report for each student in a directory name after thier id
            a. Full file compilation 
            b. Module wise test bench generation and compilation reults and probable marks 

###     Prompts Changes if Necessary
        Now we have two prompts in prompt_template.py do modify if necessary and do not modify ((variable)) fomats these are used in run time for replacing values.
        Each prompt has system and content.
        
# (note: The student file name is used to extract the student id which is in main.py line number 92 student_id = base_name.split('_')[-1].split('.')[0] modify this if need now this is supporting files name in format Assignment_2025H1030083P.v -> 2025H1030083P)

### Other Info:

    Debug: Can see each API prompt and Response in log.txt in root directory after task is completed.
