# Reveal.js Presentation Generator

## Description
Use this skill when the user wants to programmatically generate presentations, slide decks, or PPT-like documents with complex animations (fade, fly-in, zoom, morph). Because native `.pptx` XML generation is highly unstable across Office versions and prone to animation downgrades, this skill uses **Reveal.js (HTML/CSS)** as a modern, reliable, and highly extensible alternative for AI-generated presentations.

## Instructions
1. When generating a presentation, output a single standalone HTML file.
2. Embed the Reveal.js CDN links for CSS and JS.
3. Use `<section>` tags for slides.
4. Use `<div class="fragment [animation-class]">` for component-level animations (e.g., `fade-up`, `fade-down`, `zoom-in`, `fade-in-then-out`).
5. For custom complex animations (like "fly-in from far away with bounce"), embed custom CSS in the `<style>` block and apply the class name to the fragment.
6. Initialize Reveal at the bottom of the body.
7. Save the file to the workspace (e.g., `presentation.html`) and send it to the user.

## Boilerplate Template

```html
<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>AI Generated Presentation</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.3.1/reset.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.3.1/reveal.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.3.1/theme/dracula.min.css">
    
    <style>
        /* Custom Animations */
        .reveal .slides section .fragment.custom-fly-in {
            opacity: 0;
            transform: translateY(300px) scale(0.2);
            transition: all 1.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        .reveal .slides section .fragment.custom-fly-in.visible {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    </style>
</head>
<body>
    <div class="reveal">
        <div class="slides">
            <section data-transition="zoom">
                <h1>Slide 1 Title</h1>
                <p>Subtitle or description</p>
            </section>

            <section>
                <h2>Slide 2 Title</h2>
                <h1 class="fragment custom-fly-in">Custom Fly-In Animation!</h1>
                <p class="fragment fade-up">Standard fade-up animation.</p>
            </section>
        </div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.3.1/reveal.min.js"></script>
    <script>
        Reveal.initialize({
            controls: true,
            progress: true,
            center: true,
            hash: true,
            transition: 'slide'
        });
    </script>
</body>
</html>
```

## Note for AI
If the user explicitly insists on `.pptx` files, warn them about animation instability, and fall back to the "Template Replacement" method (modifying text in an existing manually-animated PPTX file) using `python-pptx`, rather than generating animation XML from scratch.