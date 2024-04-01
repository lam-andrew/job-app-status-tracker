import os
from openai import OpenAI
from datetime import date
from flask import Flask

app = Flask(__name__)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/hello")
def hello():
    return "Hello World"

# job_desc format: string
# current_date format: YYYY-MM-DD
@app.route("/insert_job/<job_desc_input>/<current_date>")
def gen_job_entry(job_desc_input, current_date):
    api_prompt=f'''
    Given the following job description, extract and structure the essential details into a JSON format including the Job Title, Company Name, Location, Work Format, Remote Work Availability, Application Deadline, and any additional relevant details you can find. 
    If certain information cannot be found within the job description, please identify those fields as null. Do not attempt to assume any unspecified attributes based on the context, but ensure all fields are present in the final JSON. 
    Add an Application Date as the current date to track when the job description was entered and set the Application Status to 'Applied' as a default for the entry.
    Note: The "ApplicationDate" field should be set to the date on which this prompt is being processed {current_date}.
    If there are any additional details that you find in the job description that are not current an attribute of the json template below, please add them into the nested AdditionalDetails json

    ---

    {job_desc_input}

    ---

    Please structure the information as follows:

    {{
    "JobTitle": "<Job Title or null>",
    "CompanyName": "<Company Name or null>",
    "Location": "<Location or null>",
    "WorkFormat": "<Full-Time/Part-Time/Contract/Internship or null>",
    "RemoteWorkAvailability": "<Onsite/Remote/Hybrid or null>",
    "ApplicationDeadline": "<YYYY-MM-DD or null>",
    "ApplicationDate": "Please insert the current date in YYYY-MM-DD format",
    "SalaryRange": "<If available or null>",
    "RequiredSkills": ["<Skill 1>", "<Skill 2>", "... or null"],
    "Benefits": ["<Benefit 1>", "<Benefit 2>", "... or null"],
    "ApplicationStatus": "Applied",
    "AdditionalDetails": {{
        "ApplicationLink": "<URL if available or null>"
    }}
    }}
    '''

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": api_prompt,
            }
        ],
        response_format={"type": "json_object"},
        model="gpt-4-1106-preview",
    )

    res = chat_completion.choices[0].message.content
    return res


contains_extra_fields_for_later = '''
    {
        "JobID": "12345",
        "JobTitle": "Software Engineer",
        "CompanyName": "Tech Innovations Inc.",
        "Location": "San Francisco, CA",
        "Industry": "Technology",
        "WorkFormat": "Full-Time",
        "RemoteWorkAvailability": "Hybrid",
        "ApplicationDate": "2024-03-20",
        "ApplicationDeadline": "2024-04-15",
        "StatusOfApplication": "Applied",
        "Salary": "$120,000 - $130,000",
        "Benefits": ["Health insurance", "401(k) matching", "Remote work options"],
        "ContactInformation": {
        "Name": "Jane Doe",
        "Email": "jane.doe@techinnovations.com",
        "Phone": "555-1234"
        },
        "InterviewDate": "2024-04-05",
        "OfferDetails": {
        "Salary": "$120,000",
        "Start Date": "2024-05-01",
        "OtherBenefits": ["Health Insurance", "Retirement Plan", "Paid Time Off"]
        },
        "NotesComments": "Need to prepare for the coding test. Review the company's recent projects."
    }
    '''

current_date = date.today()

job_desc_input='''
Software Developer- job post
Sherman Buildings
Remote
$40 - $50 an hour - Part-time, Contract
Sherman Buildings
Remote
$40 - $50 an hour
Profile insights
Your profile might be missing qualifications mentioned in the job description
Skills

VBA

APIs

Software troubleshooting
+ show more

Do you have experience in VBA?
&nbsp;
Job details
Here’s how the job details align with your profile.
Pay

$40 - $50 an hour
Job type

Part-time

Contract
Shift and schedule

Choose your own hours
Encouraged to apply
Fair chance
&nbsp;
Full job description

Simplify
Simplify
3 of 10 keywords
Beta
30%
resume match
About us

We are a family owned construction company focused on using technology to improve Teamwork, Safety, Quality, and Efficiency.

We build the best tools we can for our in-house crews, then turn around and share those tools with our industry of small residential accessory building contractors.

Develop from Home

Job Overview:

We are seeking an ambitious junior freelance software developer to join our team. Features will initially be provided by a manager, but could be developed independently in collaboration with salespeople, job foremen and administrators if you'd like to become more involved.

Duties:

- Develop and maintain our in-house construction, construction management, and HR applications. These are written in Excel, Excel VBA, Ruby on Rails, Heroku, S3, Sketchup, and Ruby for Sketchup.

- Ruby is hosted on Github. Excel and VBA are currently accessed via Sharepoint.

- One Goal is to transition all Excel & VBA to RoR

- Write clean, efficient, and well-documented code

- Conduct thorough testing and debugging of software applications

- Integrate software components and third-party APIs

- Troubleshoot and resolve software defects and issues

- Participate in code reviews to ensure code quality and adherence to coding standards

- interest in AI for productivity

Skills:

- Web Development with interest in RoR and Excel

- Experience with version control: Git and very basic Sharepoint

- Knowledge of application development methodologies and best practices

- Problem-solving and analytical skills

- Strong attention to detail and ability to prioritize tasks

If you are a junior freelance developer looking for an opportunity to work on innovative projects, we would love to hear from you. Apply now to join our dynamic team!

Job Types: Part-time, Contract

Pay: $40.00 - $50.00 per hour

Expected hours: 8 – 32 per week

Compensation package:

1099 contract
Bonus opportunities
Hourly pay
Experience level:

1 year
2 years
Schedule:

Choose your own hours
People with a criminal record are encouraged to apply

Work Location: Remote
'''

app.run(host="127.0.0.1")