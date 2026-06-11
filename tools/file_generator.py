import os
from datetime import datetime
from config import DOCUMENTS_DIR

class FileGenerator:
    """Handles generating and creating files (documents, code, etc.)"""
    
    def __init__(self):
        os.makedirs(DOCUMENTS_DIR, exist_ok=True)
    
    def generate_document(self, filename: str, content: str, format: str = "txt") -> dict:
        """
        Generate a text/document file
        
        Args:
            filename: Name of the file to create
            content: Content to write to the file
            format: File format (txt, md, html, etc.)
            
        Returns:
            dict with status and file path
        """
        try:
            # Ensure proper file extension
            if not filename.endswith(f".{format}"):
                filename = f"{filename}.{format}"
            
            filepath = os.path.join(DOCUMENTS_DIR, filename)
            
            # Add timestamp to filename if it already exists
            if os.path.exists(filepath):
                base, ext = os.path.splitext(filename)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{base}_{timestamp}{ext}"
                filepath = os.path.join(DOCUMENTS_DIR, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return {
                "status": "success",
                "message": f"Document created: {filename}",
                "filepath": filepath
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to create document: {str(e)}"
            }
    
    def generate_python_script(self, filename: str, code: str) -> dict:
        """Generate a Python script"""
        return self.generate_document(filename, code, format="py")
    
    def generate_email_template(self, filename: str, recipient: str, subject: str, body: str) -> dict:
        """Generate an email template"""
        content = f"""To: {recipient}
Subject: {subject}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{body}
"""
        return self.generate_document(filename, content, format="txt")
    
    def generate_markdown(self, filename: str, content: str) -> dict:
        """Generate a Markdown document"""
        return self.generate_document(filename, content, format="md")
    
    def generate_html(self, filename: str, content: str) -> dict:
        """Generate an HTML document"""
        html_template = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{filename}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
    </style>
</head>
<body>
{content}
</body>
</html>
"""
        return self.generate_document(filename, html_template, format="html")
    
    def generate_report(self, filename: str, title: str, sections: dict) -> dict:
        """Generate a structured report"""
        content = f"# {title}\n\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        for section_name, section_content in sections.items():
            content += f"## {section_name}\n{section_content}\n\n"
        
        return self.generate_markdown(filename, content)
    
    def generate_csv(self, filename: str, headers: list, rows: list) -> dict:
        """Generate a CSV file"""
        content = ",".join(headers) + "\n"
        for row in rows:
            content += ",".join(str(cell) for cell in row) + "\n"
        
        return self.generate_document(filename, content, format="csv")
