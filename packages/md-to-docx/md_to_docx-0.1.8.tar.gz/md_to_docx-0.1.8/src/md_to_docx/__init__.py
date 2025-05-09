"""
Markdown to DOCX converter with Mermaid diagram support

This module provides tools to convert Markdown files to DOCX format,
including rendering Mermaid diagrams as images.

Optional dependencies:
- pymermaid: pip install pymermaid  # 用于纯Python渲染Mermaid图表
- mermaid-py: pip install mermaid-py==0.7.0  # 功能丰富的Mermaid渲染工具

Basic usage:
  from md_to_docx import md_to_docx
  
  # Convert markdown to docx
  md_to_docx(markdown_content, output_file="output.docx")
"""

__version__ = "0.1.1"

import click
import sys
import asyncio
import logging
import os
from pathlib import Path
from typing import Any
from mcp.server import Server
import mcp.types as types
import re
import textwrap

# Handle imports for both package usage and direct script execution
try:
    # When used as a package
    from .core import md_to_docx, render_mermaid_to_image
except ImportError:
    # When run directly
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
    from src.md_to_docx.core import md_to_docx, render_mermaid_to_image

from mcp.server.fastmcp import FastMCP

__all__ = ["md_to_docx", "render_mermaid_to_image"]

# Initialize FastMCP server
mcp = FastMCP("md_to_docx")

# 添加 textwrap 导入，用于文本换行
import textwrap


def generate_placeholder_image(text: str) -> bytes:
    """生成一个包含错误信息的占位图像"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        import io
        
        # 创建一个带有文本的图像
        width, height = 400, 200
        image = Image.new("RGB", (width, height), (240, 240, 240))
        draw = ImageDraw.Draw(image)
        
        # 绘制边框
        draw.rectangle([0, 0, width-1, height-1], outline=(200, 200, 200))
        
        # 添加文本
        try:
            # 尝试使用系统字体
            font = ImageFont.truetype("arial.ttf", 14)
        except:
            # 如果没有可用字体，使用默认字体
            font = ImageFont.load_default()
            
        draw.text((20, 20), "图片资源错误", fill=(255, 0, 0), font=font)
        
        # 将长文本分行显示
        wrapped_text = '\n'.join(textwrap.wrap(text, width=40))
        y_position = 50
        for line in wrapped_text.split('\n'):
            draw.text((20, y_position), line, fill=(0, 0, 0), font=font)
            y_position += 20
            
        # 返回图像的二进制数据
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        return buffer.getvalue()
    except Exception:
        # 如果无法创建图像，返回一个极简的1x1像素
        return b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDAT\x08\xd7c\xf8\xff\xff?\x00\x05\xfe\x02\xfe\xdc\xccY\xe7\x00\x00\x00\x00IEND\xaeB`\x82'



@mcp.tool()
async def md_to_docx_tool(
    md_content: str, 
    output_file: str = None, 
    debug_mode: bool = False, 
    table_style: str = 'Table Grid',
    mermaid_theme: str = 'default',
    template_file: str = None
) -> str:
    """将Markdown文件转换为DOCX，并将Mermaid图表渲染为图片。
    
    Args:
        md_content: 要转换的Markdown内容
        output_file: 可选的输出文件路径，默认为'output.docx'
        debug_mode: 是否启用调试模式
        table_style: 表格样式，默认为'Table Grid'，可选值见下方列表
        mermaid_theme: Mermaid图表主题，默认为'default'，可选值：['default', 'dark', 'forest', 'ocean', 'elegant']
        template_file: 可选的模板文件路径，用于作为基础文档样式
        
    Returns:
        保存的DOCX文件路径
        
    Table Styles:
        ['Normal Table', 'Table Grid', 'Light Shading', 'Light Shading Accent 1', 
         'Light Shading Accent 2', 'Light Shading Accent 3', 'Light Shading Accent 4', 
         'Light Shading Accent 5', 'Light Shading Accent 6', 'Light List', 
         'Light List Accent 1', 'Light List Accent 2', 'Light List Accent 3', 
         'Light List Accent 4', 'Light List Accent 5', 'Light List Accent 6', 
         'Light Grid', 'Light Grid Accent 1', 'Light Grid Accent 2', 
         'Light Grid Accent 3', 'Light Grid Accent 4', 'Light Grid Accent 5', 
         'Light Grid Accent 6', 'Medium Shading 1', 'Medium Shading 1 Accent 1', 
         'Medium Shading 1 Accent 2', 'Medium Shading 1 Accent 3', 
         'Medium Shading 1 Accent 4', 'Medium Shading 1 Accent 5', 
         'Medium Shading 1 Accent 6', 'Medium Shading 2', 'Medium Shading 2 Accent 1', 
         'Medium Shading 2 Accent 2', 'Medium Shading 2 Accent 3', 
         'Medium Shading 2 Accent 4', 'Medium Shading 2 Accent 5', 
         'Medium Shading 2 Accent 6', 'Medium List 1', 'Medium List 1 Accent 1', 
         'Medium List 1 Accent 2', 'Medium List 1 Accent 3', 'Medium List 1 Accent 4', 
         'Medium List 1 Accent 5', 'Medium List 1 Accent 6', 'Medium List 2', 
         'Medium List 2 Accent 1', 'Medium List 2 Accent 2', 'Medium List 2 Accent 3', 
         'Medium List 2 Accent 4', 'Medium List 2 Accent 5', 'Medium List 2 Accent 6', 
         'Medium Grid 1', 'Medium Grid 1 Accent 1', 'Medium Grid 1 Accent 2', 
         'Medium Grid 1 Accent 3', 'Medium Grid 1 Accent 4', 'Medium Grid 1 Accent 5', 
         'Medium Grid 1 Accent 6', 'Medium Grid 2', 'Medium Grid 2 Accent 1', 
         'Medium Grid 2 Accent 2', 'Medium Grid 2 Accent 3', 'Medium Grid 2 Accent 4', 
         'Medium Grid 2 Accent 5', 'Medium Grid 2 Accent 6', 'Medium Grid 3', 
         'Medium Grid 3 Accent 1', 'Medium Grid 3 Accent 2', 'Medium Grid 3 Accent 3', 
         'Medium Grid 3 Accent 4', 'Medium Grid 3 Accent 5', 'Medium Grid 3 Accent 6', 
         'Dark List', 'Dark List Accent 1', 'Dark List Accent 2', 'Dark List Accent 3', 
         'Dark List Accent 4', 'Dark List Accent 5', 'Dark List Accent 6', 
         'Colorful Shading', 'Colorful Shading Accent 1', 'Colorful Shading Accent 2', 
         'Colorful Shading Accent 3', 'Colorful Shading Accent 4', 
         'Colorful Shading Accent 5', 'Colorful Shading Accent 6', 'Colorful List', 
         'Colorful List Accent 1', 'Colorful List Accent 2', 'Colorful List Accent 3', 
         'Colorful List Accent 4', 'Colorful List Accent 5', 'Colorful List Accent 6', 
         'Colorful Grid', 'Colorful Grid Accent 1', 'Colorful Grid Accent 2', 
         'Colorful Grid Accent 3', 'Colorful Grid Accent 4', 'Colorful Grid Accent 5', 
         'Colorful Grid Accent 6']
    """
    return md_to_docx(md_content, output_file, debug_mode, table_style, mermaid_theme, template_file)


def serve():
    """Run the MCP server."""
    mcp.run(transport='stdio')


@click.group()
def cli():
    """MD to DOCX converter with Mermaid diagram support."""
    pass


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('-o', '--output', type=str, help='Path to the output DOCX file (default: input_file_name.docx)')
@click.option('-d', '--debug', is_flag=True, help='Enable debug mode')
@click.option('-t', '--table-style', type=str, default='Table Grid', 
              help='Style to apply to tables (default: Table Grid). Common styles include: Table Normal, Table Grid, Light Shading, Light List, Light Grid, Medium Shading 1, Medium Shading 2, etc.')
@click.option('-m', '--mermaid-theme', type=click.Choice(['default', 'dark', 'forest', 'ocean', 'elegant']), 
              default='default', help='Theme for Mermaid diagrams (default: default)')
@click.option('--template', type=click.Path(exists=True), help='Path to a template DOCX file to use as base document')
def convert(input_file, output, debug, table_style, mermaid_theme, template):
    """Convert Markdown file to DOCX file with Mermaid diagram support."""
    # Process input file path
    input_path = Path(input_file)
    
    # Determine output file path
    if output:
        output_path = output
    else:
        # Replace .md extension with .docx, or add .docx if no extension
        if input_path.suffix.lower() == '.md':
            output_path = str(input_path.with_suffix('.docx'))
        else:
            output_path = f"{input_file}.docx"
    
    try:
        # Read input file
        with open(input_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        click.echo(f"Converting {input_file} to {output_path}...")
        click.echo(f"Using table style: {table_style}")
        click.echo(f"Using Mermaid theme: {mermaid_theme}")
        if template:
            click.echo(f"Using template file: {template}")
        
        # Convert to DOCX
        result = md_to_docx(md_content, output_path, debug, table_style, mermaid_theme, template)
        
        click.echo(f"Conversion completed successfully! Output file: {result}")
        return 0
    
    except Exception as e:
        click.echo(f"Error during conversion: {e}", err=True)
        import traceback
        traceback.print_exc()
        return 1


@cli.command()
@click.option("-v", "--verbose", count=True, help="Increase verbosity (can be used multiple times)")
def server(verbose):
    """Run as an MCP server."""
    logging_level = logging.WARN
    if verbose == 1:
        logging_level = logging.INFO
    elif verbose >= 2:
        logging_level = logging.DEBUG

    logging.basicConfig(level=logging_level, stream=sys.stderr)
    # Don't use asyncio.run() here as mcp.run() handles the event loop itself
    serve()


def main():
    """Entry point for the application."""
    return cli()


if __name__ == "__main__":
    sys.exit(main()) 