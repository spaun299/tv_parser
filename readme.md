#**This is tv channels and programs parser**
###**To run this you should:**
    1:)install required package libs:
    sudo apt-get install libpq-dev
    2:)install phantomjs(local):
    sudo apt-get install phantomjs
    (openshift with ghostdriver):
    cd tvparser
    scp required_apps/phantomjs SSH_KEY:$OPENSHIFT_DATA_DIR
    ssh to your openshift app
    cd $OPENSHIFT_DATA_DIR/phantomjs/bin
    chmod +x phantomjs
    if file '.openshift/action_hooks/post_deploy' exists and you want change ghostdriver port, 
    you can do it by modify .openshift/action_hooks/post_deploy file.
    But then you have to run 'chmod +x .openshift/action_hooks/post_deploy'
    if file '.openshift/action_hooks/post_deploy' does't exists you should create this one within:
    **
    #!/bin/bash
    nohup ${OPENSHIFT_DATA_DIR}/phantomjs/bin/phantomjs --webdriver=$OPENSHIFT_PYTHON_IP:15005 &
    **
    3:)install necessary libraries:
    source venv/bin/activate
    pip instal -r requirements.txt
    4:)install and configure rhc tool:
    https://developers.openshift.com/en/getting-started-debian-ubuntu.html#client-tools
    5:)install postgresql-9.2:
    sudo add-apt-repository ppa:pitti/postgresql
    sudo apt-get update
    sudo apt-get install postgresql-9.2
    6:)CREATE DB and USER
    sudo -u postgres psql
    CREATE DATABASE yandex;
    CREATE USER admin with password '1111';
    GRANT ALL privileges ON DATABASE yandex TO admin;
    7:)CREATE ALL SEQUENCES AND TABLES:
    cd sql_scripts
    sudo -u admin psql -d yandex -a -f SCRIPT_NAME
