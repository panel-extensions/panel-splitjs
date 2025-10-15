import Split from "https://esm.sh/split.js@1.6.5"

const COLLAPSED_SIZE = 5

export function render({ model, view, el }) {
  const split_div = document.createElement("div")
  split_div.className = `split single-split ${model.orientation}`
  split_div.classList.add("loading")

  const split0 = document.createElement("div")
  const split1 = document.createElement("div")
  split_div.append(split0, split1)

  const content_wrapper = document.createElement("div")
  content_wrapper.classList.add("content-wrapper")
  if (model.collapsed) {
    content_wrapper.className = "collapsed-content"
  }

  const left_content_wrapper = document.createElement("div")
  left_content_wrapper.classList.add("left-content-wrapper")

  if (model.objects != null) {
    const [left, right] = model.get_child("objects")
    left_content_wrapper.append(left)
    content_wrapper.append(right)
  }
  split0.append(left_content_wrapper)
  split1.append(content_wrapper)

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
      } else {
        new_sizes = [0, 100]
        left_click_count = 0
      }

      is_collapsed = new_sizes[1] <= COLLAPSED_SIZE
      model.collapsed = is_collapsed

      sync_ui(new_sizes, true)
    })

    right_arrow_button.addEventListener("click", () => {
      right_click_count++
      left_click_count = 0

      let new_sizes
      if (right_click_count === 1 && model.sizes[0] < model.expanded_sizes[0]) {
        new_sizes = model.expanded_sizes
      } else {
        new_sizes = [100, 0]
        right_click_count = 0
      }

      is_collapsed = new_sizes[1] <= COLLAPSED_SIZE
      model.collapsed = is_collapsed

      sync_ui(new_sizes, true)
    })
  }

  el.append(split_div)

  let is_collapsed = model.collapsed
  const init_sizes = is_collapsed ? [100, 0] : model.sizes
  const split_instance = Split([split0, split1], {
    sizes: init_sizes,
    minSize: model.min_size,
    maxSize: model.max_size || Number("Infinity"),
    dragInterval: model.step_size,
    snapOffset: model.snap_size,
    gutterSize: 8,
    direction: model.orientation,
    onDrag: (sizes) => {
      const new_collapsed_state = Math.min(...sizes) <= COLLAPSED_SIZE
      if (is_collapsed !== new_collapsed_state) {
        is_collapsed = new_collapsed_state
        sync_ui(sizes)
      }
    },
    onDragEnd: (sizes) => {
      const new_collapsed_state = sizes[1] <= COLLAPSED_SIZE
      if (is_collapsed !== new_collapsed_state) {
        is_collapsed = new_collapsed_state
        model.collapsed = new_collapsed_state
      }
      sync_ui(sizes, true)
      reset_click_counts()
    },
  })

  function sync_ui(sizes = null, resize = false) {
    const left_panel_hidden = sizes ? sizes[0] <= COLLAPSED_SIZE : false
    const right_panel_hidden = sizes ? sizes[1] <= COLLAPSED_SIZE : false

    let [ls, rs] = sizes
    if (right_panel_hidden) {
      content_wrapper.className = "collapsed-content";
      [ls, rs] = [100, 0]
    } else {
      content_wrapper.className = "content-wrapper"
    }

    if (left_panel_hidden) {
      left_content_wrapper.className = "collapsed-content";
      [ls, rs] = [0, 100]
    } else {
      left_content_wrapper.className = "left-content-wrapper"
    }
    if (resize) {
      split_instance.setSizes([ls, rs])
      model.sizes = [ls, rs]
    }
  }

  model.on("collapsed", (event) => {
    if (is_collapsed === model.collapsed) {
      return
    }
    is_collapsed = model.collapsed
    const new_sizes = is_collapsed ? [100, 0] : model.sizes
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

      // Remove animation after it completes and set flag
      setTimeout(() => {
        left_arrow_button.classList.remove("animated")
        right_arrow_button.classList.remove("animated")
      }, 1500)
    }
    split_div.classList.remove("loading")
  })
}
