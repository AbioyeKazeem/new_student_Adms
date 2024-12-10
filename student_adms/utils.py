from datetime import datetime

def generate_matriculation_number(programme, last_serial_number):
    """
    Generates a matriculation number in the format:
    {Programme Shortform}/{Year}/{Serial Number}
    Example: DPT/2024/017
    """
    year = datetime.now().year
    shortform = programme[:3].upper()
    return f"{shortform}/{year}/{last_serial_number:03d}"

