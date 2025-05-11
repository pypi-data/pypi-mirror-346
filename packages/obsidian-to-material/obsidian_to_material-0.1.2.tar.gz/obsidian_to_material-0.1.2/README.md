# Obsidian to Material

## 🇪🇸 Español

**Obsidian to Material** es una extensión para MkDocs que transforma automáticamente los bloques tipo _admonition_ utilizados en [Obsidian.md](https://obsidian.md) (específicamente los del plugin [Admonition](https://github.com/valentine195/obsidian-admonition) de Jeremy Valentine) en bloques compatibles con el tema [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).

Esto permite reutilizar notas personales escritas en Obsidian directamente en sitios estáticos generados con MkDocs, sin necesidad de scripts intermedios ni cambios manuales.

### 🧩 ¿Por qué?

Obsidian permite escribir bloques como:

````
```ad-warning
title: ¡Cuidado!
Este es un mensaje importante.
```
````

Pero MkDocs Material requiere el formato:

```
!!! warning "¡Cuidado!"
Este es un mensaje importante.
```

Esta extensión convierte automáticamente los bloques `ad-*` en su equivalente `!!!` durante el proceso de construcción del sitio.

### 🚀 Instalación

```bash
pip install obsidian-to-material
```

Y en `mkdocs.yml`:

```yaml
markdown_extensions:
  - admonition
  - obsidian_admonitions
  - pymdownx.superfences
```

### 🙌 Créditos

Este proyecto está inspirado en el excelente trabajo de [Jeremy Valentine](https://github.com/valentine195), autor del plugin [Admonition](https://github.com/valentine195/obsidian-admonition) para Obsidian.md.

---

## 🇬🇧 English

**Obsidian to Material** is a MkDocs extension that automatically transforms _admonition_-style blocks used in [Obsidian.md](https://obsidian.md) (specifically via the plugin [Admonition](https://github.com/valentine195/obsidian-admonition) by Jeremy Valentine) into blocks compatible with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).

This allows you to reuse notes written in Obsidian directly inside MkDocs documentation, with no manual conversion or intermediate scripts.

### 🧩 Why?

With Obsidian and its Admonition plugin, you can write:

````
```ad-warning
title: Warning!
This is an important message.
```
````

But MkDocs Material expects:

```
!!! warning "Warning!"
This is an important message.
```

This extension converts `ad-*` blocks to proper `!!!` admonitions during the Markdown processing phase.

### 🚀 Installation

```bash
pip install obsidian-to-material
```

In your `mkdocs.yml`:

```yaml
markdown_extensions:
  - admonition
  - obsidian_admonitions
  - pymdownx.superfences
```

### 🙌 Credits

This project is inspired by the great work of [Jeremy Valentine](https://github.com/valentine195), author of the [Admonition](https://github.com/valentine195/obsidian-admonition) plugin for Obsidian.md.

---

## 📄 License

Distributed under the [MIT License](LICENSE).
