import radon.complexity as cyclomatic_complexity_module
from radon import cli


def get_cyclomatic_complexity_configuration() -> (
    cli.Config
):
    order = (
        cyclomatic_complexity_module.SCORE
    )

    configuration = cli.Config(
        min="A",
        max="F",
        exclude=None,
        ignore=None,
        show_complexity=False,
        average=False,
        order=order,
        no_assert=False,
        total_average=False,
        show_closures=False,
        include_ipynb=False,
        ipynb_cells=False,
    )

    return configuration
