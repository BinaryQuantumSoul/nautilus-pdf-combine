#!/usr/bin/env python3
from gi import require_version
require_version('Gtk', '3.0')
require_version('Nautilus', '3.0')

from gi.repository import Nautilus, GObject
import os
import subprocess
import tempfile
import shutil
from PIL import Image
import mimetypes
import datetime

class PDFCombineExtension(Nautilus.MenuProvider, GObject.GObject):
    def __init__(self):
        log_dir = os.path.join(os.path.expanduser('~'), '.local/share/nautilus-python/extensions/log')
        os.makedirs(log_dir, exist_ok=True)
        log_filename = f'{os.path.basename(__file__)}.log'
        self.log_path = os.path.join(log_dir, log_filename)

        self.temp_dir = None

    def get_file_items(self, window, files):
        item = Nautilus.MenuItem(
            name="CombinePDFs",
            label="Combine PDFs",
            tip="Combines selected PDF files using pdftk"
        )
        item.connect('activate', self.combine_pdfs, files)
        return [item]

    def get_background_items(self, window, file_):
        item = Nautilus.MenuItem(
            name="CombinePDFsBackground",
            label="Combine PDFs",
            tip="Combines PDF files in the current folder using pdftk"
        )
        item.connect('activate', self.combine_pdfs, [file_])
        return [item]

    def find_files(self, files):
        paths = [file.get_location().get_path() for file in files]
        file_paths = []

        for path in paths:
            if not os.path.isdir(path):
                file_paths += [path]
            else:
                for dirpath, _, filenames in os.walk(path):
                    for filename in filenames:
                        new_path = os.path.join(dirpath, filename)
                        if not os.path.isdir(new_path):
                            file_paths += [new_path]

        pdf_files = []
        image_files = []

        for path in sorted(file_paths):
            mime, _ = mimetypes.guess_type(path)
            if not mime:
                continue
            if mime == 'application/pdf':
                pdf_files += [path]
            elif mime.startswith('image/'):
                image_files += [path]
      
        return pdf_files, image_files

    def convert_images_to_pdf(self, image_files):
        if not image_files:
            return []
        
        pdf_file_list = []
        self.temp_dir = tempfile.mkdtemp()

        for i, image_file in enumerate(image_files):
            image = Image.open(image_file)
            pdf_file_path = os.path.join(self.temp_dir, f'image_{i}.pdf')
            image.save(pdf_file_path, 'PDF')
            pdf_file_list.append(pdf_file_path)

        return pdf_file_list

    def combine_pdfs(self, menu: Nautilus.MenuItem, files):
        try:
            pdf_files, image_files = self.find_files(files)
            pdf_files += self.convert_images_to_pdf(image_files)
            if not pdf_files:
                return
            
            output_file = os.path.join(os.path.dirname(files[0].get_location().get_path()), 'combined.pdf')
            process = subprocess.Popen(['pdftk'] + pdf_files + ['cat', 'output', output_file], shell=False)

            if self.temp_dir:
                process.wait()
                shutil.rmtree(self.temp_dir, ignore_errors=True)
                self.temp_dir = None
            
        except Exception as message:
            timestamp = datetime.datetime.now().isoformat()
            with open(self.log_path, 'a') as log:
                log.write(f'{timestamp}: {message}\n')
