from pyngrok import ngrok


def create_tunnel():
    tunnel = ngrok.connect(5000)
    print(tunnel.public_url)
    return tunnel
