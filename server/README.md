# coding-project-template
# 1. Create Virtual Env
# 2. Activate Virual Env
#   a. source djangoenv/bin/activate
# 4. Makemigrations django app
# 5. Migrate
# 6. Docker build
#   a. Go to database
#   b. docker build . -t nodeapp
#   c. docker-compose up
#   d. Open "https://phamduchuy20-3030.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai"
# 7. IBM CE Cloud
#   a. Go to microservices
#   b. docker build . -t us.icr.io/${SN_ICR_NAMESPACE}/senti_analyzer
#   c. docker push us.icr.io/${SN_ICR_NAMESPACE}/senti_analyzer
#   d. ibmcloud ce application create --name sentianalyzer --image us.icr.io/${SN_ICR_NAMESPACE}/senti_analyzer --registry-secret icr-secret --port 5000
#   e. Use url output add in /analyze/hello to verify if it's working or not
# 8. Manage.py runserver
# 9. Go to Frontend
#   a. npm i
#   b. npm run build