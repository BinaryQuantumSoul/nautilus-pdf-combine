# nautilus-pdf-combine
Combine any pdfs and images using right click in Gnome Nautilus

## Usage
Select any files or folders, right click > "Combine PDFs".
This will take all pdfs and images selected as well as those inside the subfolders.
The resulting `combined.pdf` file is made concatenating the files in alphabetical path order.

## Installation
1. Install [nautilus-python](https://github.com/GNOME/nautilus-python) using package manager
1. Make sure `pdftk` is installed
1. Add the python file to the extensions folder, shell script for the lazy ones:
  ```shell
  mkdir ~/.local/share/nautilus-python
  mkdir ~/.local/share/nautilus-python/extensions
  cd ~/.local/share/nautilus-python/extensions
  wget https://raw.githubusercontent.com/BinaryQuantumSoul/nautilus-pdf-combine/refs/heads/main/nautilus-pdf-combine.py
  nautilus -q
  ```
