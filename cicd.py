import subprocess
import smtplib
from email.mime.text import MIMEText
import requests

IMAGE = "devopssteps/node-demo:latest"
CONTAINER = "node-demo"
#SLACK_WEBHOOK = "my-slack-url"
SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK")

def run_cmd(cmd):
    subprocess.check_call(cmd, shell=True)

def docker_build_push():
    run_cmd(f"docker build -t {IMAGE} .")
    run_cmd(f"docker push {IMAGE}")

def docker_deploy():
    run_cmd(f"docker rm -f {CONTAINER} || true")
    run_cmd(f"docker run -d --name {CONTAINER} -p 3000:3000 {IMAGE}")

def slack_notify(msg):
    requests.post(SLACK_WEBHOOK, json={"text": msg})

def email_notify(msg):
    sender = "rajiv19831@gmail.com"
    receiver = "rajiv19831@gmail.com"

    email = MIMEText(msg)
    email["Subject"] = "CI/CD Pipeline Status"
    email["From"] = sender
    email["To"] = receiver

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender, "aaaa")
        server.send_message(email)

if __name__ == "__main__":
    try:
        docker_build_push()
        docker_deploy()
        slack_notify("✅ Docker App Deployed Successfully")
        #email_notify("Pipeline SUCCESS: App deployed")
    except Exception as e:
        slack_notify(f"❌ Pipeline Failed: {e}")
        #email_notify(f"Pipeline FAILED: {e}")
        raise
