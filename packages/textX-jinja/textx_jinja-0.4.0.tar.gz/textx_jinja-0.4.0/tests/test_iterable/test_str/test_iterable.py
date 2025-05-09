"""
Test generating set of files when filename includes variable that is iterable.
"""
import os
import shutil
from textxjinja import textx_jinja_generator


class Model():

    def __init__(self, name, text):
        self.name = name
        self.text = text

    def __str__(self):
        return self.name


def test_iterable():
    this_folder = os.path.dirname(__file__)
    template_folder = os.path.join(this_folder, 'templates')
    output_folder = os.path.join(this_folder, 'output')

    # Remove output folder
    try:
        shutil.rmtree(output_folder)
    except OSError:
        pass

    first = Model('first', 'first file text')
    second = Model('second', 'second file text')
    #
    # Prepare config
    config = {}
    config['models'] = [first, second]
    config['root'] = '-root-'

    # Generate
    textx_jinja_generator(template_folder, output_folder, config, overwrite=True)

    # Assert both files are present
    first = os.path.join(output_folder, 'first.txt')
    second = os.path.join(output_folder, 'second.txt')
    assert os.path.exists(first)
    assert os.path.exists(second)

    # Test the content
    with open(first, 'r') as f:
        first_content = f.read()
        assert 'some content' in first_content
        assert 'text is \'first file text\'' in first_content

    with open(second, 'r') as f:
        second_content = f.read()
        assert 'some content' in second_content
        assert 'text is \'second file text\'' in second_content
