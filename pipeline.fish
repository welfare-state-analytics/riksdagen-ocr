echo $argv
rm images/*
pdfimages -j $argv[1] images/personregister
fish ocr.fish
rm images/*
