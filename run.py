from parser_app import init_app


app = init_app()

if __name__ == '__main__':
    app.run()
    # app.run(host='tvparser-tvonline1.rhcloud.com', port=8080)
