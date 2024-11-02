# hackng  

This is a command line tool to convert HackMD markdown files to PDF format, with the ability to download images linked in the markdown files and replace the links with the downloaded image names.

/!\ Important /!\

For now, the hackmd notes should be published or with anyone read permissions in order for the tool to download the images.

## Installation

To install the tool, you can clone the github repository:

```bash
git clone https://github.com/NonoHM/hackng.git
cd hackng
```

Using a venv or conda environment is advised:

```bash
python3 -m venv .venv
```

Install the requirements.txt with pip:

```bash
source .venv/bin/activate
pip install requirements.txt
```

For windows, the venv activation is:

```bash
./.venv/Scripts/activate.ps1
```

> Note:
> If you cannot run a powershell script, you may allow it with `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`.

## Usage

To use the tool, you can run the following command:

```bash
python hackng.py [options]
```

Where `[options]` are the following:

- `-f, --file-name`: The file name of the HackMD markdown file to convert.
- `-d, --directory`: The directory where the HackMD markdown files are located.
- `-r, --recursive`: Search for HackMD markdown files in the directory and subdirectories.
- `--replace-image-liquid`: Convert markdown images to Liquid tags (used for nonohm.io)
- `--new-base-path`: New base path for images without altering filenames (e.g., ./images -> /assets/images)
- `-nd, --no-download`: Do not download images.
- `-nl, --no-link`: Do not change links to the image's names.
- `-s, --skip`: Skip the download and link change process.
- `-pdf, --pdf-output`: Convert the markdown file to PDF format.
- `-a, --pandoc-args`: Arguments to be passed through pandoc. Hyphens are automatically added to the args.

## Example

To only download the images and change the links in `example.md` file:

```bash
python hackng.py -f ./example.md
```

The images will be downloaded in `./images/example` directory.

To convert all HackMD markdown files in a directory named `markdown_files` to PDF format and download and replace the linked images, you can run the following command:

```bash
hackmd-png-to-pdf -d ~/markdown_files -pdf [-r]
```

To convert a HackMD markdown file named `example.md` to PDF format and download and replace the linked images, you can run the following command:

```bash
python hackng.py -f ./example.md -pdf -a toc template=template.latex 
```

## Requirements

- Python 3.6 or higher
- requests
- pypandoc

## Contributions

We welcome and appreciate contributions from the community to help improve this project. If you'd like to contribute, here are a few ways you can get involved:

- Report bugs or issues you encounter while using this project
- Suggest new features or improvements
- Submit pull requests with bug fixes, new features, or other improvements
  
Before submitting a pull request, please take a moment to review our contribution guidelines to ensure a smooth and efficient process.
Thank you for your interest in contributing to this project! We look forward to working with you.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
