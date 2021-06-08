set plainname $argv[1]
for filename in images/$plainname/*.jpg
    set plain_filename (string replace .jpg "" $filename)
    set plain_filename (string replace images/$plainname/ "" $plain_filename)
    echo $filename
    echo $plain_filename
    tesseract -l swe $filename altofiles/$plain_filename alto
end