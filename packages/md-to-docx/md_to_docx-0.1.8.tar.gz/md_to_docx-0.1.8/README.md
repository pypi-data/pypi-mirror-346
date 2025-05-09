
一个MCP Server。
一个功能强大的Markdown转DOCX文档转换器，支持Mermaid图表渲染。
A MCP Server.
A powerful Markdown to DOCX document converter that supports rendering Mermaid charts as images.

## 特性/Features

- 将Markdown文件转换为Word DOCX格式/Convert Markdown files to Word DOCX format
- 自动渲染Mermaid图表为图像/Auto render Mermaid charts as images
   - 支持指定Mermaid主题['default','dark','forest','ocean','elegant']/Support specifying Mermaid themes ['default', 'dark', 'forest', 'ocean', 'elegant']
- 支持代码块格式化和语法高亮/Support code block formatting and syntax highlighting
- 支持表格、列表和其他Markdown元素/Support tables, lists, and other Markdown elements
   - 支持指定表格主题/Support specifying table themes  ['Normal Table', 'Table Grid', 'Light Shading', 'Light Shading Accent 1', 'Light Shading Accent 2', 'Light Shading Accent 3', 'Light Shading Accent 4', 'Light Shading Accent 5', 'Light Shading Accent 6', 'Light List', 'Light List Accent 1', 'Light List Accent 2', 'Light List Accent 3', 'Light List Accent 4', 'Light List Accent 5', 'Light List Accent 6', 'Light Grid', 'Light Grid Accent 1', 'Light Grid Accent 2', 'Light Grid Accent 3', 'Light Grid Accent 4', 'Light Grid Accent 5', 'Light Grid Accent 6', 'Medium Shading 1', 'Medium Shading 1 Accent 1', 'Medium Shading 1 Accent 2', 'Medium Shading 1 Accent 3', 'Medium Shading 1 Accent 4', 'Medium Shading 1 Accent 5', 'Medium Shading 1 Accent 6', 'Medium Shading 2', 'Medium Shading 2 Accent 1', 'Medium Shading 2 Accent 2', 'Medium Shading 2 Accent 3', 'Medium Shading 2 Accent 4', 'Medium Shading 2 Accent 5', 'Medium Shading 2 Accent 6', 'Medium List 1', 'Medium List 1 Accent 1', 'Medium List 1 Accent 2', 'Medium List 1 Accent 3', 'Medium List 1 Accent 4', 'Medium List 1 Accent 5', 'Medium List 1 Accent 6', 'Medium List 2', 'Medium List 2 Accent 1', 'Medium List 2 Accent 2', 'Medium List 2 Accent 3', 'Medium List 2 Accent 4', 'Medium List 2 Accent 5', 'Medium List 2 Accent 6', 'Medium Grid 1', 'Medium Grid 1 Accent 1', 'Medium Grid 1 Accent 2', 'Medium Grid 1 Accent 3', 'Medium Grid 1 Accent 4', 'Medium Grid 1 Accent 5', 'Medium Grid 1 Accent 6', 'Medium Grid 2', 'Medium Grid 2 Accent 1', 'Medium Grid 2 Accent 2', 'Medium Grid 2 Accent 3', 'Medium Grid 2 Accent 4', 'Medium Grid 2 Accent 5', 'Medium Grid 2 Accent 6', 'Medium Grid 3', 'Medium Grid 3 Accent 1', 'Medium Grid 3 Accent 2', 'Medium Grid 3 Accent 3', 'Medium Grid 3 Accent 4', 'Medium Grid 3 Accent 5', 'Medium Grid 3 Accent 6', 'Dark List', 'Dark List Accent 1', 'Dark List Accent 2', 'Dark List Accent 3', 'Dark List Accent 4', 'Dark List Accent 5', 'Dark List Accent 6', 'Colorful Shading', 'Colorful Shading Accent 1', 'Colorful Shading Accent 2', 'Colorful Shading Accent 3', 'Colorful Shading Accent 4', 'Colorful Shading Accent 5', 'Colorful Shading Accent 6', 'Colorful List', 'Colorful List Accent 1', 'Colorful List Accent 2', 'Colorful List Accent 3', 'Colorful List Accent 4', 'Colorful List Accent 5', 'Colorful List Accent 6', 'Colorful Grid', 'Colorful Grid Accent 1', 'Colorful Grid Accent 2', 'Colorful Grid Accent 3', 'Colorful Grid Accent 4', 'Colorful Grid Accent 5', 'Colorful Grid Accent 6']
   

## 使用方法/Usage
```json
  "mcpServers": {
    "md-to-docx": {
      "command": "uvx",
        "args": [
            "md-to-docx",
            "server"
        ]
    }
  }
```
```python
from md_to_docx import md_to_docx

md_to_docx("# Test\nHello World", "output.docx")
```

```shell
md-to-docx convert .\test.md -o output.docx
md-to-docx convert --help
md-to-docx server
```

