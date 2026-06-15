import google.generativeai as genai
import os 
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

filepath = "input/client.txt"
specpath = "input/spec.txt"

def readcontent(file):

    try:
        with open(file, "r") as file:
            content = file.read()
        if not content:
            raise ValueError(f"{file} is empty")
        return content
    
    except FileNotFoundError:
        raise FileNotFoundError(f"The required file {file} is not available") 

def generate_email(clientrequirements, specfile):

    prompt = f"""

    You are a senior software developer with expertise in building backend systems.
    We have a client with a set of requirements regarding a new project that we have to build 
    from scratch. \n

    The client requirements are as follows : {clientrequirements} \n

    The spec file is as follows : {specfile} \n

    Generate the final structured response.
    """

    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel("gemini-3.5-flash")
        response = model.generate_content(prompt)

        return response.text
    
    except:
        raise RuntimeError("API call failed")
    

def send_email(sender_email, receiver_email, app_password, body):

    try:

        message = MIMEMultipart()

        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = "Client Requirement Analysis"

        message.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()

        print("Email sent successfully")

    except Exception as e:
        raise RuntimeError(f"Failed to send email: {e}")



clientrequirements = readcontent(filepath)
specfile = readcontent(specpath)

print(clientrequirements, specfile)

content = generate_email(clientrequirements, specfile)

print(content)
mailbody = f"""

        Dear Client, 

        Thank you for sharing your requirements for the Smart Society / Apartment 
        Management System. We have reviewed your brief and prepared a structured 
        analysis document for your reference.

        Kindly review the following sections covering our understanding of your 
        requirements, potential risks, and a few clarification questions at the end 
        that we would appreciate your input on before we proceed further.

        {content}

        We look forward to your response. Feel free to reach out any time necessary.
        Regards,
        Preetam.


"""

with open("output/analysis.txt", "w") as file:
    file.write(content)

send_email(sender_email = "kspreetam2608@gmail.com",
    receiver_email = "preetamkommavarapu@gmail.com",
    app_password = 'ncdepmoqmdvqcbmj', body = mailbody
)



