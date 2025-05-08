from radon import cli


def get_maintainability_index_configuration() -> (
    cli.Config
):
    configuration = cli.Config(
        min="A",
        max="C",
        exclude=None,
        ignore=None,
        show=True,
        multi=False,
        sort=False,
        include_ipynb=False,
        ipynb_cells=False,
    )

    return configuration
