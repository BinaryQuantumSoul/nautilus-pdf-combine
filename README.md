# nautilus-pdf-combine
Combine any pdfs and images using right click in Gnome nautilus

## Installation
- Install [nautilus-python](https://github.com/GNOME/nautilus-python) using package manager
- Add the python file to the extensions folder:
```shell
git clone https://github.com/BinaryQuantumSoul/nautilus-pdf-combine
cd nautilus-pdf-combine
mkdir ~/.local/share/nautilus-python
mkdir ~/.local/share/nautilus-python/extensions
cp nautilus-pdf-combine.py ~/.local/share/nautilus-python/extensions/
cd ..
rm -rf nautilus-pdf-combine
nautilus -q
```
- Make sure `pdftk` is installed

## Usage
Select any files or folders, right click > "Combine PDFs".
This will take all pdfs and images selected as well as those inside the subfolders.
The resulting `combined.pdf` file is made conctanenating the files in alphabetical path order.
