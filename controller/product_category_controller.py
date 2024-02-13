from app import app


@app.route('/prod_cats/')
def prod_cats():
    return 'products category'
