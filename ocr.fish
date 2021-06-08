for filename in personregister-*.jpg
    set plain_filename (string replace .jpg "" $filename)
    echo $filename
    echo $plain_filename
    tesseract -l swe $filename altofiles/$plain_filename alto
end