"""
Test generating project with layered folder structure
"""
import os
import shutil
from textxjinja import textx_jinja_generator


def test_folder_structure():
    this_folder = os.path.dirname(__file__)
    template_folder = os.path.join(this_folder, 'templates')
    output_folder = os.path.join(this_folder, 'output')

    # Remove output folder
    try:
        shutil.rmtree(output_folder)
    except OSError:
        pass

    # Prepare config
    config = {'text': '-textx-'}

    # Generate
    textx_jinja_generator(template_folder, output_folder, config, overwrite=True)

    # Assert both files are present
    first = os.path.join(output_folder, 'base', 'first_dir', 'file.txt')
    second = os.path.join(output_folder, 'base', 'second_dir', 'file.txt')
    assert os.path.exists(first)
    assert os.path.exists(second)

    # Test the content
    with open(first, 'r') as f:
        first_content = f.read()
        assert '-textx-' in first_content

    with open(second, 'r') as f:
        second_content = f.read()
        assert 'Some text here.' in second_content
