import pytest

pytest.importorskip('playwright')

from panel.tests.util import serve_component, wait_until
from panel.pane import Markdown
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

def test_split_replace_panel(page):
    split = Split(Markdown("LEFT"), Markdown("RIGHT"))
    serve_component(page, split)

    expect(page.locator(".markdown").first).to_have_text("LEFT")
    expect(page.locator(".markdown").last).to_have_text("RIGHT")

    split[0] = Markdown("CHANGED LEFT")
    expect(page.locator(".markdown").first).to_have_text("CHANGED LEFT")

@pytest.mark.parametrize('orientation', ['horizontal', 'vertical'])
def test_split_min_size_and_total_width(page, orientation):
    split = Split(
        Markdown("## Left Panel\nContent here", width=150, margin=25),
        Markdown("## Right Panel\nMore content", width=150, margin=25),
        sizes=(50, 50),  # Equal sizing initially
        min_size=300,    # Minimum 300px for each panel
        show_buttons=True,
        orientation=orientation
    )
    serve_component(page, split)

    # Check total width/height is 608px
    attr = "width" if orientation == "horizontal" else "height"
    expect(page.locator(".single-split")).to_have_attribute("style", f"min-{attr}: 608px;")

    # Collapse left panel using the left button
    left_button = page.locator(".toggle-button-left,.toggle-button-up").first
    left_button.click()
    # Wait to ensure UI has updated; the left panel should not collapse below min_size=300px,
    # so after collapse, its width/height should be 300px.
    expect(page.locator(".split-panel").first).to_have_css(attr, "300px")

    # Collapse right panel using the right button
    right_button = page.locator(".toggle-button-right,.toggle-button-down").first
    right_button.click()
    # Wait, then check right does not collapse below 300px
    expect(page.locator(".split-panel").last).to_have_css(attr, "300px")

@pytest.mark.parametrize('orientation', ['horizontal', 'vertical'])
def test_split_min_size_one_side(page, orientation):
    # Only first panel has a min_size of 300px, second is unconstrained
    split = Split(
        Markdown("## Left", width=150),
        Markdown("## Right", width=150),
        sizes=(50, 50),
        min_size=(300, None),
        show_buttons=True,
        orientation=orientation,
        width=600 if orientation == "horizontal" else None,
        height=600 if orientation == "vertical" else None
    )
    serve_component(page, split)

    attr = "width" if orientation == "horizontal" else "height"
    # The minimum size style is still 308px (because None becomes 0, so 300+0+8)
    expect(page.locator(".single-split")).to_have_attribute("style", f"min-{attr}: 308px;")

    # Collapse left panel -- it should not collapse below 300px
    left_button = page.locator(".toggle-button-left,.toggle-button-up").first
    left_button.click()
    expect(page.locator(".split-panel").first).to_have_css(attr, "300px")

    # Collapse right panel -- right can collapse to minimum, which is 5px (default collapsed size)
    right_button = page.locator(".toggle-button-right,.toggle-button-down").first
    right_button.click()
    # The right panel should be collapsed to zero
    expect(page.locator(".split-panel").last).to_have_css(attr, "0px")

    # The left panel still stays at its min_size
    expect(page.locator(".split-panel").first).to_have_css(attr, "592px")


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
    wait_until(lambda: split.sizes == (1, 99), page)
    wait_until(lambda: split.collapsed == 0, page)

    split.collapsed = 1
    expect(page.locator('.split-panel').first).to_have_attribute('style', 'width: calc(99% - 4px);')
    expect(page.locator('.split-panel').last).to_have_attribute('style', 'width: calc(1% - 4px);')
    wait_until(lambda: split.sizes == (99, 1), page)
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
    split = Split(Button(name='Left'), Button(name='Right'), orientation=orientation, show_buttons=True, **kwargs)
    serve_component(page, split)

    btn1, btn2 = ("left", "right") if orientation == "horizontal" else ("up", "down")
    expect(page.locator(f'.toggle-button-{btn1}')).to_have_count(1)
    expect(page.locator(f'.toggle-button-{btn2}')).to_have_count(1)

    attr = "width" if orientation == "horizontal" else "height"
    page.locator(f'.toggle-button-{btn1}').click()
    expect(page.locator('.split-panel').first).to_have_attribute('style', f'{attr}: calc(1% - 4px);')
    expect(page.locator('.split-panel').last).to_have_attribute('style', f'{attr}: calc(99% - 4px);')
    wait_until(lambda: split.sizes == (1, 99), page)
    wait_until(lambda: split.collapsed == 0, page)

    page.locator(f'.toggle-button-{btn2}').click()
    expect(page.locator('.split-panel').first).to_have_attribute('style', f'{attr}: calc(50% - 4px);')
    expect(page.locator('.split-panel').last).to_have_attribute('style', f'{attr}: calc(50% - 4px);')
    wait_until(lambda: split.sizes == (50, 50), page)
    wait_until(lambda: split.collapsed == None, page)

    page.locator(f'.toggle-button-{btn2}').click()
    expect(page.locator('.split-panel').first).to_have_attribute('style', f'{attr}: calc(99% - 4px);')
    expect(page.locator('.split-panel').last).to_have_attribute('style', f'{attr}: calc(1% - 4px);')
    wait_until(lambda: split.sizes == (99, 1), page)
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

def test_multi_split_replace_panel(page):
    split = MultiSplit(Markdown("LEFT"), Markdown("MIDDLE"), Markdown("RIGHT"))
    serve_component(page, split)

    expect(page.locator(".markdown").first).to_have_text("LEFT")
    expect(page.locator(".markdown").nth(1)).to_have_text("MIDDLE")
    expect(page.locator(".markdown").last).to_have_text("RIGHT")

    split[0] = Markdown("CHANGED LEFT")
    expect(page.locator(".markdown").first).to_have_text("CHANGED LEFT")
    expect(page.locator(".markdown").nth(1)).to_have_text("MIDDLE")
    expect(page.locator(".markdown").last).to_have_text("RIGHT")

def test_multi_split_append_panel(page):
    split = MultiSplit(Markdown("LEFT"), Markdown("MIDDLE"), Markdown("RIGHT"))
    serve_component(page, split)

    expect(page.locator(".markdown").first).to_have_text("LEFT")
    expect(page.locator(".markdown").nth(1)).to_have_text("MIDDLE")
    expect(page.locator(".markdown").last).to_have_text("RIGHT")

    split.append(Markdown("NEW"))
    expect(page.locator(".markdown").first).to_have_text("LEFT")
    expect(page.locator(".markdown").nth(1)).to_have_text("MIDDLE")
    expect(page.locator(".markdown").nth(2)).to_have_text("RIGHT")
    expect(page.locator(".markdown").last).to_have_text("NEW")
