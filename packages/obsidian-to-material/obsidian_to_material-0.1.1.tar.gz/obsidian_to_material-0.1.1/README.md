# Obsidian to Material

**Obsidian to Material** es una extensión para MkDocs que transforma automáticamente los bloques tipo *admonition* utilizados en [Obsidian.md](https://obsidian.md) (específicamente los del plugin [Admonition](https://github.com/valentine195/obsidian-admonition) de Jeremy Valentine) en bloques compatibles con el tema [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).

Esto permite reutilizar notas personales escritas en Obsidian directamente en sitios estáticos generados con MkDocs, sin necesidad de scripts intermedios ni cambios manuales.

---

## 🧩 ¿Por qué?

Obsidian, usando el plugin Admonition, permite escribir bloques como este:

```
```ad-warning
title: ¡Cuidado!
Este es un mensaje importante.
```
```

Pero MkDocs Material requiere el formato:

```
!!! warning "¡Cuidado!"
    Este es un mensaje importante.
```

Esta extensión convierte automáticamente los bloques `ad-*` en su equivalente `!!!` durante el proceso de construcción del sitio, facilitando el copiado directo de contenidos desde Obsidian.

---

## 🚀 Instalación

Instálalo con `pip`:

```bash
pip install obsidian-to-material
```

Luego, en tu archivo `mkdocs.yml`, añade:

```yaml
markdown_extensions:
  - admonition
  - obsidian_admonitions
  - pymdownx.superfences
```

No necesitas configurar `custom_fences` ni ningún paso adicional.

---

## 🙌 Créditos

Este proyecto está inspirado en el excelente trabajo de [Jeremy Valentine](https://github.com/valentine195), autor del plugin [Admonition](https://github.com/valentine195/obsidian-admonition) para Obsidian.md.

---

## 📄 Licencia

Distribuido bajo licencia [MIT](LICENSE).