#**This is tv channels and programs parser**
###**To run this you should:**

    1:)install phantomjs(local):
    sudo apt-get install phantomjs
    (openshift with ghostdriver):
    cd tvparser
    scp required_apps/phantomjs SSH_KEY:$OPENSHIFT_DATA_DIR
    ssh to your openshift app
    cd $OPENSHIFT_DATA_DIR/phantomjs/bin
    chmod +x phantomjs
    if you want change ghostdriver port, you can do it by modify .openshift/action_hooks/post_deploy file.
    But then you have to run 'chmod +x .openshift/action_hooks/post_deploy'
**------------------------------------------------------------------**
    2:)install necessary libraries:
    source venv/bin/activate
    pip instal -r requirements.txt
**------------------------------------------------------------------**
    3:)install and configure rhc tool:
    https://developers.openshift.com/en/getting-started-debian-ubuntu.html#client-tools

