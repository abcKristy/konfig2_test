import pytest
from terminal import MyTerminal
from zipfile import ZipFile
from window_mode import Window


@pytest.fixture
def terminal():
    fs_path = 'my_zip_tes.zip'
    t = MyTerminal(ZipFile(fs_path, 'a'))
    return t


@pytest.fixture
def empty_terminal():
    return MyTerminal(None)


def test_init_1(terminal):
    assert terminal.window is None


def test_init_2(terminal):
    assert terminal.fs is not None


def test_init_3(empty_terminal):
    assert empty_terminal.fs is None


def test_attach_1(empty_terminal):
    assert empty_terminal.window is None


def test_attach_2(terminal):
    terminal.attach(Window(terminal))
    assert terminal.window is not None


def test_start_polling_1(terminal, monkeypatch, capfd):
    inp = ['exit']

    def my_input(arg, *args, **kwargs):
        return inp.pop()

    monkeypatch.setattr('builtins.input', my_input)
    terminal.start_polling()
    out, err = capfd.readouterr()
    assert out == 'stop polling...\n'


def test_cd_1(terminal):
    assert terminal.cd([]) == ''


def test_cd_2(terminal):
    assert terminal.cd(['desktop/..']) == ''


def test_cd_3(terminal):
    assert terminal.cd(['desktop']) == 'desktop/'


def test_ls_1(terminal):
    assert all(i in terminal.ls([]) for i in "1 desktop hello img.png my.txt user".split())


def test_ls_2(terminal):
    terminal.cur_d = terminal.cd(['user'])
    assert all(i in terminal.ls([]) for i in "me secrets.txt top_secret.txt".split())


def test_ls_3(terminal):
    assert all(i in terminal.ls(['user']) for i in "me secrets.txt top_secret.txt".split())


def test_cat_1(terminal):
    assert terminal.cat('1') == ''


def test_cat_2(terminal):
    assert terminal.cat(['user/secrets.txt']) == """я программирую на python
а ещё на Джаве
а ещё на cc++"""


def test_cat_3(terminal):
    terminal.cur_d = terminal.cd(['user'])
    assert terminal.cat(['secrets.txt']) == """я программирую на python
а ещё на Джаве
а ещё на cc++"""


def test_head_1(terminal):
    assert terminal.head('1') == ''


def test_head_2(terminal):
    assert terminal.head(['user/secrets.txt']) == """я программирую на python
а ещё на Джаве
а ещё на cc++"""


def test_head_3(terminal):
    terminal.cur_d = terminal.cd(['user'])
    assert terminal.head(['secrets.txt']) == """я программирую на python
а ещё на Джаве
а ещё на cc++"""


def test_head_4(terminal):
    terminal.cur_d = terminal.cd(['user'])
    assert terminal.head(['-2', 'secrets.txt']) == """я программирую на python
а ещё на Джаве"""


def test_touch_1(terminal, capfd):
    terminal.touch([])
    out, err = capfd.readouterr()
    assert out == 'Не указано имя файла\n'


def test_touch_2(terminal, capfd):
    terminal.touch(['/\\'])
    out, err = capfd.readouterr()
    assert out == 'Не удалось создать файл\n'


def test_touch_3(terminal, capfd):
    terminal.touch(['test.txt'])
    out, err = capfd.readouterr()
    assert out == ''
