# import pyfiglet
# T = input("Enter Text you want to convert to ASCII art : ")
# ASCII_art_1 = pyfiglet.figlet_format(T)
# print(ASCII_art_1)

# import pyfiglet
# T = input("Enter Text you want to convert to ASCII art : ")
# ASCII_art_1 = pyfiglet.figlet_format(T,font='isometric1')
# print(ASCII_art_1)

from asciify import ASCIIArtConverter

converter = ASCIIArtConverter()
ascii_art = converter.convert("ascii-art-test.jpg", width=80)
ascii_art1 = converter.convert("test-1.jpg", width=80)
print(ascii_art)
print(ascii_art1)