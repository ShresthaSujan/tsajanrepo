#Remove the paragraph tag present in the text
sed 's/<p>//g' 31_51260.txt > temp1.txt

#Remove the closing paragraph tag 
sed 's/<\/\p>//g' temp1.txt

#Remove all line beginning with a hash symbol
cat temp1.txt | grep -Ev '#' temp1.txt > temp2.txt

#Remove the first line beginning with a 0
cat temp2.txt |grep -Ev '0' temp2.txt > temp3.txt

#Remove any line with empty string
grep -e '^$' -v temp3.txt > temp4.txt

#Enter a new line after the end of sentence
sed 's/। /।\n/g' temp4.txt > temp5.txt 

#Enter a new line after a question mark obtained
sed 's/? /?\n/g' temp5.txt > temp6.txt

#Replace all the commas that are in the text by a dot symbol
sed 's/, /./g' temp6.txt > temp7.txt

#Add a comma after the end of the sentence
sed 's/।/।,/g' temp7.txt > final.txt

mv final.txt final.csv
# renaming .txt file to .csv and separated them on the basis of comma inserted at the end of the line.

# After the .csv file conversion, 1 was added to next column for facts and 0 for opinions manually
#please look for the insertedOpionsAndFactsToFinal.csv file

#Remove all the intermediatory files created
rm temp*.txt

