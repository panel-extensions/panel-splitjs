import Split from "https://esm.sh/split.js@1.6.5"

export function render({ model, el }) {
  const split_div = document.createElement("div")
  split_div.className = `split multi-split ${model.orientation}`
  split_div.classList.add("loading")

  const objects = model.objects ? model.get_child("objects") : []
  const split_items = []
  for (let i = 0; i < objects.length; i++) {
    const split_item = document.createElement("div")
    split_item.className = "split-panel"
    split_div.append(split_item)
    split_items.push(split_item)
    split_item.append(objects[i])
  }

  el.append(split_div)

  let sizes = model.sizes
  const split = Split(split_items, {
    sizes: sizes,
    minSize: model.min_size || 0,
    maxSize: model.max_size || Number("Infinity"),
    dragInterval: model.step_size || 1,
    snapOffset: model.snap_size || 30,
    gutterSize: 8,
    direction: model.orientation,
    onDragEnd: (new_sizes) => {
      sizes = new_sizes
      this.model.sizes = sizes
    }
  })

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
