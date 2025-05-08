from importlib.resources import files, as_file
from ._version import __version__


def main():
    with as_file(files("ctao_sphinx_theme") / "static") as static:
        print(f"ctao-sphinx-theme v{__version__}")
        print("\nAvailable branding options:")
        for logo in sorted(static.glob("ctao_*.png")):
            if "reversed" in logo.name:
                continue

            if logo.stem == "ctao":
                branding = "ctao"
            else:
                _, _, branding = logo.stem.partition("_")

            print(f"  {branding}")


if __name__ == "__main__":
    main()
