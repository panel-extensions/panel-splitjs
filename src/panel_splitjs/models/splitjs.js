import Split from "https://esm.sh/split.js@1.6.5"

export function render({ model, view }) {
  const splitDiv = document.createElement("div")
  splitDiv.className = `split ${model.orientation}`
  splitDiv.classList.add("loading")

  const split0 = document.createElement("div")
  const split1 = document.createElement("div")
  splitDiv.append(split0, split1)

  // Create content wrapper for right panel
  const contentWrapper = document.createElement("div")
  contentWrapper.classList.add("content-wrapper")

  let leftArrowButton, rightArrowButton
  if (model.show_buttons) {
    // Create toggle icons for both sides of the divider
    leftArrowButton = document.createElement("div")  // < button
    rightArrowButton = document.createElement("div") // > button

    // Set button icons based on orientation
    if (model.orientation === "horizontal") {
      leftArrowButton.className = "toggle-button-left"
      rightArrowButton.className = "toggle-button-right"
    } else {
      leftArrowButton.className = "toggle-button-up"
      rightArrowButton.className = "toggle-button-down"
    }

    // Add both buttons to the right panel (split1) so they're positioned relative to the divider
    split1.appendChild(leftArrowButton)
    split1.appendChild(rightArrowButton)

    // Left/Up arrow button event listener - two-step toggle
    leftArrowButton.addEventListener("click", () => {
      leftClickCount++
      rightClickCount = 0 // Reset other button's count

      let newSizes

      if (leftClickCount === 1) {
        // First tap: make sizes 50, 50
        newSizes = [50, 50]
      } else {
        // Second tap (or more): make sizes 0, 100
        newSizes = [0, 100]
        leftClickCount = 0 // Reset after second tap
      }

      splitInstance.setSizes(newSizes)

      // Update collapsed state based on new sizes
      const newCollapsedState = newSizes[1] <= 5
      model.send_msg({ collapsed: newCollapsedState })
      model.collapsed = newCollapsedState

      updateUIForCollapsedState(newSizes)
      view.invalidate_layout()
    })

    // Right/Down arrow button event listener - two-step toggle
    rightArrowButton.addEventListener("click", () => {
      rightClickCount++
      leftClickCount = 0 // Reset other button's count

      let newSizes

      if (rightClickCount === 1) {
        // First tap: make sizes 50, 50
        newSizes = [50, 50]
      } else {
        // Second tap (or more): make sizes 100, 0
        newSizes = [100, 0]
        rightClickCount = 0 // Reset after second tap
      }

      splitInstance.setSizes(newSizes)

      // Update collapsed state based on new sizes
      const newCollapsedState = newSizes[1] <= 5
      model.send_msg({ collapsed: newCollapsedState })
      model.collapsed = newCollapsedState

      updateUIForCollapsedState(newSizes)
      view.invalidate_layout()
    })
  }

  // Determine initial state - collapsed means right panel is hidden
  const initSizes = model.collapsed ? [100, 0] : model.expanded_sizes

  // Track click counts for toggle behavior
  let leftClickCount = 0  // For < button
  let rightClickCount = 0 // For > button

  // Function to reset click counts when sizes change via dragging
  function resetClickCounts() {
    leftClickCount = 0
    rightClickCount = 0
  }

  // Use minSize of 0 to allow full collapse via buttons
  const splitInstance = Split([split0, split1], {
    sizes: initSizes,
    minSize: [0, 0], // Allow full collapse for both panels
    gutterSize: 8, // Match the 8px width in CSS
    direction: model.orientation,
    onDrag: (sizes) => {
      const leftPanelHidden = sizes ? sizes[0] <= 5 : false
      const rightPanelHidden = sizes ? sizes[1] <= 5 : false
      if (Math.min(...sizes) < 5) {
        updateUIForCollapsedState(sizes)
        view.invalidate_layout()
      }
    },
    onDragEnd: (sizes) => {
      // Determine the new collapsed state based on panel sizes
      const rightPanelCollapsed = sizes[1] <= 5
      const leftPanelCollapsed = sizes[0] <= 5

      // The model's collapsed state represents whether the right panel is collapsed
      const newCollapsedState = rightPanelCollapsed

      if (model.collapsed !== newCollapsedState) {
        // Send message to Python about collapsed state change
        model.send_msg({ collapsed: newCollapsedState })
        model.collapsed = newCollapsedState
      }

      // Update UI based on current sizes
      updateUIForCollapsedState(sizes, true)

      view.invalidate_layout()

      // Reset click counts when user drags the splitter
      resetClickCounts()
    },
  })

  // Function to update UI elements based on collapsed state
  function updateUIForCollapsedState(sizes = null, resize = false) {
    // Determine current panel state
    const leftPanelHidden = sizes ? sizes[0] <= 5 : false
    const rightPanelHidden = sizes ? sizes[1] <= 5 : false

    // Update content visibility
    let [ls, rs] = sizes
    if (rightPanelHidden) {
      contentWrapper.className = "collapsed-content";
      [ls, rs] = [100, 0]
    } else {
      contentWrapper.className = "content-wrapper"
    }

    if (leftPanelHidden) {
      leftContentWrapper.className = "collapsed-content";
      [ls, rs] = [0, 100]
    } else {
      leftContentWrapper.className = "content-wrapper"
    }
    if (resize) {
      splitInstance.setSizes([ls, rs])
    }
  }

  // Listen for collapsed state changes from Python
  model.on("msg:custom", (event) => {
    if (event.type === "update_collapsed") {
      const newCollapsedState = event.collapsed

      model.collapsed = newCollapsedState

      // Update split sizes based on new collapsed state
      if (newCollapsedState) {
        // Collapse right panel (show only left)
        splitInstance.setSizes([100, 0])
      } else {
        // Expand to show both panels
        splitInstance.setSizes(model.expanded_sizes)
      }

      updateUIForCollapsedState()
      view.invalidate_layout()
    }
  })

  model.on("after_layout", () => {
    setTimeout(() => {
      splitDiv.classList.remove("loading")

      // Only add animation on initial load
      if (model.show_buttons && !window._toggleAnimationShown) {
        // Add animation on first load only
        leftArrowButton.classList.add("animated")
        rightArrowButton.classList.add("animated")

        // Remove animation after it completes and set flag
        setTimeout(() => {
          leftArrowButton.classList.remove("animated")
          rightArrowButton.classList.remove("animated")
          window._toggleAnimationShown = true
        }, 1500)
      }

      window.dispatchEvent(new Event("resize"))
    }, 100)
  })

  // Create a centered content wrapper for the left panel
  const leftContentWrapper = document.createElement("div")
  leftContentWrapper.classList.add("left-content-wrapper")

  // Set initial display based on collapsed state
  if (model.collapsed) {
    contentWrapper.className = "collapsed-content"
  }

  // Apply left-panel-content class to the left panel
  leftContentWrapper.classList.add("left-panel-content")

  // Append children to the appropriate containers
  if (model.objects != null) {
    const [left, right] = model.get_child("objects")
    leftContentWrapper.append(left)
    contentWrapper.append(right)
  }
  split0.append(leftContentWrapper)
  split1.append(contentWrapper)

  return splitDiv
}
