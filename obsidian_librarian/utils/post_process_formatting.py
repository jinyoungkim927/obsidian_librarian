import re

def remove_markdown_fences(content):
    """Remove markdown code fences if they exist at the start and end of the content"""
    return re.sub(r'^```markdown\n|```\n?$', '', content.strip())

def convert_latex_delimiters(content):
    """Convert LaTeX delimiters from \( \) to $ and \[ \] to $$, handling multi-line cases"""
    # Convert display math (multi-line)
    content = re.sub(r'\\\[\s*(.*?)\s*\\\]', r'$$\1$$', content, flags=re.DOTALL)
    # Convert inline math
    content = re.sub(r'\\\((.*?)\\\)', r'$\1$', content)
    return content

def adjust_heading_levels(content):
    """Convert all headers to bold text"""
    lines = content.split('\n')
    processed_lines = []
    
    for line in lines:
        if line.startswith('#'):
            # Convert any header level to bold
            line = '**' + line.lstrip('#').strip() + '**'
        processed_lines.append(line)
    
    return '\n'.join(processed_lines)

def format_latex(content):
    """Format LaTeX expressions by removing spaces and converting display math"""
    # Remove spaces between $ and content for inline math
    content = re.sub(r'\$ (.*?) \$', r'$\1$', content)
    
    # Convert display math blocks to double dollar signs and remove all preceding whitespace
    content = re.sub(r'\s*\\\[(.*?)\\\]', r'$$\1$$', content)
    content = re.sub(r'\s*\$\$(.*?)\$\$', r'$$\1$$', content)
    
    return content

def unindent_content(content):
    """Remove one level of indentation from all content while preserving hierarchy"""
    lines = content.split('\n')
    processed_lines = []
    
    for line in lines:
        # If line starts with spaces and a bullet point, remove 2 spaces but keep remaining indentation
        if re.match(r'\s+[-\*•]', line):
            if line.startswith('    '):  # Remove first level of indentation only
                line = line[2:]
        processed_lines.append(line)
    
    return '\n'.join(processed_lines)

def remove_extra_newlines(content):
    """Remove extra newlines, keeping appropriate spacing"""
    # First, handle multiple consecutive newlines
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    # Remove newline after double dollar signs unless followed by bullet point or bold
    content = re.sub(r'\$\$\n\n(?![-\*•\*\*])', r'$$\n', content)
    
    # Keep double newlines between sections, single newline between bullet points
    content = re.sub(r'(\*\*.*?\*\*)\n\n(?![\*\-])', r'\1\n', content)
    content = re.sub(r'(-.*)\n\n(-)', r'\1\n\2', content)
    
    return content

def format_bullet_points(content):
    """Format bullet points consistently"""
    lines = content.split('\n')
    processed_lines = []
    
    for line in lines:
        # Standardize bullet points to use single dash with space
        if re.match(r'\s*[-\*•]\s', line):
            line = re.sub(r'\s*[-\*•]\s+', '- ', line)
        processed_lines.append(line)
    
    return '\n'.join(processed_lines)

def post_process_ocr_output(content):
    """Apply all post-processing steps to OCR output"""
    content = remove_markdown_fences(content)
    content = convert_latex_delimiters(content)
    content = adjust_heading_levels(content)
    content = format_latex(content)
    content = format_bullet_points(content)
    content = unindent_content(content)
    content = remove_extra_newlines(content)
    return content
