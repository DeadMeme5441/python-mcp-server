from ._server_impl import create_app


def cli():
    app = create_app()
    app.run(transport="http", host=app._host, port=app._port)  # type: ignore[attr-defined]


if __name__ == "__main__":
    cli()

