import os
import shutil
import stat
import click
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

from splent_cli.utils.path_utils import PathUtils

def pascalcase(s):
    return "".join(word.capitalize() for word in s.split("_"))


def setup_jinja_env():
    env = Environment(
        loader=FileSystemLoader(searchpath=PathUtils.get_splent_cli_templates_dir()),
        autoescape=select_autoescape(["html", "xml", "j2"]),
    )
    env.filters["pascalcase"] = pascalcase
    return env

def render_and_write_file(env, template_name, filename, context):
    content = env.get_template(template_name).render(context) + "\n"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        f.write(content)

@click.command("product:create", help="Creates a new product with a given name.")
@click.argument("name")
@click.option("--features-file", type=click.Path(exists=True), help="Path to features.txt")
def make_product(name, features_file):
    env = setup_jinja_env()
    context = {
        "product_name": name,
        "pascal_name": pascalcase(name)
    }

    base_path = os.path.join(PathUtils.get_working_dir(), name)
    src_path = os.path.join(base_path, "src", name)

    if os.path.exists(base_path):
        click.echo(click.style(f"The product '{name}' already exists.", fg="red"))
        return

    # Crear carpetas base
    for subdir in ["entrypoints", "scripts", f"src/{name}"]:
        os.makedirs(os.path.join(base_path, subdir), exist_ok=True)
    open(os.path.join(base_path, "src", "__init__.py"), "a").close()

    # Archivos desde plantillas
    files_and_templates = {
        "entrypoints/dev_entrypoint.sh": "product/product_dev_entrypoint.sh.j2",
        "scripts/00_install_features.sh": "product/product_00_install_features.sh.j2",
        "scripts/01_compile_assets.sh": "product/product_01_compile_assets.sh.j2",
        "scripts/02_0_db_wait_connection.sh": "product/product_02_0_db_wait_connection.sh.j2",
        "scripts/02_1_db_create_db_test.sh": "product/product_02_1_db_create_db_test.sh.j2",
        "scripts/03_initialize_migrations.sh": "product/product_03_initialize_migrations.sh.j2",
        "scripts/04_handle_migrations.sh": "product/product_04_handle_migrations.sh.j2",
        "scripts/05_0_start_app_dev.sh": "product/product_05_0_start_app_dev.sh.j2",
        "README.md": "product/product_README.md.j2",
        "pyproject.toml": "product/product_pyproject.toml.j2",
        "features.txt": "product/product_features.txt.j2",
        "LICENSE": "product/product_LICENSE.j2",
        "package.json": "product/product_package.json.j2",
        ".gitignore": "product/product_.gitignore.j2",
        f"src/{name}/__init__.py": "product/product_init.py.j2",

    }

    for rel_path, tpl in files_and_templates.items():
        abs_path = os.path.join(base_path, rel_path)
        if tpl:
            render_and_write_file(env, tpl, abs_path, context)
        else:
            if features_file:
                os.makedirs(os.path.dirname(abs_path), exist_ok=True)
                shutil.copy(features_file, abs_path)
                
    # Cambiar permisos y propietario
    uid = 1000
    gid = 1000

    os.chown(base_path, uid, gid)
    os.chmod(base_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IROTH | stat.S_IXOTH)

    for root, dirs, files in os.walk(base_path):
        for d in dirs:
            dir_path = os.path.join(root, d)
            os.chown(dir_path, uid, gid)
            os.chmod(dir_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IROTH | stat.S_IXOTH)
        for f in files:
            file_path = os.path.join(root, f)
            os.chown(file_path, uid, gid)
            os.chmod(
                file_path,
                stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH,
            )

    click.echo(click.style(f"✅ Product '{name}' created successfully in {base_path}", fg="green"))
