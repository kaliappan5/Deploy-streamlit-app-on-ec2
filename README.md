# Deploy-streamlit-app-on-ec2
# How to Deploy stream lit app on EC2 machine
1. Login to AWS Console and launch ec2 machine
2. Run the following commands

Note: Do the port mapping to this port: 8501

sudo get update

sudo apt get update

sudo apt upgrade -y

sudo apt install git curl unzip tar make sudo vim wget -y

sudo apt install git curl unzip tar make sudo vim wget -y

git clone "our repository"

sudo apt install python3-pip

pip3 install -r requirements.txt

# temperory running
python3 -m streamlit run app.py

#Permanent running
nohup python3 -m streamlit run app.py
