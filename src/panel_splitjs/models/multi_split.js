import Split from "https://esm.sh/split.js@1.6.5"

export function render({ model, el }) {
  const split_div = document.createElement("div")
  split_div.className = `split multi-split ${model.orientation}`
  split_div.classList.add("loading")

  let split = null

  function reconcileChildren(parent, desiredChildren) {
    // Ensure each desired child is at the correct index
    for (let i = 0; i < desiredChildren.length; i++) {
      const child = desiredChildren[i]
      const current = parent.children[i]
      if (current?.id === child.id) continue
      if (current) {
        parent.insertBefore(child, current)
      } else {
        parent.append(child)
      }
    }

    // Remove any extra children that are no longer desired
    while (parent.children.length > desiredChildren.length) {
      parent.removeChild(parent.lastElementChild)
    }
  }

  const render_splits = () => {
    if (split != null) {
      split.destroy()
      split = null
    }

    const objects = model.objects ? model.get_child("objects") : []
    const split_items = []

    for (let i = 0; i < objects.length; i++) {
      const obj = objects[i]
      const id = `split-panel-${model.objects[i].id}`

      // Try to reuse an existing split_item
      let split_item = el.querySelector(`#${id}`)
      if (split_item == null) {
        split_item = document.createElement("div")
        split_item.className = "split-panel"
        split_item.id = id
        split_item.replaceChildren(obj)
      }

      split_items.push(split_item)
    }

    // Incrementally reorder / trim children of split_div
    reconcileChildren(split_div, split_items)

    let sizes = model.sizes
    split = Split(split_items, {
      sizes,
      minSize: model.min_size || 0,
      maxSize: model.max_size || Number("Infinity"),
      dragInterval: model.step_size || 1,
      snapOffset: model.snap_size || 30,
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
      onDragEnd: (new_sizes) => {
        sizes = new_sizes
        this.model.sizes = sizes
      }
    })
  }

  render_splits()
  el.append(split_div)

  model.on("objects", render_splits)
  model.on("sizes", () => {
    if (sizes === model.sizes) {
      return
    }
    sizes = model.sizes
    split.setSizes(sizes)
  })

  let initialized = false
  model.on("after_layout", () => {
    if (!initialized) {
      initialized = true
      split_div.classList.remove("loading")
    }
  })

  model.on("remove", () => split.destroy())
}
