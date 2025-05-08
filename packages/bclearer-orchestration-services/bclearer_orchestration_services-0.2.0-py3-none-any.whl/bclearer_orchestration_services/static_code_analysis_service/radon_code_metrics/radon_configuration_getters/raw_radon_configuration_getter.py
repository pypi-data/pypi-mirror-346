from radon import cli


def get_raw_configuration() -> (
    cli.Config
):
    configuration = cli.Config(
        exclude=None,
        ignore=None,
        summary=True,
        include_ipynb=False,
        ipynb_cells=False,
    )

    return configuration
