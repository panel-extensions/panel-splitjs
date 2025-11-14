import Split from "https://esm.sh/split.js@1.6.5"

const COLLAPSED_SIZE = 5

export function render({ model, el }) {
  const split_div = document.createElement("div")
  split_div.className = `split single-split ${model.orientation}`
  split_div.classList.add("loading")

  const split0 = document.createElement("div")
  split0.className = "split-panel"
  const split1 = document.createElement("div")
  split1.className = "split-panel"
  split_div.append(split0, split1)

  const left_content_wrapper = document.createElement("div")
  const right_content_wrapper = document.createElement("div")
  left_content_wrapper.className = model.collapsed === 0 ? "collapsed-content" : "content-wrapper"
  right_content_wrapper.className = model.collapsed === 1 ? "collapsed-content" : "content-wrapper"

  if (model.objects != null && model.objects.length == 2) {
    const [left, right] = model.get_child("objects")
    left_content_wrapper.append(left)
    right_content_wrapper.append(right)
  }
  split0.append(left_content_wrapper)
  split1.append(right_content_wrapper)

  model.on("objects", () => {
    const [left, right] = model.get_child("objects")
    left_content_wrapper.replaceChildren(left)
    right_content_wrapper.replaceChildren(right)
  })

  let left_arrow_button, right_arrow_button
  let left_click_count = 0
  let right_click_count = 0
  function reset_click_counts() {
    left_click_count = right_click_count = 0
  }
  if (model.show_buttons) {
    left_arrow_button = document.createElement("div")
    right_arrow_button = document.createElement("div")
    if (model.orientation === "horizontal") {
      left_arrow_button.className = "toggle-button-left"
      right_arrow_button.className = "toggle-button-right"
    } else {
      left_arrow_button.className = "toggle-button-up"
      right_arrow_button.className = "toggle-button-down"
    }
    split1.append(left_arrow_button, right_arrow_button)

    left_arrow_button.addEventListener("click", () => {
      left_click_count++
      right_click_count = 0

      let new_sizes
      if (left_click_count === 1 && model.sizes[1] < model.expanded_sizes[1]) {
        new_sizes = model.expanded_sizes
        is_collapsed = null
      } else {
        is_collapsed = 0
        new_sizes = [0, 100]
        left_click_count = 0
      }
      model.collapsed = is_collapsed
      sync_ui(new_sizes, true)
    })

    right_arrow_button.addEventListener("click", () => {
      right_click_count++
      left_click_count = 0

      let new_sizes
      if (right_click_count === 1 && model.sizes[0] < model.expanded_sizes[0]) {
        new_sizes = model.expanded_sizes
        is_collapsed = null
      } else {
        is_collapsed = 1
        new_sizes = [100, 0]
        right_click_count = 0
      }
      model.collapsed = is_collapsed
      sync_ui(new_sizes, true)
    })
  }

  el.append(split_div)

  let is_collapsed = model.collapsed
  let sizes = model.sizes
  const init_sizes = is_collapsed ? [100, 0] : model.sizes
  const split_instance = Split([split0, split1], {
    sizes: init_sizes,
    minSize: model.min_size,
    maxSize: model.max_size || Number("Infinity"),
    dragInterval: model.step_size,
    snapOffset: model.snap_size,
    gutterSize: 8,
    gutter: (index, direction) => {
      const gutter = document.createElement('div')
      gutter.className = `gutter gutter-${direction}`
      const divider = document.createElement('div')
      divider.className = "divider"
      gutter.append(divider)
      return gutter
    },
    direction: model.orientation,
    onDrag: (sizes) => {
      const new_collapsed_state = sizes[0] <= COLLAPSED_SIZE ? 0 : (sizes[1] <= COLLAPSED_SIZE ? 1 : null)
      if (is_collapsed !== new_collapsed_state) {
        is_collapsed = new_collapsed_state
        sync_ui(sizes)
      }
    },
    onDragEnd: (sizes) => {
      const new_collapsed_state = sizes[0] <= COLLAPSED_SIZE ? 0 : (sizes[1] <= COLLAPSED_SIZE ? 1 : null)
      is_collapsed = new_collapsed_state
      model.collapsed = is_collapsed
      sync_ui(sizes, true)
      reset_click_counts()
    },
  })

  function sync_ui(sizes = null, resize = false) {
    const left_panel_hidden = sizes ? sizes[0] <= COLLAPSED_SIZE : false
    const right_panel_hidden = sizes ? sizes[1] <= COLLAPSED_SIZE : false

    let [ls, rs] = sizes
    if (right_panel_hidden) {
      right_content_wrapper.className = "collapsed-content";
      [ls, rs] = [100, 0]
    } else {
      right_content_wrapper.className = "content-wrapper"
    }

    if (left_panel_hidden) {
      left_content_wrapper.className = "collapsed-content";
      [ls, rs] = [0, 100]
    } else {
      left_content_wrapper.className = "content-wrapper"
    }
    if (resize) {
      split_instance.setSizes([ls, rs])
      sizes = [ls, rs]
      model.sizes = [ls, rs]
      window.dispatchEvent(new Event('resize'))
    }
  }

  model.on("sizes", () => {
    if (sizes === model.sizes) {
      return
    }
    sizes = model.sizes
    sync_ui(sizes, true)
  })

  model.on("collapsed", () => {
    if (is_collapsed === model.collapsed) {
      return
    }
    is_collapsed = model.collapsed
    const new_sizes = is_collapsed === 0 ? [0, 100] : (is_collapsed === 1 ? [100, 0] : model.expanded_sizes)
    sync_ui(new_sizes, true)
  })

  let initialized = false
  model.on("after_layout", () => {
    if (initialized) {
      return
    }
    initialized = true
    if (model.show_buttons) {
      // Add animation on first load only
      left_arrow_button.classList.add("animated")
      right_arrow_button.classList.add("animated")

      // Remove animation after it completes
      setTimeout(() => {
        left_arrow_button.classList.remove("animated")
        right_arrow_button.classList.remove("animated")
      }, 1500)
    }
    window.dispatchEvent(new Event('resize'))
    split_div.classList.remove("loading")
  })

  model.on("remove", () => split_instance.destroy())
}
