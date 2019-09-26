import argparse
class Decoder:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-i',help='input ciphertext file', dest='inputfile',required=True)
        parser.add_argument('-o', help='output plaintext file', default='outFile', dest='outfile')
        parser.add_argument('-t', type=int, help='cipher type\n1=substitution\n2=Vigenere',dest='type',required=True)
        args = parser.parse_args()
        self.ct = Decoder.read_text(args.inputfile)
        self.output = args.outfile
        self.type = args.type
        self.outtext = ''
        self.alpha_freq_dic = {'e':0.1249, 't':0.0928, 'a':0.0804, 'o':0.0764, 'i':0.0757, 'n':0.0723, 's':0.0651, 'r':0.0628, 'h':0.0505,
        'l':0.0407, 'd':0.0382, 'c':0.0334, 'u':0.0273, 'm':0.0251, 'f':0.024, 'p':0.0214, 'g':0.0187, 'w':0.0168,'y':0.0166, 'b':0.0148, 'v':0.0105,
        'k':0.0054, 'x':0.0023, 'j':0.0016, 'q':0.0012, 'z':0.001}

    def read_text(file):
        with open(file, 'r') as f:
            return ''.join([_.strip() for _ in f.readlines()])

    def output_text(file, text):
        with open(file, 'w') as f:
            f.write(text)

    def alpha_freq_count(text,step,shift):
        text = text.lower()
        dic = {chr(i):0 for i in range(97, 123)}
        total = 0
        for i in range(shift, len(text), step):
            _ = text[i]
            if _ in dic:
                dic[_] += 1
                total += 1
        return dic, total
    
    def gram_freq_count(text, l):
        dic = {}
        for i in range(len(text) - l):
            gram = text[i:i+l]
            if gram in dic:
                dic[gram] += 1
            else:
                dic[gram] = 1
        return sorted(dic.items(), key=lambda x:x[1])

    def find_word(self, text, freq_dic, word, th, sub_dic):
        l = len(word)
        word_total_freq = [self.alpha_freq_dic[_] for _ in word]
        gram_freq = Decoder.gram_freq_count(text, l)
        reverse_dic = {sub_dic[_]:_ for _ in sub_dic}
        def pos(s, k):
            return [i for i in range(len(s)) if s[i] == s[k]]
        def judge(s1, s2):#gram, word
            for i in range(len(s1)):
                tms = sub_dic[s1[i].upper()]
                if (tms.islower() and tms != s2[i]) or (tms.isupper() and s2[i] in reverse_dic):
                    return False
                if pos(s1, i) != pos(s2, i):
                    return False
            return True

        candidate = []
        for _ in gram_freq:
            if _[1] <= th:
               continue
            _  = _[0].lower()
            if judge(_, word):
                freq = [freq_dic[_[i]]/len(text) for i in range(l)]
                candidate.append((freq, _))
        #print(gram_freq)
        delta_freq = [(sum([(word_total_freq[i] - _[0][i])**2 for i in range(l) if sub_dic[_[1][i].upper()].isupper()]),_[1]) for _ in candidate]
        ans = sorted(delta_freq)
        #print(delta_freq)
        return ans

    def get_all_gram_freq(self):
        self.all_gram_freq = []
        for i in range(2, 15):
            i_gram_freq = Decoder.gram_freq_count(self.ct, i)
            self.all_gram_freq.append([_ for _ in i_gram_freq if _[1] > 1])
        for k,_ in enumerate(self.all_gram_freq):
            for j,__ in enumerate(_):
                for i in range(k+1, len(self.all_gram_freq)):
                    for ___ in self.all_gram_freq[i]:
                        if __[0] in ___[0] and __[1] == ___[1]:
                            self.all_gram_freq[k][j] = ()
    
    def output_all_gram_freq(self, sub_dic):
        for k,_ in enumerate(self.all_gram_freq):
            add_one = False
            s = ''
            for __ in _:
                if __ != ():
                    add_one = True
                    s = (''.join([sub_dic[c] for c in __[0]])+':'+str(__[1])+' ') + s
            if add_one: 
                print('--%dgram--:\n%s\n'%(k+2, s))
    
    def output_part_plain_text(self, text, sub_dic):
        s = ''
        for _ in text:
            s += sub_dic[_]
        print(s)

    def decode_substitution(self):
        sub_dic = {chr(i):chr(i) for i in range(65, 91)}
        dic, total = Decoder.alpha_freq_count(self.ct, 1, 0)
        real_freq = sorted(dic.items(), key=lambda x:x[1])
        self.get_all_gram_freq()

        sub_e = real_freq[-1][0].upper()+'e'
        sub_order = [sub_e,'Ga','Id','On','Ut','Zh', 'So','Fw', 'Nl', 'Db', 'Ly', 'Mm', 'Ei', 'Wg', 'Yr', 'Hf', 'Pu', 'Ks', 'Av', 'Qj', 'Xp', 'Jc']

        for k,v in enumerate(sub_order):        
            sub_dic[v[0]] = v[1]
            print('\n\n-----fixed substitution rule-----')
            for i in range(k+1):
                print(sub_order[i][0]+'-'+sub_order[i][1], end = '  ')
            print('\n')
            test_word = 'the'
            fix_word_list = self.find_word(self.ct, dic, test_word, 1, sub_dic)

            print('-------all meaningful gram-------')
            self.output_all_gram_freq(sub_dic)

            print('-------word possibilty test-------')
            print('->test word = \'%s\''%test_word)
            print([(''.join([sub_dic[s.upper()] for s in fix_word[1]]), fix_word[0]) for fix_word in fix_word_list])
            print()

            print('--------current text--------')
            self.output_part_plain_text(self.ct, sub_dic)


        # default_freq = 'zqjxkvbpygwfcmuldrhsinoate'

        # print(real_freq)
        # substution_dic = {}
        # for k,v in enumerate(real_freq): 
        #     substution_dic[v[1]] = default_freq[k]
        # self.outtext = ''
        # for _ in self.ct.lower():
        #     if _ in substution_dic:
        #         self.outtext += substution_dic[_]


    def decode_Vigenere(self):
        max_len = 10
        len_prob = [[] for i in range(max_len)]
        default_v = sum([_**2 for _ in self.alpha_freq_dic.values()])
        
        

        def shift_alpha(s, n):
            return ''.join(chr(97 + ((ord(_) - 97) + n) %26) for _ in s)

        for guess_len in range(1, max_len+1):
            for shift in range(guess_len):
                dic, total = Decoder.alpha_freq_count(self.ct, guess_len, shift)

                v = sum([_*(_-1)/(total*(total-1)) for _ in dic.values()])
                len_prob[guess_len - 1].append(v)

        len_prob_var = [sum([(__ - default_v)**2 for __ in _])/len(_) for _ in len_prob]
        print('-------------------\n--mutiply result--')
        [print(k+1, ':', _) for k,_ in enumerate(len_prob)]
        min_var = min(len_prob_var)
        key_len = len_prob_var.index(min_var) + 1
        print('----variance from standard result(about 0.065)--')
        [print(k+1, ':', _) for k,_ in enumerate(len_prob_var)]
        print('Recommend Vigenere length(min variance) =', key_len)

        key = ''
        min_guess_var_list = []
        for shift in range(key_len):
            dic, total = Decoder.alpha_freq_count(self.ct, key_len, shift)
             
            guess_var = [0 for i in range(26)]
            possible_key = ''
            for i in range(26):     
                guess_var[i] = sum([(dic[shift_alpha(chr(j+97),i)]/total - self.alpha_freq_dic[chr(j+97)])**2 for j in range(26)])
            idx = guess_var.index(min(guess_var))
            min_guess_var_list.append((idx, guess_var[idx]))
            key += chr(97+idx)
        print('-------------------\nCalculate Vigenere key')
        [print('shift =', _[0], '  alphabet =', key[i], '  min_variance =', _[1]) for i,_ in enumerate(min_guess_var_list)]
        print('Recommed Vigenere key =', key)

        text_slice = [shift_alpha(''.join([self.ct[j].lower() for j in range(i, len(self.ct), key_len)]), 97-ord(key[i])) for i in range(key_len)]
        s = ''.join(text_slice[i][t] for t in range(len(text_slice[0])) for i in range(6)  if t < len(text_slice[i]))
        print('-------------------\nFinal plain text :')
    
        print(s)

        

    def run_decoder(self):
        if self.type ==1:
            self.decode_substitution()
        elif self.type == 2:
            self.decode_Vigenere()

            #Decoder.output_text(self.output, self.outtext)
            


a = Decoder()
a.run_decoder()