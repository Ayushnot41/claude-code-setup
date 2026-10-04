---
name: motion-animations
description: Use this skill when implementing modern web animations with the Motion library (from the motiondivision organization) in React or vanilla JavaScript.
---

# Motion Animation Skill

This skill provides guidelines and reference implementations for creating animations using the **Motion** library (formerly Framer Motion and Motion One, developed by the `motiondivision` organization).

## When to Use

Use this skill when:
1. Creating interactive web interfaces with animations (hover, tap, scroll, view transitions).
2. Implementing high-performance UI transitions in React (`motion/react`) or Vanilla JS (`motion`).
3. Enhancing user experience with spring physics, custom easing, and hardware-accelerated animations.

---

## 1. React Implementation (`motion/react`)

Always use `motion/react` for the official, modern React package of the library.

### Basic Usage

```jsx
import { motion } from "motion/react";

export function FadeInComponent() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, ease: "easeOut" }}
    >
      Content goes here
    </motion.div>
  );
}
```

### Gestures & Hover States

```jsx
import { motion } from "motion/react";

export function AnimatedButton() {
  return (
    <motion.button
      whileHover={{ scale: 1.05, backgroundColor: "#1d4ed8" }}
      whileTap={{ scale: 0.95 }}
      transition={{ type: "spring", stiffness: 400, damping: 15 }}
    >
      Click Me
    </motion.button>
  );
}
```

### Scroll Animations

```jsx
import { motion } from "motion/react";

export function FadeInOnScroll() {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      whileInView={{ opacity: 1, scale: 1 }}
      viewport={{ once: true, margin: "-100px" }}
      transition={{ duration: 0.6 }}
    >
      Animate on Enter Viewport
    </motion.div>
  );
}
```

---

## 2. Vanilla JavaScript Implementation (`motion`)

For vanilla JavaScript, HTML, and SVGs, use the core `motion` package which leverages the native Web Animations API (WAAPI) for maximum performance.

### Installation

```bash
npm install motion
```

### Basic Usage

```javascript
import { animate } from "motion";

// animate(target, keyframes, options)
animate(
  ".box",
  { 
    opacity: [0, 1], 
    x: 100, 
    rotate: 360 
  },
  { 
    duration: 0.8, 
    ease: "easeOut",
    repeat: Infinity 
  }
);
```

### Animation Controls

The `animate` function returns a controller object to manage the animation lifecycle:

```javascript
import { animate } from "motion";

const animation = animate(".box", { scale: 1.5 }, { duration: 1 });

// Controls
animation.pause();
animation.play();
animation.stop();
animation.finish();
animation.speed = 2; // Double speed
```

---

## Best Practices

1. **Keep it performant**: Prefer animating hardware-accelerated CSS properties (`transform` attributes like `x`, `y`, `scale`, `rotate`, and `opacity`) rather than layout-triggering properties (`width`, `height`, `margin`, `top`, `left`).
2. **Use Spring Physics**: For interactive elements like buttons and modals, use `type: "spring"` with `stiffness` and `damping` for a premium, natural feel.
3. **Optimized Imports**: Use `motion/mini` for lightweight pages to keep the bundle size small (only 2.3kb).
