import Split from "https://esm.sh/split.js@1.6.5"

export function render({ model, el, view }) {
  const split_div = document.createElement("div")
  split_div.className = `split multi-split ${model.orientation}`
  split_div.style.visibility = "hidden"
  split_div.classList.add("loading")

  let split = null
  let initialized = false
  let sizes = model.sizes

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

    const object_models = model.objects || []
    const objects = model.objects ? model.get_child("objects") : []
    const desired_ids = object_models.map((obj_model) => `split-panel-${obj_model.id}`)
    const desired_id_set = new Set(desired_ids)
    const current_children = Array.from(split_div.children)
    const current_ids = current_children.map((child) => child.id)
    const current_filtered = current_ids.filter((id) => desired_id_set.has(id))
    const removals_only =
      current_filtered.length === desired_ids.length &&
      desired_ids.every((id, idx) => id === current_filtered[idx])

    const rerender_views = []
    let split_items = []

    if (removals_only) {
      for (const child of current_children) {
        if (!desired_id_set.has(child.id)) {
          child.remove()
        }
      }
      split_items = desired_ids
        .map((id) => split_div.querySelector(`#${id}`))
        .filter((child) => child != null)
    } else {
      for (let i = 0; i < objects.length; i++) {
        const obj_model = object_models[i]
        const id = `split-panel-${obj_model.id}`
        const current_child = current_children[i]
        let split_item = split_div.querySelector(`#${id}`)

        if (current_child?.id === id) {
          split_items.push(current_child)
          continue
        }

        const obj = objects[i]
        const child_view = view.get_child_view(obj_model)
        if (split_item && (child_view?.rerender_ || child_view?.rerender)) {
          rerender_views.push(child_view)
        }

        // Try to reuse an existing split_item
        if (split_item == null) {
          split_item = document.createElement("div")
          split_item.className = "split-panel"
          split_item.id = id
          split_item.replaceChildren(obj)
        } else if (split_item.firstChild !== obj) {
          split_item.replaceChildren(obj)
        }

        split_items.push(split_item)
      }

      // Incrementally reorder / trim children of split_div
      reconcileChildren(split_div, split_items)
    }

    sizes = model.sizes
    split = Split(split_items, {
      sizes,
      minSize: model.min_size || 0,
      maxSize: model.max_size || Number("Infinity"),
      dragInterval: model.step_size || 1,
      snapOffset: model.snap_size || 30,
      gutterSize: model.gutter_size,
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
    if (initialized) {
      for (const child_view of rerender_views) {
        if (child_view?.rerender_) {
          child_view.rerender_()
        } else if (child_view?.rerender) {
          child_view.rerender()
        }
      }
    }
  }

  render_splits()
  el.append(split_div)

  model.on("objects", render_splits)
  model.on("sizes", () => {
    if (sizes === model.sizes) {
      return
    }
    sizes = model.sizes
    if (initialized && split) {
      split.setSizes(sizes)
    }
  })

  model.on("after_layout", () => {
    if (!initialized) {
      initialized = true
      split_div.style.visibility = ""
      split_div.classList.remove("loading")
      if (split && model.sizes) {
        split.setSizes(model.sizes)
      }
    }
  })

  model.on("remove", () => split.destroy())
}
