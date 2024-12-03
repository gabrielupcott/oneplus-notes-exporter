import os
import re
import html
from lxml import etree

def sanitize_filename(filename, max_length=100):
    """
    Sanitize the filename by removing or replacing invalid characters,
    replacing spaces with underscores, and truncating to a maximum length.
    
    Parameters:
    - filename: Original filename string.
    - max_length: Maximum allowed length for the filename.
    
    Returns:
    - A sanitized and truncated filename string.
    """
    # Remove any characters that are not alphanumeric, underscores, or hyphens
    sanitized = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '', filename)
    # Replace spaces with underscores
    sanitized = sanitized.replace(' ', '_')
    # Truncate to max_length
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length].rstrip('_')  # Remove trailing underscore if any
    # Remove trailing dots or spaces
    sanitized = sanitized.rstrip('. ')
    return sanitized

def is_valid_xml_char(codepoint):
    """
    Check if a Unicode codepoint is a valid XML 1.0 character.
    
    Parameters:
    - codepoint: Integer representing the Unicode codepoint.
    
    Returns:
    - True if valid, False otherwise.
    """
    return (
        codepoint == 0x9 or
        codepoint == 0xA or
        codepoint == 0xD or
        (0x20 <= codepoint <= 0xD7FF) or
        (0xE000 <= codepoint <= 0xFFFD) or
        (0x10000 <= codepoint <= 0x10FFFF)
    )

def remove_invalid_xml_chars(xml_string):
    """
    Remove invalid XML character references from the XML string.
    
    Parameters:
    - xml_string: The original XML content as a string.
    
    Returns:
    - A cleaned XML string with invalid character references removed.
    """
    # Regex to find all numeric character references (e.g., &#3;)
    char_ref_re = re.compile(r'&#(\d+);')
    
    def replace_invalid(match):
        num = int(match.group(1))
        if not is_valid_xml_char(num):
            return ''  # Remove invalid character
        else:
            return match.group(0)  # Keep valid character reference
    
    # Remove invalid numeric character references
    cleaned_xml = char_ref_re.sub(replace_invalid, xml_string)
    
    return cleaned_xml

def escape_quotes(xml_string):
    """
    Escape unescaped quotes within attribute values.
    
    Parameters:
    - xml_string: The XML content as a string.
    
    Returns:
    - XML string with escaped quotes.
    """
    # This function assumes that attribute values are enclosed in double quotes.
    # It replaces unescaped double quotes within attribute values with &quot;
    
    # Regex to find attribute values
    attr_re = re.compile(r'(\w+)="([^"]*)"')
    
    def escape_inner_quotes(match):
        attr = match.group(1)
        value = match.group(2)
        # Replace unescaped double quotes with &quot;
        escaped_value = value.replace('"', '&quot;')
        return f'{attr}="{escaped_value}"'
    
    escaped_xml = attr_re.sub(escape_inner_quotes, xml_string)
    return escaped_xml

def parse_xml_to_txt_lxml(xml_file, output_dir):
    """
    Parse the XML file and create a text file for each <noteRecord>.
    
    Parameters:
    - xml_file: Path to the XML file.
    - output_dir: Directory where text files will be saved.
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Read the XML content from the file
        with open(xml_file, 'r', encoding='utf-8') as f:
            xml_content = f.read()
        
        # Step 1: Remove invalid character references
        cleaned_xml = remove_invalid_xml_chars(xml_content)
        
        # Step 2: Escape unescaped quotes within attribute values
        cleaned_xml = escape_quotes(cleaned_xml)
        
        # Parse the cleaned XML using lxml with recovery enabled
        parser = etree.XMLParser(recover=True)
        root = etree.fromstring(cleaned_xml.encode('utf-8'), parser=parser)
        
        # Check if parsing was successful
        if root is None:
            print("Failed to parse XML.")
            return
        
        # Iterate through each <noteRecord> element
        for note in root.findall('.//noteRecord'):
            _id = note.get('_id')  # Unique identifier for the note
            title = note.get('title', 'Untitled')  # Title of the note
            content = note.get('content', '')  # Content of the note
            
            # Ensure _id is present
            if not _id:
                print("Skipping a noteRecord without _id.")
                continue  # Skip records without _id
            
            # Decode HTML entities (e.g., &#10; to newline)
            content = html.unescape(content)
            
            # Include title in the file content (helpful when notes dont have titles and their first line becomes a title)
            file_content = f"{title}{content}"
            
            # Sanitize the title to create a valid filename
            sanitized_title = sanitize_filename(title)
            
            # Create the filename using sanitized title
            filename = f"{sanitized_title}.txt"
            
            # Full path for the text file
            file_path = os.path.join(output_dir, filename)
            
            # Ensure the filename does not already exist
            if os.path.exists(file_path):
                print(f"Warning: File {filename} already exists. Skipping to avoid overwriting.")
                continue  # Skip to avoid overwriting existing files
            
            # Write the content to the text file
            with open(file_path, 'w', encoding='utf-8') as f_out:
                f_out.write(file_content)
            
            print(f"Created: {file_path}")
    
    except etree.XMLSyntaxError as e:
        print(f"Error parsing XML with lxml: {e}")
    except OSError as os_err:
        print(f"OS error: {os_err}")
    except Exception as ex:
        print(f"An error occurred: {ex}")

if __name__ == "__main__":
    # Define the path to the XML backup file
    xml_file_path = 'OnePlusNote.xml'       # Path to your XML file
    # Define the output directory for the parsed text files
    output_directory = 'parsed_notes'       # Directory to save text files
    # Execute the parsing function
    parse_xml_to_txt_lxml(xml_file_path, output_directory)
