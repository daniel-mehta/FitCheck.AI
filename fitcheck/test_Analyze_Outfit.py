"""
Test script for the analyze_outfit function. 
Loads an image filename from the 'Images' folder and prints the model's critique.
"""

from analyze_outfit import analyze_outfit

result = analyze_outfit("fit_look_01.jpg")
print(result.encode('utf-8', errors='replace').decode('utf-8'))
