# Tag Reference

This page lists all supported tags in the DSL language, what they do, what parameters they support, and what output they generate.

For each tag, the parameters listed below are the officially defined ones. If you pass any **additional parameters**, they will automatically be treated as **CSS properties** and applied to the resulting element. This means you can extend any tag with your own CSS styling, using key-value pairs (e.g., `margin="10px"`, `border="1px solid red"`).

---

## 1. `header`

**DSL Example:**

```dsl
header <title="My App", args=["Menu1", "Menu2"], color="#f0f0f0">
```

**Description:** Defines the top section of the page with optional logo and navigation.

**Supported Parameters:**

* `title` (string)
* `args` (list of strings)
* `color`, `text_color`, `logo_color`
* All color values should be in valid hex format (e.g., `#ffffff`)

**Expected Output:** A top section that shows a logo and menu items styled with the given colors.

---

## 2. `side_nav`

**DSL Example:**

```dsl
side_nav <title="Logo", args=["Dashboard", "Settings"]>
```

**Description:** Adds a vertical sidebar with a logo and menu links.

**Supported Parameters:**

* `title` (string)
* `args` (list of strings)
* `color`, `text_color`, `logo_color`
* All color values should be in valid hex format (e.g., `#ffffff`)

**Expected Output:** A sidebar with a logo and a list of clickable navigation links.

---

## 3. `footer`

**DSL Example:**

```dsl
footer <title="© 2025 MyApp">
```

**Description:** Adds a footer to the bottom of the page.

**Supported Parameters:**

* `title` (string)
* `args` (list of strings)
* `color`, `text_color`, `logo_color`
* All color values should be in valid hex format (e.g., `#ffffff`)

**Expected Output:** A footer section displaying the provided title text.

---

## 4. `body`

**DSL Example:**

```dsl
body {
  row {
    box {
      title <text="Welcome">
    }
  }
}
```

**Description:** Wraps the main layout content. Can only contain `row` tags.

**CSS Class:** `main-content`

---

## 5. `row`

**DSL Example:**

```dsl
row {
  box {
    title <text="Hi">
  }
}
```

**Description:** Represents a horizontal section inside the body. Can only contain `box` tags.

**Supported Attributes:**

* `style`, `color`, `size`

**Expected Output:** A horizontal layout segment dividing the page into boxes.

---

## 6. `box`

**DSL Example:**

```dsl
box {
  title <text="Header">,
  text <content="Description">
}
```

**Description:** Basic container for content. Can only contain leaf tags like `title`, `text`, `image`.

**Supported Attributes:**

* `color` (used as background)

**Expected Output:** A content block that groups leaf elements together.

---

## 7. `title`

**DSL Example:**

```dsl
title <text="Main Title", color="blue", size="20px">
```

**Description:** Displays a bold or emphasized title in a box.

**Supported Attributes:**

* `text` (required)
* `color`, `size`

---

## 8. `text`

**DSL Example:**

```dsl
text <content="Body paragraph here.", color="#222", size="14px">
```

**Description:** Displays a normal paragraph or descriptive line.

**Supported Attributes:**

* `content` (required)
* `color`, `size`

---

## 9. `image`

**DSL Example:**

```dsl
image <src="/path/to/img.png", color="#ccc">
```

**Description:** Inserts an image into the layout.

**Supported Attributes:**

* `src` (required)
* `color`, `size`

**Expected Output:** An image with optional styling and sizing.

---

## 10. `button`

**DSL Example:**

```dsl
button <text="Click Me", color="#333", size="16px">
```

**Description:** Displays an interactive button.

**Supported Attributes:**

* `text` (required)
* `color`, `size`

**Expected Output:** A styled clickable button with the given text.

---

## 11. `input`

**DSL Example:**

```dsl
input <placeholder="Enter name", color="#eee">
```

**Description:** Displays a single-line input field.

**Supported Attributes:**

* `placeholder`
* `color`

---

## 12. `select_box`

**DSL Example:**

```dsl
select_box <options=["A", "B", "C"]>
```

**Description:** A dropdown list with selectable options.

**Supported Attributes:**

* `options` (list of strings)
* `color`

**Expected Output:** A select menu with provided choices.
