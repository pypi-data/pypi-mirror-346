import click

from cli.pmcli import generate_map, validate_file, generate_map_analyze_requirements


@click.command()
@click.version_option()
@click.pass_context
@click.argument("url")
@click.argument("nickname")
@click.argument("email")
@click.option("--action", type=click.Choice(["validate", "generate","analyze_requirements"]), required=True)
def main(
        ctx: click.Context,
        url: str,
        nickname: str,
        email: str,
        action: str,
):
    """
        CLI for validating and generating maps for files using the ProductMap API.
        """
    if url is None:
        ctx.fail("Repo/File URL is required")
    if nickname is None or nickname == "" or nickname == "null":
        nickname = "public_user"
    if email is None or email == "" or email == "null":
        email = "axel+public@product-map.ai"

    try:
        if action == "validate":
            result = validate_file(ctx, url, nickname, email)
            click.echo(result)
        elif action == "generate":
            result = generate_map(url, nickname, email)
            click.echo(result)
        elif action == "analyze_requirements":
            result = generate_map_analyze_requirements(url, nickname, email)
            click.echo(result)
    except click.ClickException as e:
        ctx.fail(f"Operation failed: {e}")


if __name__ == "__main__":
    main()
