echo $argv
set firstname $argv[1]
set plainname (string replace pdfs/ "" $firstname)
set plainname (string replace .pdf "" $plainname)
rm -rf images/$plainname
mkdir images/$plainname
pdfimages -j $argv[1] images/$plainname/$plainname
fish ocr.fish $plainname

rm -rf images/$plainname