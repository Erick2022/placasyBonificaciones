bind = "0.0.0.0:5000"
workers = 4
timeout = 120  # Aumenta el tiempo de espera del trabajador
wsgi_app = "app:app"