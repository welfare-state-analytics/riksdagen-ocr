for filename in images/personregister-*.jpg
    set plain_filename (string replace .jpg "" $filename)
    set plain_filename (string replace images/ "" $plain_filename)
    echo $filename
    echo $plain_filename
    tesseract -l swe $filename altofiles/$plain_filename alto
end