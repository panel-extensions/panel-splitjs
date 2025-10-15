import pytest

pytest.importorskip('playwright')

from panel.tests.util import serve_component, wait_until
from panel.widgets import Button
from panel_splitjs import MultiSplit, Split
from playwright.sync_api import expect

pytestmark = pytest.mark.ui

@pytest.mark.parametrize('orientation', ['horizontal', 'vertical'])
def test_split(page, orientation):
    split = Split(Button(name='Left'), Button(name='Right'), orientation=orientation)
    serve_component(page, split)
    expect(page.locator('.split-panel')).to_have_count(2)
    expect(page.locator('.content-wrapper')).to_have_count(2)
    expect(page.locator('.single-split')).to_have_class(f'split single-split {orientation}')

    expect(page.locator('.bk-btn')).to_have_count(2)
    expect(page.locator('.bk-btn').first).to_have_text('Left')
    expect(page.locator('.bk-btn').last).to_have_text('Right')

    attr = "width" if orientation == "horizontal" else "height"
    expect(page.locator('.split-panel').first).to_have_attribute('style', f'{attr}: calc(50% - 4px);')
    expect(page.locator('.split-panel').last).to_have_attribute('style', f'{attr}: calc(50% - 4px);')


def test_split_sizes(page):
    split = Split(Button(name='Left'), Button(name='Right'), sizes=(40, 60), width=400)
    serve_component(page, split)

    expect(page.locator('.split-panel')).to_have_count(2)
    expect(page.locator('.split-panel').first).to_have_attribute('style', 'width: calc(40% - 4px);')
    expect(page.locator('.split-panel').last).to_have_attribute('style', 'width: calc(60% - 4px);')


@pytest.mark.parametrize('orientation', ['horizontal', 'vertical'])
def test_split_drag_gutter(page, orientation):
    kwargs = {'width': 400} if orientation == 'horizontal' else {'height': 400}
    split = Split(Button(name='Left'), Button(name='Right'), orientation=orientation, **kwargs)
    serve_component(page, split)

    expect(page.locator('.gutter')).to_have_count(1)
    gutter_box = page.locator('.gutter').bounding_box()
    x, y = gutter_box['x'], gutter_box['y']
    dx, dy = (100, 0) if orientation == 'horizontal' else (0, 100)
    page.locator('.gutter').hover()
    page.mouse.down()
    page.mouse.move(x + dx, y + dy)
    page.mouse.up()

    attr = "width" if orientation == "horizontal" else "height"
    expect(page.locator('.split-panel').first).to_have_attribute('style', f'{attr}: calc(74% - 4px);')
    expect(page.locator('.split-panel').last).to_have_attribute('style', f'{attr}: calc(26% - 4px);')

    wait_until(lambda: split.sizes == (74, 26), page)


def test_split_collapsed_programmatically(page):
    split = Split(Button(name='Left'), Button(name='Right'), expanded_sizes=(40, 60), width=400)
    serve_component(page, split)

    split.collapsed = 0
    expect(page.locator('.split-panel').first).to_have_attribute('style', 'width: calc(1% - 4px);')
    expect(page.locator('.split-panel').last).to_have_attribute('style', 'width: calc(99% - 4px);')
    wait_until(lambda: split.sizes == (0, 100), page)
    wait_until(lambda: split.collapsed == 0, page)

    split.collapsed = 1
    expect(page.locator('.split-panel').first).to_have_attribute('style', 'width: calc(99% - 4px);')
    expect(page.locator('.split-panel').last).to_have_attribute('style', 'width: calc(1% - 4px);')
    wait_until(lambda: split.sizes == (100, 0), page)
    wait_until(lambda: split.collapsed == 1, page)

    split.collapsed = None
    expect(page.locator('.split-panel').first).to_have_attribute('style', 'width: calc(40% - 4px);')
    expect(page.locator('.split-panel').last).to_have_attribute('style', 'width: calc(60% - 4px);')
    wait_until(lambda: split.sizes == (40, 60), page)
    wait_until(lambda: split.collapsed is None, page)


def test_split_sizes_programmatically(page):
    split = Split(Button(name='Left'), Button(name='Right'), width=400)
    serve_component(page, split)

    split.sizes = (20, 80)
    expect(page.locator('.split-panel').first).to_have_attribute('style', 'width: calc(20% - 4px);')
    expect(page.locator('.split-panel').last).to_have_attribute('style', 'width: calc(80% - 4px);')
    wait_until(lambda: split.sizes == (20, 80), page)


@pytest.mark.parametrize('orientation', ['horizontal', 'vertical'])
def test_split_click_toggle_button(page, orientation):
    kwargs = {'width': 400} if orientation == 'horizontal' else {'height': 400}
    split = Split(Button(name='Left'), Button(name='Right'), orientation=orientation, **kwargs)
    serve_component(page, split)

    btn1, btn2 = ("left", "right") if orientation == "horizontal" else ("up", "down")
    expect(page.locator(f'.toggle-button-{btn1}')).to_have_count(1)
    expect(page.locator(f'.toggle-button-{btn2}')).to_have_count(1)

    attr = "width" if orientation == "horizontal" else "height"
    page.locator(f'.toggle-button-{btn1}').click()
    expect(page.locator('.split-panel').first).to_have_attribute('style', f'{attr}: calc(1% - 4px);')
    expect(page.locator('.split-panel').last).to_have_attribute('style', f'{attr}: calc(99% - 4px);')
    wait_until(lambda: split.sizes == (0, 100), page)
    wait_until(lambda: split.collapsed == 0, page)

    page.locator(f'.toggle-button-{btn2}').click()
    expect(page.locator('.split-panel').first).to_have_attribute('style', f'{attr}: calc(50% - 4px);')
    expect(page.locator('.split-panel').last).to_have_attribute('style', f'{attr}: calc(50% - 4px);')
    wait_until(lambda: split.sizes == (50, 50), page)
    wait_until(lambda: split.collapsed == None, page)

    page.locator(f'.toggle-button-{btn2}').click()
    expect(page.locator('.split-panel').first).to_have_attribute('style', f'{attr}: calc(99% - 4px);')
    expect(page.locator('.split-panel').last).to_have_attribute('style', f'{attr}: calc(1% - 4px);')
    wait_until(lambda: split.sizes == (100, 0), page)
    wait_until(lambda: split.collapsed == 1, page)


@pytest.mark.parametrize('orientation', ['horizontal', 'vertical'])
def test_multi_split(page, orientation):
    kwargs = {'width': 400} if orientation == 'horizontal' else {'height': 400}
    split = MultiSplit(Button(name='Left'), Button(name='Middle'), Button(name='Right'), orientation=orientation, **kwargs)
    serve_component(page, split)
    expect(page.locator('.split-panel')).to_have_count(3)
    expect(page.locator('.split')).to_have_class(f'split multi-split {orientation}')

    expect(page.locator('.bk-btn').first).to_have_text('Left')
    expect(page.locator('.bk-btn').nth(1)).to_have_text('Middle')
    expect(page.locator('.bk-btn').last).to_have_text('Right')

    attr = "width" if orientation == "horizontal" else "height"
    expect(page.locator('.split-panel').first).to_have_attribute('style', f'{attr}: calc(33.3333% - 4px);')
    expect(page.locator('.split-panel').nth(1)).to_have_attribute('style', f'{attr}: calc(33.3333% - 8px);')
    expect(page.locator('.split-panel').last).to_have_attribute('style', f'{attr}: calc(33.3333% - 4px);')
