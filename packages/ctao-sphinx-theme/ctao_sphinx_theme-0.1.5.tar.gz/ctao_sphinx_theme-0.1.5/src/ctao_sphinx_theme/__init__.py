from pathlib import Path
import shutil

from ._version import __version__

__all__ = [
    "__version__",
    "setup",
]

THEME_BASE = Path(__file__).resolve().parent


def copy_logos(app, exc):
    if app.builder.format == "html" and not exc:
        static_dir = app.outdir / "_static"
        static_dir.mkdir(exist_ok=True, parents=True)

        for k in ("image_light", "image_dark"):
            logo = app.config["html_theme_options"]["logo"][k]
            shutil.copyfile(logo, static_dir / Path(logo).name)


def update_config(app):
    branding = app.config.html_theme_options.get("branding", "ctao")

    if branding in ("ctao", ""):
        logo = "ctao"
    else:
        logo = f"ctao_{branding}"

    logos = THEME_BASE / "ctao-logos"
    logo_light = logos / f"{logo}.png"
    logo_dark = logos / f"{logo}_reversed.png"

    if not logo_light.is_file():
        raise ValueError(f"Invalid branding option '{branding}'")

    logo_config = dict(
        image_light=str(logo_light),
        image_dark=str(logo_dark),
        alt_text="ctao-logo",
    )

    if "logo" in app.config.html_theme_options:
        app.config.html_theme_options["logo"].update(logo_config)
    else:
        app.config.html_theme_options["logo"] = logo_config

    app.config["html_favicon"] = str(THEME_BASE / "static/ctao-favicon.png")


def setup(app):
    app.add_html_theme("ctao", THEME_BASE)
    app.connect("builder-inited", update_config)
    app.connect("build-finished", copy_logos)
