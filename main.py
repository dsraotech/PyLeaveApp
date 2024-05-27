#main.py
# https://www.youtube.com/watch?v=dam0GPOAvVI
from website import create_app  # from website directory reads the __init__.py automatically

app=create_app()

if __name__=='__main__':
    #app.run(debug=True,use_reloader=True)
    app.run(debug=True)

# To refresh then changes automatically, an environment variable has to be set
# set FLASK_ENV=development