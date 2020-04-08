from flask import request, session

def home():
    print(request)
    # print(session['item'], 'session item is here')
    import pdb; pdb.set_trace()
    return "Hello World"