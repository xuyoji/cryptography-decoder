#cryptography-decoder
this tool can be used to decode Vigenère automately and to help decode subsitution cryptography(with some human knowledge).

##start
python3 is required
'python .\Decoder.py -i inputfile -t type'
inputfile is the cryptography text file
type = 1 if decode subsititution
type = 2 if decode Vigenère

##decode subsititution
sub.txt is an attached testcase
we define meaningful n-gram: Meaningful n-gram is a gram of n letters(n >= 2) which appear more than twice in a text, and if it is a sub-string of a k-gram (k > n), its appearence time must be different from the k-gram.(Which means it appears more than the k-gram)
All gram we show to you is meaningful n-gram
You need to interate with the program with information and tips on screen.

##decode Vigenère
vig.txt is an attached testcase
All this procedure can be run automately.

##more help
Yan can view the attached pdf file for the example detail.