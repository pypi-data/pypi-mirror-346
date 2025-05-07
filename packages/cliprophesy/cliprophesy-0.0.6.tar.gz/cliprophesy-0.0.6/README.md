# cliprophesy

A CLI tool that suggests commands based on your shell history.

## Local development

* Deploying
** rm -rf build/
** python -m build
** python3 -m twine upload --repository testpypi dist/* --verbose

* Developing
** PYTHONPATH=. python cliprophesy/main.py <command> # run from /src
** Use absolute imports

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
