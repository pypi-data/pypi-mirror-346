from wordpress_poster.utils import clean_filename

def test_clean_filename_basic():
    assert clean_filename('test.jpg') == 'test.jpg'
    assert clean_filename('my-file.png') == 'my-file.png'
    assert clean_filename('file name with spaces.txt') == 'file-name-with-spaces.txt'

def test_clean_filename_special_chars():
    assert clean_filename('a@b#c$d%e^f&g*h(i)j!.txt') == 'a-b-c-d-e-f-g-h-i-j-.txt'
    assert clean_filename('üñîçødë.txt') == '-----d-.txt'
    assert clean_filename('file[1].txt') == 'file-1-.txt'

def test_clean_filename_empty():
    assert clean_filename('') == '' 