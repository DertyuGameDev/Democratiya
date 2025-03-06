from flask import Flask, url_for

app = Flask(__name__)


@app.route('/')
def main():
    return ''


@app.route('/carousel')
def carousel():
    return f'''<!DOCTYPE html>
    <html lang="en">
    <head>
      <title>Пейзажи Марса</title>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/css/bootstrap.min.css" rel="stylesheet">
      <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js" 
              integrity="sha384-IQsoLXl5PILFhosVNubq5LC7Qb9DXgDA9i+tQ8Zj3iwWAwPtgFTxbJ8NT4GN1R8p" 
              crossorigin="anonymous"></script>
      <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/js/bootstrap.min.js" 
              integrity="sha384-Atwg2Pkwv9vp0ygtn1JAojH0nYbwNJLPhwyoVbhoPwBhjQPR5VtM2+xf0Uwh9KtT" 
              crossorigin="anonymous"></script>
        <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
    </head>
    
    
    <body class="body">
    <h1 align="center">Пейзажи Марса</h1>
    <div id="carouselExampleDark" class="carousel carousel-dark slide">
      <div class="carousel-indicators">
        <button type="button" data-bs-target="#carouselExampleDark" data-bs-slide-to="0" class="active" 
                aria-current="true" aria-label="Slide 1"></button>
        <button type="button" data-bs-target="#carouselExampleDark" data-bs-slide-to="1" 
                aria-label="Slide 2"></button>
        <button type="button" data-bs-target="#carouselExampleDark" data-bs-slide-to="2" 
                aria-label="Slide 3"></button>
      </div>
      <div class="carousel-inner">
        <div class="carousel-item active" data-bs-interval="10000">
          <img src="{url_for('static', filename='img/mars3.jpg')}" class="d-block w-100" alt="...">
          <div class="carousel-caption d-none d-md-block">
            <h5>Хз как это описать, сами подумайте</h5>
          </div>
        </div>
        <div class="carousel-item" data-bs-interval="2000">
          <img src="{url_for('static', filename='img/mars1.png')}" class="d-block w-100" alt="...">
          <div class="carousel-caption d-none d-md-block">
            <h5>Ну, эт Марс</h5>
          </div>
        </div>
        <div class="carousel-item">
          <img src="{url_for('static', filename='img/mars2.jpg')}" class="d-block w-100" alt="...">
          <div class="carousel-caption d-none d-md-block">
            <h5>Красота ляпота</h5>
          </div>
        </div>
      </div>
      <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleDark" 
              data-bs-slide="prev">
        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Previous</span>
      </button>
      <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleDark" 
              data-bs-slide="next">
        <span class="carousel-control-next-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Next</span>
      </button>
    </div>
    
    </body>
    </html>'''


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
