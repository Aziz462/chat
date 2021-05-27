from pyngrok import ngrok


def create_tunnel():
    tunnel = ngrok.connect(5000)
    return tunnel
