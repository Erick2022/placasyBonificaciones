bind = "0.0.0.0:5000"
workers = 2
timeout = 120  # Aumenta el tiempo de espera del trabajador
wsgi_app = "app:app"