"""
Test basic code generation from a set of files.
"""
import os
import shutil
from textxjinja import textx_jinja_generator


class Model:
    first = "This is first"
    second = "This is second"
    some_list = [1, 2, 3]


def test_basic():
    this_folder = os.path.dirname(__file__)
    template_folder = os.path.join(this_folder, 'templates')
    output_folder = os.path.join(this_folder, 'output')

    # Remove output folder
    try:
        shutil.rmtree(output_folder)
    except OSError:
        pass

    # Prepare config
    config = {}
    config['model'] = Model
    config['root'] = '-root-'

    # Generate
    textx_jinja_generator(template_folder, output_folder, config, overwrite=True)

    # Assert both files are present
    first = os.path.join(output_folder, 'first.txt')
    second = os.path.join(output_folder, 'second')
    assert os.path.exists(first)
    assert os.path.exists(second)

    # Test the content
    with open(first, 'r') as f:
        first_content = f.read()
        assert 'This is a simple template.' in first_content
        assert 'root = -root-' in first_content
        assert 'first = This is first' in first_content

    with open(second, 'r') as f:
        second_content = f.read()
        assert 'i = 1' in second_content
        assert 'i = 3' in second_content
