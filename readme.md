#**This is tv channels and programs parser**
###**To run this you should:**
>*    1.)install required package libs:
<br />sudo apt-get install libpq-dev
>*    2:)install phantomjs(local):
<br />sudo apt-get install phantomjs
<br />(openshift with ghostdriver):
<br />cd tvparser
<br />scp required_apps/phantomjs SSH_KEY:$OPENSHIFT_DATA_DIR
<br />ssh to your openshift app
<br />cd $OPENSHIFT_DATA_DIR/phantomjs/bin
<br />chmod +x phantomjs
<br />if file '.openshift/action_hooks/post_deploy' exists and you want change ghostdriver port, 
<br />you can do it by modify .openshift/action_hooks/post_deploy file.
<br />But then you have to run 'chmod +x .openshift/action_hooks/post_deploy',
<br />if file '.openshift/action_hooks/post_deploy' does't exists you should create this one within:
<br />\#!/bin/bash
<br />nohup ${OPENSHIFT_DATA_DIR}/phantomjs/bin/phantomjs --webdriver=$OPENSHIFT_PYTHON_IP:15005 &
<br />nohup python ${OPENSHIFT_REPO_DIR}/run_scheduler.py
>*    3:)install necessary libraries:
<br />source venv/bin/activate
<br />pip instal -r requirements.txt
>*    4:)install and configure rhc tool:
<br /><https://developers.openshift.com/en/getting-started-debian-ubuntu.html#client-tools>
>*    5:)install postgresql-9.2:
<br />sudo add-apt-repository ppa:pitti/postgresql
<br />sudo apt-get update
<br />sudo apt-get install postgresql-9.2
>*    6:)CREATE DB and USER
<br />sudo -u admin psql
<br />CREATE DATABASE yandex;
<br />CREATE USER admin with password '1111';
<br />GRANT ALL privileges ON DATABASE yandex TO admin;
>*    7:)CREATE ALL SEQUENCES AND TABLES:
<br />cd sql_scripts
<br />LOCALHOST:
<br />sudo -u admin psql -d yandex -a -f SCRIPT_NAME
<br />OPENSHIFT:
<br />psql -d $PGDATABASE -a -f SCRIPT_NAME

###**Errors:**
>*    If you have problem with smtp connection, you can try:
<br />go to <https://accounts.google.com/DisplayUnlockCaptcha>
<br />and try to run program (you have 10 minutes)
