from app import app


@app.route('/products/')
def products():
    return 'products'
