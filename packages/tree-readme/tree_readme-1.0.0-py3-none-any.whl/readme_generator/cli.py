import click
from pathlib import Path
from readme_generator.readme_builder import build_readme

@click.command()
@click.argument("repo_path", default=".", type=click.Path(exists=True))
@click.option("--overview", default="", help="Project overview text")
def generate_readme(repo_path, overview):
    """Generates README.md with folder tree"""
    readme_content = build_readme(repo_path, overview)
    output_path = Path(repo_path) / "README.md"
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    click.echo(f"✅ README.md generated at {output_path}")

if __name__ == "__main__":
    generate_readme()