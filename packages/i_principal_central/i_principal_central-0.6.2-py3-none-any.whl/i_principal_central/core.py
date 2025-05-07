













import os

from pathlib import Path





class i_class:


    def __init__(i_self):


        i_self.i = {}

        i_self.i["i am you"] = False

        i_self.i["i develope"] = False


    def i_am_you(i_self):


        i_self.i["i am you"] = True


    def i_develope(i_self):

        i_self.i["i develope"] = True



    def i_function(i_self, i_function):


        if ((i_self.i["i am you"] == True) and (i_self.i["i develope"] == True)):



            if (i_function == "make file-s of send-ing and receive-ing and i_math and i_money"):

                print("i_hello .")



                i_self.i["i_math"] = r"""


















global i


i = {}



i["principal-central"] = "i am here"


i["i am you"] = True

if (i["i am you"] == True):



    import os

    import time



    def read_i(file):

        # lit le entier depuit le fichier 'file'

        i = 0

        try:

            with open(file, "r") as f_:

                i = int(f_.read(os.path.getsize(file)))

        except:

            semaphore = True

        return i


    def my_max(a, b):

        # renvoi le max de 'a' et 'b'

        if (a <= b):

            return b

        else:

            return a

    def my_min(a, b):

        # renvoi le min de 'a' et 'b'

        if (a >= b):

            return b

        else:

            return a


    def my_abs(a):

        # calcule le abs de 'a'

        if (a < 0):

            return -a

        else:

            return a



    def my_puissance(a, n):

        # calcule la puissance 'a' de 'n'

        m = 1

        if (n > 0):

            i = 0

            while (i < n):

                m = m * a

                i += 1

        elif (n == 0):

            m = 1

        elif (n < 0):

            i = 0

            while (i < (-n)):

                m = m * (1 / a)

                i += 1

        return m



    def my_div(a, b, number_of_digit_after_the_floating_pointax):

        # calcule  'a' / 'b' avec 'number_of_digit_after_the_floating_pointax' nombre de numereau apres la vergule

        m = 0

        if (a < 0):

            a = -a

        if (b < 0):

            b = -b

        i = 0
        
        q = 1
        
        while (q < a):
            
            q = q * 10
            
            i += 1

        while (i > -1):

            while (m * b < a):

                # m = m - my_puissance(a=10, n=(i))

                m = m + q

                # print("i = ", i, " . m = ", m, " . a = ", a, " . m * b = ", m * b)

            if (m * b > a):

                m = m - q

                i -= 1
                
                q = my_puissance(a=10, n=i)
                            
            else:
                
                break


            # print("1 . i = ", i, " . m = ", m)

        # print("finished . 1")

        k = 0

        m1 = 0

        if ((number_of_digit_after_the_floating_pointax > 0) and (m * b != a)):

            d1 = my_puissance(a=10, n=number_of_digit_after_the_floating_pointax)

            m1 = m * d1

            i = number_of_digit_after_the_floating_pointax

            while (i > -1):

                d2 = my_puissance(a=10, n=i)

                while ((m1 + k) * b < a * d1):

                    k = k + d2

                if ((m1 + k) * b == a * d1):

                    break

                else:

                    k = k - d2

                i -= 1
                
        i = 0
        
        while (my_puissance(a=10, n=i) <= k):
            
            i += 1
            
        #if (i == 0):
            
        #    i = 1

        # print("finale . m = ", m, " .  (m * b == a) = ", (m * b == a), " . (m1 + k) * b == a * my_puissance(a=10, n=number_of_digit_after_the_floating_pointax) = ", (m1 + k) * b == a * my_puissance(a=10, n=number_of_digit_after_the_floating_pointax))


        return [m, k, number_of_digit_after_the_floating_pointax - i]

    def conv_chr_int(c):

        # convertie un caractere à un chiffre

        n = 0

        if (len(c) == 1):

            if (c == "0"):

                n = 0

            elif (c == "1"):

                n = 1

            elif (c == "2"):

                n = 2

            elif (c == "3"):

                n = 3

            elif (c == "4"):

                n = 4

            elif (c == "5"):

                n = 5

            elif (c == "6"):

                n = 6

            elif (c == "7"):

                n = 7

            elif (c == "8"):

                n = 8

            elif (c == "9"):

                n = 9

        return n

    def str_to_int(s):

        # convertie un string à un integer

        erreur = False

        num = 0

        i = -1

        r = True

        p = 0

        s_ = ""

        r_ = True

        t = 1

        while ((i < len(s)) and (r_)):

            i += 1

            if ((s[i] == "+") or (s[i] == "-")):

                if (s[i] == "-"):

                    t = -t

            else:

                r_ = False



        while ((i < len(s)) and (r)):

            if (not ((s[i] == "0") or (s[i] == "1") or (s[i] == "2") or (s[i] == "3") or (s[i] == "4") or (s[i] == "5") or 
                (s[i] == "6") or (s[i] == "7") or (s[i] == "8") or (s[i] == "9") or (s[i] == "."))):

                r = False

            if (s[i] == "."):

                p += 1

            if ((r) and (p == 0)):

                s_ += s[i]

            i += 1

        if ((i < len(s)) or (p > 1)):

            erreur = True


        if (not (erreur)):

            i = len(s_) - 1

            q = 1

            while (i >= 0):

                num += conv_chr_int(c=s_[i]) * q

                i -= 1

                q *= 10


            num = num * t
        

        return [erreur, num]


    def conv_int_chr(p):

        # convertie un integer à un chr

        c = ""

        if ((p < 10) and (p >= 0)):

            if (p == 0):

                c = "0"

            elif (p == 1):

                c = "1"

            elif (p == 2):

                c = "2"

            elif (p == 3):

                c = "3"

            elif (p == 4):

                c = "4"

            elif (p == 5):

                c = "5"

            elif (p == 6):

                c = "6"

            elif (p == 7):

                c = "7"

            elif (p == 8):

                c = "8"

            elif (p == 9):

                c = "9"

        return c
        


    def my_puissance_1(l, n, number_of_digit_after_the_floating_pointax):

        # calcule la puissance 'l' de 'n' avec 'number_of_digit_after_the_floating_pointax' nombre de numereau apres la vergule

        # 'a3' c'est le nombre de zero avent 'a2' : 'a1', 0{'a3'}'a2'

        a1 = l[0]

        a2 = l[1]

        a3 = l[2]
        
        a4 = l[3]

        m = [0, 0, number_of_digit_after_the_floating_pointax - 1, 1]

        if (n > 0):

            a = a1 * a4

            f = False

            if (a2 != 0):

                s_ = str(a2)

                if ((number_of_digit_after_the_floating_pointax < len(str(a2))) or (a3 > 0)):

                    s_ = ""

                    s = str(a2)

                    i = 0

                    while (i < a3):

                        s_ += "0"

                        i += 1

                    # print("s_ = ", s_)

                    i = 0

                    while (i < len(s)):

                        s_ += s[i]

                        i += 1

                # print("a1 = ", a1, " . s_ = ", s_, " . len(s_) = ", len(s_), " . a3 = ", a3)

                a = int(str(a1 * a4) + s_)


                f = True

            if (not f):

                x = my_puissance(a=a, n=n)

                if (x < 0):
                    
                    a4 = -1
                    
                    x = -x
                    
                else:
                    
                    a4 = 1

                m = [x, 0, number_of_digit_after_the_floating_pointax - 1, a4]

                #print("m = ", m, " . a = ", a)

            else:

                i = 0

                m1 = 1

                while (i < n):

                    m1 = m1 * a

                    i += 1

                #print("i = ", i, " . m1 = ", m1, " . len(str(m1)) = ", len(str(m1)), " . a = ", a, " . len(str(a)) = ", len(str(a)))

                l1 = my_div(a=m1, b=my_puissance(a=10, n=(n * number_of_digit_after_the_floating_pointax)), number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)
                
                #print("l1 = ", l1)
                

                if (m1 < 0):
                    
                    a4 = -1
                    
                else:
                    
                    a4 = 1
                
                m = []
                
                i = 0
                
                while (i < len(l1)):
                    
                    m.append(l1[i])
                    
                    i += 1
                    
                m.append(a4)

        elif (n == 0):

            m = [1, 0, number_of_digit_after_the_floating_pointax - 1, 1]

        return m


    def liste_number_of_digit_after_the_floating_pointax_to_n_1(l, number_of_digit_after_the_floating_pointax):
        
        # renvoi le nombre de 'l' compatible avec numba
        
        m = 0
        
        if (number_of_digit_after_the_floating_pointax > 0):
        
            m = l[0] * my_puissance(a=10, n=number_of_digit_after_the_floating_pointax)
        
            m += l[1]
        
        else:
            
            m = l[0] * 10
            
            m += l[1]
        
        m = m * l[3]
        
        return m



    def n_to_liste_number_of_digit_after_the_floating_pointax_1(n, number_of_digit_after_the_floating_pointax):

        # transform une liste 'l' en numereau 'n' compatible avec numba
        
        a4 = 1
        
        #print("n = ", n)
        
        if (n < 0):
            
            a4 = -1
            
            n = -n
        
        a = my_div(a=n, b=my_puissance(a=10, n=number_of_digit_after_the_floating_pointax), number_of_digit_after_the_floating_pointax=1)
        
        a1 = a[0]
        
        a2 = n - (a1 * my_puissance(a=10, n=number_of_digit_after_the_floating_pointax))
        
        #print("a = ", a, " . a1 = ", a1, " . a2 = ", a2)
        
        i = 0
        
        while (my_puissance(a=10, n=i) <= a2):
            
            i += 1
            
        if (i == 0):
            
            i = 1
            
        a3 = number_of_digit_after_the_floating_pointax - i
        
        return [a1, a2, a3, a4]
        
        



    def my_puissance_2(l, n, number_of_digit_after_the_floating_pointax):
        
        # compatible avec numba

        # calcule la puissance 'l' de 'n' avec 'number_of_digit_after_the_floating_pointax' nombre de numereau apres la vergule

        # 'a3' c'est le nombre de zero avent 'a2' : 'a1', 0{'a3'}'a2'

        d = liste_number_of_digit_after_the_floating_pointax_to_n_1(l=l, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)
        
        d = my_puissance(a=d, n=n)
        
        t = 1
        
        if (l[3] == -1):
        
            t = my_puissance(a=-1, n=n)

        # d1 = my_div(a=d, b=my_puissance(a=10, n=((n - 1) * number_of_digit_after_the_floating_pointax)), number_of_digit_after_the_floating_pointax=1)

        d1 = [d // my_puissance(a=10, n=((n - 1) * number_of_digit_after_the_floating_pointax))]

        d = d1[0]

        d2 = n_to_liste_number_of_digit_after_the_floating_pointax_1(n=d, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

        d2[3] = t
        
        return d2


    def n_de_my_puissance_1(L, number_of_digit_after_the_floating_pointax):

        # renvoi le 'int(s)' pour my_puissance_1

        i = len(str(L))

        s = str(L)

        while (i < number_of_digit_after_the_floating_pointax):

            s += "0"

            i += 1

        return int(s)




    def mod(a, b):

        # retourne le mode 'a' à 'b'

        r = my_div(a=a, b=b, number_of_digit_after_the_floating_pointax=1)

        r2 = r[0] * b

        r3 = a - r2

        return r3




    def pgcd(a, b):

        # trouve le PGCD entre 'a' et 'b'

        r0 = a

        r1 = b

        r2 = 0
        
        r = mod(a=r0, b=r1)

        while (r != 0):

            r2 = r
            
            r0 = r1

            r1 = r2
            
            r = mod(a=r0, b=r1)

        return r1


    def ppcm(a, b):

        # trouve le ppcm entre 'a' et 'b'

        a1 = my_div(a=a * b, b=pgcd(a=a, b=b), number_of_digit_after_the_floating_pointax=1)
        
        return a1[0]




    def ent(a):
        
        # retourne le nombre entier de 'a'
        
        i = 0
        
        while (my_puissance(a=10, n=i) <= a):
            
            i += 1
            
        d = 0
        
        while (i > -1):
        
            while (d < a):
            
                d += my_puissance(a=10, n=i)
            
            if (d > a):
                
                d -= my_puissance(a=10, n=i)
                
                i -= 1
                
            else:
                
                break
            
            
        return d

    def s_ent(s):
        
        # renvoi le coté entier de numero 's'

        i = 0
        
        s_ = ""
        
        while ((i < len(s)) and (s[i] != ".")):
            
            s_ += s[i]
            
            i += 1
        
        return s_


    def generer_number_of_digit_after_the_floating_pointax(n):

        # genere 'number_of_digit_after_the_floating_pointax' superieur ou egale à 'n'

        o = 2

        if (mod(a=n, b=2) == 0):

            o = n

        else:

            o = n + 1


        return o


    def my_racine(a, n):

        # calcule le racine 'a' de 'n'

        m = 0.0

        if (n == 1):

            m = a

        elif ((a < 0) and (mod(a=n, b=2) == 0)):

            m = 0.0

        elif (n > 1):

            i = 0

            while (i < 11):

                while (my_puissance(a=m, n=n) < a):

                    m = m + my_puissance(a=10, n=(-i))

                if (my_puissance(a=m, n=n) == a):

                    break

                else:

                    m = m - my_puissance(a=10, n=(-i))

                    i += 1

                # print("m = ", m)

        return m



    def liste_number_of_digit_after_the_floating_pointax_to_n(l, number_of_digit_after_the_floating_pointax):

        # renvoi le nombre de 'l'

        s_ = ""
        
        moin = ""
        
        #print("l = ", l)
        
        if (l[3] == -1):
            
            moin = "-"
            
        
        if (number_of_digit_after_the_floating_pointax == len(str(l[1])) + l[2]):
            
            #print("hello 1 .")
            
            if (l[1] != 0):

                s = str(l[1])

                if (l[2] != 0):
                    
                    #print("hello 2 .")

                    i = 0

                    while (i < l[2]):

                        s_ += "0"

                        i += 1
                        
                    #print("h 2 . i = ", i, " . s_ = ", s_)

                i = 0

                while (i < len(s)):

                    s_ += s[i]

                    i += 1
                    
                #print("h 3 . s_ = ", s_)

            else:

                i = 0

                while (i < number_of_digit_after_the_floating_pointax):

                    s_ += "0"

                    i += 1

        else:
            
            i = 0
            
            while (i < my_min(a=l[2], b=number_of_digit_after_the_floating_pointax)):
                
                s_ += "0"
                
                i += 1
                
            ss = str(l[1])
            
            j = 0
            
            while ((j < len(ss)) and (i < number_of_digit_after_the_floating_pointax)):
                
                s_ += ss[j]
                
                j += 1
                
                i += 1
                

        return int(moin + str(l[0]) + s_)    


    def my_inferieur_1(l1, l2, number_of_digit_after_the_floating_pointax):

        # inferieur : <

        res = False

        d1 = liste_number_of_digit_after_the_floating_pointax_to_n_1(l=l1, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

        d2 = liste_number_of_digit_after_the_floating_pointax_to_n_1(l=l2, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

        if (d1 < d2):

            res = True

        else:

            res = False

        return res


    def my_superieur_1(l1, l2, number_of_digit_after_the_floating_pointax):

        # superieur : >

        res = False

        d1 = liste_number_of_digit_after_the_floating_pointax_to_n_1(l=l1, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

        d2 = liste_number_of_digit_after_the_floating_pointax_to_n_1(l=l2, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

        if (d1 > d2):

            res = True

        else:

            res = False

        return res



    def my_egale_1(l1, l2, number_of_digit_after_the_floating_pointax):

        # egale : =

        res = False

        d1 = liste_number_of_digit_after_the_floating_pointax_to_n_1(l=l1, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

        d2 = liste_number_of_digit_after_the_floating_pointax_to_n_1(l=l2, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

        if (d1 == d2):

            res = True

        else:

            res = False

        return res


    def n_to_liste_number_of_digit_after_the_floating_pointax(n, number_of_digit_after_the_floating_pointax):

        # transform une liste 'l' en numereau 'n'

        n1 = str(n)
        
        n2 = n1
        
        moin = False
        
        a1 = 0

        a2 = 0

        a3 = 0
        
        a4 = 1

        
        if (n < 0):
            
            moin = True
            
            a4 = -1
            
            n = -n
            
            i = 1
            
            n2 = ""
            
            while (i < len(n1)):
                
                n2 += n1[i]
                
                i += 1

        
        if (number_of_digit_after_the_floating_pointax < len(n2)):

            
            s = ""

            i = 0

            while (i < len(n2) - number_of_digit_after_the_floating_pointax):

                s += n2[i]

                i += 1

            # print("1 . s = ", s)

            if (s != ""):

                a1 = int(s)


            a3 = 0

            while ((i < len(n2)) and (n2[i] == "0")):

                a3 += 1

                i += 1

            if (i == len(n2)):

                a3 -= 1

            s = ""

            while (i < len(n2)):

                s += n2[i]

                i += 1

            if (s != ""):

                # print("2 . s = ", s)

                a2 = int(s)

        else:

            a1 = 0

            a2 = n

            a3 = number_of_digit_after_the_floating_pointax - len(str(a2))
            
        return [a1, a2, a3, a4]


    def my_div_1(l_a, l_b, number_of_digit_after_the_floating_pointax):

        # my_division 'l_a' / 'l_b'

        #print("l_a = ", l_a, " . l_b = ", l_b)

        d1 = liste_number_of_digit_after_the_floating_pointax_to_n_1(l=l_a, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

        d2 = liste_number_of_digit_after_the_floating_pointax_to_n_1(l=l_b, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

        #print("d1 = ", d1, " . d2 = ", d2)

        d3 = my_div(a=d1, b=d2, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)



        d = 1

        if (l_a[3] * l_b[3] <= 0):

            d = -1
            
        l = []
        
        i = 0
        
        while (i < len(d3)):
            
            l.append(d3[i])
            
            i += 1
            
        l.append(d)
        
        #print("l = ", l)
            
        #print("d1 = ", d1, " . d2 = ", d2, " . d3 = ", d3)

        return l


    def my_multip_1(l_a, l_b, number_of_digit_after_the_floating_pointax):

        # my_multiplication  'l_a' * 'l_b'

        d1 = liste_number_of_digit_after_the_floating_pointax_to_n_1(l=l_a, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

        d2 = liste_number_of_digit_after_the_floating_pointax_to_n_1(l=l_b, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

        d3 = d1 * d2
        
        mo = 1
        
        if (d3 < 0):
            
            d3 = -d3
            
            mo = -1

        
        d4 = n_to_liste_number_of_digit_after_the_floating_pointax_1(n=d3, number_of_digit_after_the_floating_pointax=(number_of_digit_after_the_floating_pointax * 2))


        d4[3] = mo

        return d4


    def my_moin_1(l_a, l_b, number_of_digit_after_the_floating_pointax):

        # my_moin  'l_a' - 'l_b'

        d1 = liste_number_of_digit_after_the_floating_pointax_to_n_1(l=l_a, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

        d2 = liste_number_of_digit_after_the_floating_pointax_to_n_1(l=l_b, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

        d3 = d1 - d2

        d4 = n_to_liste_number_of_digit_after_the_floating_pointax_1(n=d3, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

        return d4


    def my_plus_1(l_a, l_b, number_of_digit_after_the_floating_pointax):

        # my_plus  'l_a' + 'l_b'

        d1 = liste_number_of_digit_after_the_floating_pointax_to_n_1(l=l_a, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

        d2 = liste_number_of_digit_after_the_floating_pointax_to_n_1(l=l_b, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

        d3 = d1 + d2

        d4 = n_to_liste_number_of_digit_after_the_floating_pointax_1(n=d3, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

        return d4


    def my_racine_1(l, n, number_of_digit_after_the_floating_pointax):

        # calcule  'l' R 'b' avec 'number_of_digit_after_the_floating_pointax' nombre de numereau apres la vergule

        m = [0, 0, number_of_digit_after_the_floating_pointax - 1, 1]

        d = 0

        d1 = liste_number_of_digit_after_the_floating_pointax_to_n(l=l, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

        #print("1 . d1 = ", d1 , " . len(str(d1)) = ", len(str(d1)))    

        d1 = d1 * my_puissance(a=10, n=((n - 1) * number_of_digit_after_the_floating_pointax))

        #print("2 . d1 = ", d1 , " . len(str(d1)) = ", len(str(d1)))
        
        mo = 1
        
        if (d1 < 0):
        
            d1 = -d1

            mo = -1

        i = 0

        while (-1 < i):

            i = 0

            o = d

            t = 0

            # print("m = ", m, " . n = ", n, " _ = ", my_puissance(a=m, n=n))

            while (my_puissance(a=d, n=n) < d1):

                if (t < 10):

                    d = d + my_puissance(a=10, n=i)

                    t += 1
                    
                else:
                    
                    t = 0
                    
                    d = o
                    
                    i += 1

                #print("i = ", i, " . t = ", t, " . d = ", d, " . my_puissance(a=d, n=n) = ", my_puissance(a=d, n=n), " . d1 = ", d1)

            #print("i = ", i, " . m = ", m, " . d = ", d, " . len(str(d)) = ", len(str(d)), " . len(str(d1)) = ", len(str(d1)), " . d1 = ", d1, " . _ = ", (my_puissance(a=d, n=n) > d1))

            if (my_puissance(a=d, n=n) > d1):

                d = d - my_puissance(a=10, n=i)

                i -= 1

            # if (i < 0):
            #
            #     break
            #
            # # print("1 . i = ", i, " . m = ", m)
            #
            # i = 0

        m = n_to_liste_number_of_digit_after_the_floating_pointax(n=d, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

        if (mod(a=n, b=2) == 1):
            
            m[3] = mo

        return m



    def my_racine_2(l, n, number_of_digit_after_the_floating_pointax):

        # compatible avec numba

        # calcule  'l' R 'b' avec 'number_of_digit_after_the_floating_pointax' nombre de numereau apres la vergule

        m = [0, 0, number_of_digit_after_the_floating_pointax - 1, 1]

        d = 0

        d1 = liste_number_of_digit_after_the_floating_pointax_to_n_1(l=l, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

        d1 = d1 * my_puissance(a=10, n=((n - 1) * number_of_digit_after_the_floating_pointax))
        
        mo = 1
        
        if (d1 < 0):
        
            d1 = -d1

            mo = -1

        i = n * number_of_digit_after_the_floating_pointax
        
        q = my_puissance(a=10, n=i)

        while (q <= d1):
            
            q = q * 10
            
            i += 1

        o = 0

        while (-1 < i):

            o = my_puissance(a=d, n=n)
            
            # print("m = ", m, " . n = ", n, " _ = ", my_puissance(a=m, n=n))

            while (o < d1):
                
                d = d + my_puissance(a=10, n=i)

                o = my_puissance(a=d, n=n)

                # print("i = ", i, " . m = ", m, " . d = ", d)

            # print("i = ", i, " . m = ", m, " . d = ", d, " . len(str(d)) = ", len(str(d)), " . len(d1) = ", len(str(d1)), " . d1 = ", d1, " . _ = ", (my_puissance(a=d, n=n) == d1))

            if (o > d1):

                d = d - my_puissance(a=10, n=i)

                i -= 1
                
            else:
                
                break

            
        m = n_to_liste_number_of_digit_after_the_floating_pointax_1(n=d, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

        if (mod(a=n, b=2) == 1):
            
            m[3] = mo

        return m






    def s_n_to_liste_number_of_digit_after_the_floating_pointax(s, number_of_digit_after_the_floating_pointax):

        # transforme 's' en liste_number_of_digit_after_the_floating_pointax

        a1 = 0

        a2 = 0

        a3 = 0
        
        a4 = 1

        point = False

        s1 = ""

        i = 0

        while ((i < len(s)) and ((s[i] == '+') or (s[i] == '-'))):

            if (s[i] == '-'):
                
                a4 = -a4
                
            i += 1

        #print("_1 . s1 = ", s1)

        while ((i < len(s)) and (s[i] != '.')):

            s1 += s[i]

            i += 1

        #print("s1 = ", s1, " . s = ", s)

        if ((i < len(s)) and (s[i] == '.')):

            point = True

            i += 1

        #print("1 . s1 = ", s1, " . point = ", point, " . s = ", s)

        if (s1 != ""):

            a1 = int(s1)
            
            # if (a1 < 0):
                
            #     a4 = -1
                
            #     a1 = -a1


        a3 = 0

        j = 0

        while ((i < len(s)) and (s[i] == "0") and (a3 < number_of_digit_after_the_floating_pointax)):

            a3 += 1

            i += 1

            j += 1

        if ((a3 > 0) and ((i == len(s)) or (a3 == number_of_digit_after_the_floating_pointax))):

            a3 -= 1

        s1 = ""

        while ((i < len(s)) and (j < number_of_digit_after_the_floating_pointax)):

            s1 += s[i]

            i += 1

            j += 1

        # print("2 . s1 = ", s1, " . j = ", j)

        if (j < number_of_digit_after_the_floating_pointax):

            if ((point) and (s1 != "") and (int(s1) != 0)):

                while (j < number_of_digit_after_the_floating_pointax):

                    s1 += "0"

                    j += 1

            else:

                a2 = 0

                a3 = number_of_digit_after_the_floating_pointax - 1

        if (s1 != ""):

            # print("3 . s1 = ", s1, " . len(s1) = ", len(s1))

            a2 = int(s1)


        return [a1, a2, a3, a4]

    def liste_number_of_digit_after_the_floating_pointax_to_s_n(l, number_of_digit_after_the_floating_pointax):

        # transforme une liste_number_of_digit_after_the_floating_pointax 'l' en s

        #d = liste_number_of_digit_after_the_floating_pointax_to_n(l=l, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

        #print("l = ", l, " . d = ", d)


        s = ""

        
        #sd = str(d)

        # t = len(sd) - number_of_digit_after_the_floating_pointax

        # # print("t = ", t)

        # while (i < t):

        #     s += sd[i]

        #     i += 1

        # if (s == ""):

        #     s = "0"

        # if (s == "-"):
            
        #     s = "-0"

        # s += "."

        # while (i < len(sd)):

        #     s += sd[i]

        #     i += 1


        
        s = str(l[0])
        
        if (l[3] == -1):
            
            s = "-" + s
            
        #if (l[1] != 0):
            
        s += "."
            
        i = 0
        
        while (i < l[2]):
            
            s += "0"
            
            i += 1
            
        s += str(l[1])
        

        return s




    def cos_sin(alpha_1):

        # calcule le cos et le sin de 'alpha_1'

        alpha = alpha_1 / math.pi

        x = 0

        y = 0

        a = mod(a=alpha, b=(1 / 2))

        if (a == 0):

            x = 1

            y = 0

        else:

            x = my_racine(a=(1 - (1 / (my_puissance(a=((1 / (2 * a)) - 1), n=2) + 1))), n=2)

            y = my_racine(a=(1 / (my_puissance(a=((1 / (2 * a)) - 1), n=2) + 1)), n=2)

        b = int(alpha / (1 / 2))

        c = mod(a=b, b=4)

        if (c == 0):

            # 1er care

            x = x

            y = y

        elif (c == 1):

            # 2eme care

            x_ = x

            x = -y

            y = x_

        elif (c == 2):

            # 3eme care

            x = -x

            y = -y

        elif (c == 3):

            # 4eme care

            x_ = x

            x = y

            y = -x_

        return [x, y]



    def cocos_cosin(x, y):

        # calcule le alpha_1

        r = 0

        if ((x >= 0) and (y >= 0)):

            # 1er care

            r = 0

        elif ((x <= 0) and (y >= 0)):

            # 2eme care

            r = 1

        elif ((x <= 0) and (y <= 0)):

            # 3eme care

            r = 2

        elif ((x >= 0) and (y <= 0)):

            # 4eme care

            r = 3

        x = my_abs(a=x)

        y = my_abs(a=y)

        return (((y * math.pi) / (2 * (x + y))) + (r * math.pi))



    def plus_one_in_l_c(l_c, l, n):

        # n_comence_par_0

        # plus 1 avec la liste l_c

        the_max_number = len(l_c)

        i = n

        l[i] += 1

        if (l[i] == the_max_number):

            l[i] = 0

            i += 1

            # print(" - l = ", l, " . i = ", i)

            if (len(l) < i + 1):

                l.append(0)

                # print("- l = ", l)

            else:

                plus_one_in_l_c(l_c=l_c, l=l, n=i)


    def list_l_c_to_s(l_c, l):

        # transforme l à s par l_c

        s = ""

        i = 0

        while (i < len(l)):

            t = l[i]

            s = l_c[t] + s

            # print("t = ", t, " . s = ", s, " . i = ", i)

            i += 1

        return s

    def from_int_to_list_l_c(l_c, n):

        # transforme n à une liste l depuit l_c

        l = [0]

        i = 0

        while (i < n):

            plus_one_in_l_c(l_c=l_c, l=l, n=0)

            i += 1

        return l


    def check_parentheses(s):

        # check si les parentheses sont correcte

        r = False

        i = 0

        t = 0
        
        g = False

        g_ = ""

        while (i < len(s)):
            
            if ((s[i] == '"') or (s[i] == '\'')):
                
                if (((i - 1 > -1) and (s[i - 1] != '\\')) or (i == 0)):
                
                    if (g_ == ""):
                    
                        g_ = s[i]
                    
                        g = True

                    elif (g_ == s[i]):
                        
                        g_ = ""
                        
                        g = False
            
            if (not g):

                if (s[i] == '('):

                    t += 1

                elif (s[i] == ')'):

                    t -= 1

            i += 1

        if (t == 0):

            r = True

        else:

            r = False

        return r


    def ajoute_parentheses(s, a, b):

        # ajoute deux parentheses à a et b

        s_ = ""

        if ((a < b) and (b < len(s))):

            i = 0

            while (i < a):

                s_ += s[i]

                i += 1

            s_ += "("

            while (i < b):

                s_ += s[i]

                i += 1

            s_ += ")"

            while (i < len(s)):

                s_ += s[i]

                i += 1

        return s_



    def is_numereau(s):

        # check si s contien un numereau

        i = 0

        res = True
        
        if ((len(s) > 0) and (s[0] == '.')):
            
            res = False
        
        else:

            while ((i < len(s)) and ((s[i] == '+') or (s[i] == '-'))):

                i += 1

            if (len(s) == i):

                res = False

            o = 0

            while ((i < len(s)) and (res)):

                if (((s[i] == '0') or (s[i] == '1') or (s[i] == '2') or (s[i] == '3') or (s[i] == '4') or (s[i] == '5') or
                    (s[i] == '6') or (s[i] == '7') or (s[i] == '8') or (s[i] == '9') or (s[i] == '.')) and (o < 2)):

                    res = True

                else:

                    res = False

                if (s[i] == '.'):

                    o += 1

                # print("i = ", i, " . s[i] = ", s[i], " . o = ", o)

                i += 1

        if ((res) and (s[len(s) - 1] == '.')):
            
            res = False


        return [res, o]





    def supprime_espace(s):

        # supprime tout les espaces de s

        s_ = ""

        g = False
        
        g_ = ""

        i = 0

        while (i < len(s)):

            if ((s[i] == '"') or (s[i] == '\'')):
                
                if ((i == 0) or ((i - 1 > -1) and (s[i - 1] != '\\'))):
                    
                    if (g_ == ""):
                        
                        g = True
                        
                        g_ = s[i]
                        
                    elif (g_ == s[i]):
                        
                        g_ = ""
                        
                        g = False
                        

            if (not g):

                if (s[i] != ' '):

                    s_ += s[i]

            else:
                
                s_ += s[i]

            i += 1

        return s_


    def s_to_liste(s):

        # transforme s en liste l

        l = []

        erreur = False

        s = supprime_espace(s=s)

        i = 0

        s_ = ""

        while ((i < len(s)) and (not erreur)):

            if ((s[i] == '(') or (s[i] == ')') or (s[i] == '*') or (s[i] == '+') or (s[i] == '/') or (s[i] == '-') or
                    (s[i] == '^') or (s[i] == 'R')):

                if ((s_ != '') and (is_numereau(s_)[0])):

                    erreur = False

                elif (s_ != ''):

                    erreur = True

                # print("i = ", i, " . s[i] = ", s[i], " . s_ = ", s_, " . erreur = ", erreur)

                if ((s_ != '')):

                    l.append(s_)

                l.append(s[i])

                s_ = ""

            else:

                s_ += s[i]

            i += 1

        if ((len(s) > 0) and (s_ != "")):

            if (not (is_numereau(s=s_)[0])):

                erreur = True

            l.append(s_)

        return [erreur, l]



    def s_to_numereau(s):

        # transforme s à un numereau

        res = 0

        s = supprime_espace(s=s)

        if (is_numereau(s=s)[0]):

            t = 1

            i = 0

            while ((i < len(s)) and ((s[i] == '+') or (s[i] == '-'))):

                if (s[i] == '+'):

                    t = t

                elif (s[i] == '-'):

                    t = -t

                i += 1

            # print("s = ", s, " . t = ", t)

            s_1 = ""

            o = False

            while ((i < len(s)) and (not o)):

                if (s[i] == '.'):

                    o = True

                else:

                    s_1 += s[i]

                    i += 1

            s_2 = ""

            if (o):

                i += 1

                while (i < len(s)):

                    s_2 += s[i]

                    i += 1

            if (s_1 != ""):

                res = int(s_1)

            if ((s_2 != "") and (int(s_2) != 0)):

                res += int(s_2) / my_puissance(a=10, n=len(s_2))

            # print("s_1 = ", s_1, " . s_2 = ", s_2, " . res = ", res)

            res = res * t

        return res


    def assemble(l, n):

        # asemble deux element 'n' et 'n + 1' dans la liste l

        m = []

        # print("assemblage")

        if (n < len(l)):

            i = 0

            while (i < n):

                m.append(l[i])

                i += 1

            t = ""

            t += l[i]

            if (i + 1 < len(l)):

                i += 1

                t += l[i]

            m.append(t)

            i += 1

            while (i < len(l)):

                m.append(l[i])

                i += 1

        return m


    def check_erreur(l):

        # check les erreur de la liste l

        erreur = False

        i = 0

        while ((i < len(l)) and (not erreur)):

            # print("l[i] = ", l[i])

            if ((l[i] == '+') or (l[i] == '-')):

                if ((i == 0) and (i + 1 < len(l)) and (is_numereau(s=l[i + 1])[0])):

                    l = assemble(l=l, n=i)

                    erreur = False

                elif ((i > 0) and (i + 1 < len(l)) and ((l[i - 1] == "*") or (l[i - 1] == "/") or
                        (l[i - 1] == "^") or (l[i - 1] == "R") or (l[i - 1] == "+") or (l[i - 1] == "-")) and
                    (is_numereau(s=l[i + 1])[0])):

                    l = assemble(l=l, n=i)

                    erreur = False


                elif ((i > 0) and (l[i - 1] == '(') and (i + 1 < len(l)) and (is_numereau(s=l[i + 1])[0])):

                    l = assemble(l=l, n=i)

                    erreur = False

                elif ((i > 0) and (i + 1 < len(l)) and (is_numereau(s=l[i - 1])[0]) and ((l[i + 1] == "+") or (l[i + 1] == "-"))):

                    erreur = False

                elif ((i > 0) and (l[i - 1] == '(') and (i + 1 < len(l)) and (l[i + 1] == '(')):

                    erreur = False

                elif ((i > 0) and (i + 1 < len(l)) and (is_numereau(s=l[i - 1])[0]) and (is_numereau(s=l[i + 1])[0])):

                    erreur = False

                elif ((i > 0) and (i + 1 < len(l)) and (l[i - 1] == ')') and (l[i + 1] == '(')):

                    erreur = False

                elif ((i > 0) and (i + 1 < len(l)) and (l[i - 1] == ')') and (is_numereau(s=l[i + 1])[0])):

                    erreur = False

                elif ((i > 0) and (i + 1 < len(l)) and (is_numereau(s=l[i - 1])[0]) and (l[i + 1] == '(')):

                    erreur = False

                else:

                    erreur = True

            elif ((l[i] == '*') or (l[i] == '/') or (l[i] == 'R') or (l[i] == '^')):

                if ((i > 0) and (i + 1 < len(l)) and (is_numereau(s=l[i - 1])[0]) and (is_numereau(s=l[i + 1])[0])):

                    erreur = False
                    
                elif ((i > 0) and (i + 1 < len(l)) and ((l[i + 1] == "+") or (l[i + 1] == "-"))):
                    
                    erreur = False

                elif ((i > 0) and (i + 1 < len(l)) and (is_numereau(s=l[i - 1])[0]) and (l[i + 1] == '(')):

                    erreur = False

                elif ((i > 0) and (i + 1 < len(l)) and (l[i - 1] == ')') and (is_numereau(s=l[i + 1])[0])):

                    erreur = False

                elif ((i > 0) and (i + 1 < len(l)) and (l[i - 1] == ')') and (l[i + 1] == '(')):

                    erreur = False

                else:

                    erreur = True

            elif (l[i] == ')'):

                if ((i + 1 < len(l)) and (l[i + 1] == '(')):

                    erreur = True

                elif ((i + 1 < len(l)) and (l[i + 1] != "+") and (l[i + 1] != "-") and (l[i + 1] != "*")
                    and (l[i + 1] != "/") and (l[i + 1] != "^") and (l[i + 1] != "R") and (l[i + 1] != ')')):

                    erreur = True


            elif (l[i] == '('):

                if ((i - 1 > -1) and (l[i - 1] == ')')):

                    erreur = True

                elif ((i - 1 > -1) and (l[i - 1] != "+") and (l[i - 1] != "-") and (l[i - 1] != "*")
                    and (l[i - 1] != "/") and (l[i - 1] != "^") and (l[i - 1] != "R") and (l[i - 1] != '(')):

                    erreur = True

            elif (is_numereau(s=l[i])):

                if ((i - 1 > -1) and (l[i - 1] != "+") and (l[i - 1] != "-") and (l[i - 1] != "*")
                        and (l[i - 1] != "/") and (l[i - 1] != "^") and (l[i - 1] != "R") and (l[i - 1] != '(')):
                    erreur = True

                if ((i + 1 < len(l)) and (l[i + 1] != "+") and (l[i + 1] != "-") and (l[i + 1] != "*")
                        and (l[i + 1] != "/") and (l[i + 1] != "^") and (l[i + 1] != "R") and (l[i + 1] != ')')):
                    erreur = True

            #print("check_erreur . i = ", i, " . l[i] = ", l[i], " . erreur = ", erreur)

            i += 1

        return [erreur, l]


    def calcule(a, o, b):

        # clacule les deux nombre a et b avec l'operateur o

        res = 0

        erreur = False

        if (o == '+'):

            res = s_to_numereau(s=a) + s_to_numereau(s=b)

        elif (o == '-'):

            res = s_to_numereau(s=a) - s_to_numereau(s=b)

        elif (o == '*'):

            res = s_to_numereau(s=a) * s_to_numereau(s=b)

        elif (o == '/'):

            if (s_to_numereau(s=b) == 0):

                erreur = True

            else:

                res = s_to_numereau(s=a) / s_to_numereau(s=b)

        elif (o == '^'):

            t = is_numereau(s=b)

            if ((t[0]) and (t[1] == 0)):

                t_1 = s_to_numereau(s=b)

                t_2 = s_to_numereau(s=a)

                if ((t_1 < 0) and (t_2 == 0)):

                    erreur = True

                elif ((t_1 == 0) and (t_2 == 0)):

                    erreur = True

                else:

                    res = my_puissance(a=s_to_numereau(s=a), n=s_to_numereau(s=b))

            elif (t[0]):

                i = 0

                while (b[i] != '.'):

                    i += 1

                i += 1

                s = ""

                while (i < len(b)):

                    s += b[i]

                    i += 1

                if (int(s) == 0):

                    t_1 = s_to_numereau(s=b)

                    t_2 = s_to_numereau(s=a)

                    if ((t_1 < 0) and (t_2 == 0)):

                        erreur = True

                    elif ((t_1 == 0) and (t_2 == 0)):

                        erreur = True

                    else:

                        res = my_puissance(a=s_to_numereau(s=a), n=s_to_numereau(s=b))

                else:

                    erreur = True

            else:

                erreur = True

        elif ((o == 'R') or (o == 'r')):

            t = is_numereau(s=b)

            h1 = s_to_numereau(s=a)

            h = s_to_numereau(s=b)

            if ((h1 < 0) and (mod(a=h, b=2) == 0)):

                erreur = True

            elif ((t[0]) and (t[1] == 0) and (h > 0)):

                res = my_racine(a=s_to_numereau(s=a), n=s_to_numereau(s=b))

            elif ((t[0]) and (h > 0)):

                i = 0

                while (b[i] != '.'):

                    i += 1

                i += 1

                s = ""

                while (i < len(b)):

                    s += b[i]

                    i += 1

                if (int(s) == 0):

                    res = my_racine(a=s_to_numereau(s=a), n=s_to_numereau(s=b))

                else:

                    erreur = True


            else:

                erreur = True

        return [erreur, res]


    def calcule_1(a, o, b, number_of_digit_after_the_floating_pointax):

        # clacule les deux nombre a et b avec l'operateur o

        res = ""

        erreur = False

        # print("l_a = ", s_n_to_liste_number_of_digit_after_the_floating_pointax(s=a, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax))

        # print("l_b = ", s_n_to_liste_number_of_digit_after_the_floating_pointax(s=b, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax))

        #print("a = ", a, " . b = ", b, " . o = ", o)

        res_1 = []

        if (o == '+'):

            res_1 = my_plus_1(l_a=s_n_to_liste_number_of_digit_after_the_floating_pointax(s=a, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax), l_b=s_n_to_liste_number_of_digit_after_the_floating_pointax(s=b, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax), number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

            res = liste_number_of_digit_after_the_floating_pointax_to_s_n(l=res_1, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

        elif (o == '-'):

            res_1 = my_moin_1(l_a=s_n_to_liste_number_of_digit_after_the_floating_pointax(s=a, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax), l_b=s_n_to_liste_number_of_digit_after_the_floating_pointax(s=b, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax), number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

            res = liste_number_of_digit_after_the_floating_pointax_to_s_n(l=res_1, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

        elif (o == '*'):

            res_1 = my_multip_1(l_a=s_n_to_liste_number_of_digit_after_the_floating_pointax(s=a, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax), l_b=s_n_to_liste_number_of_digit_after_the_floating_pointax(s=b, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax), number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

            res = liste_number_of_digit_after_the_floating_pointax_to_s_n(l=res_1, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

        elif (o == '/'):

            s_b = s_n_to_liste_number_of_digit_after_the_floating_pointax(s=b, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

            if ((s_b[0] == 0) and (s_b[1] == 0)):

                erreur = True

            else:

                res_1 = my_div_1(l_a=s_n_to_liste_number_of_digit_after_the_floating_pointax(s=a, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax), l_b=s_n_to_liste_number_of_digit_after_the_floating_pointax(s=b, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax), number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

                res = liste_number_of_digit_after_the_floating_pointax_to_s_n(l=res_1, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

        elif (o == '^'):

            t = is_numereau(s=b)
            
            b_ = s_to_numereau(s=b)
            
            #print("b_ = ", b_)

            if ((t[0]) and (t[1] == 0) and (b_ >= 0)):

                s_b = s_n_to_liste_number_of_digit_after_the_floating_pointax(s=b, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

                s_a = s_n_to_liste_number_of_digit_after_the_floating_pointax(s=a, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

                if ((s_b[0] < 0) and (s_a[0] == 0) and (s_a[1] == 0)):

                    erreur = True

                elif ((s_b[0] == 0) and (s_b[1] == 0) and (s_a[0] == 0) and (s_a[1] == 0)):

                    erreur = True

                else:

                    res_1 = my_puissance_1(l=s_n_to_liste_number_of_digit_after_the_floating_pointax(s=a, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax), n=s_to_numereau(s=b), number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

                    res = liste_number_of_digit_after_the_floating_pointax_to_s_n(l=res_1, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

            elif ((t[0]) and (b_ >= 0)):

                i = 0

                while (b[i] != '.'):

                    i += 1

                i += 1

                s = ""

                while (i < len(b)):

                    s += b[i]

                    i += 1

                if (int(s) == 0):

                    s_b = s_n_to_liste_number_of_digit_after_the_floating_pointax(s=b, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

                    s_a = s_n_to_liste_number_of_digit_after_the_floating_pointax(s=a, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

                    if ((s_b[0] < 0) and (s_a[0] == 0) and (s_a[1] == 0)):

                        erreur = True

                    elif ((s_b[0] == 0) and (s_b[1] == 0) and (s_a[0] == 0) and (s_a[1] == 0)):

                        erreur = True

                    else:

                        res_1 = my_puissance_1(l=s_n_to_liste_number_of_digit_after_the_floating_pointax(s=a, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax), n=s_to_numereau(s=b), number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

                        res = liste_number_of_digit_after_the_floating_pointax_to_s_n(l=res_1, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

                else:
                    
                    
                    s = b.split(".")
                    
                    a1 = s[0] + s[1]
                    
                    b1 = my_puissance(a=10, n=len(s[1]))
                    
                    d = pgcd(a=int(a1), b=b1)
                    
                    a2 = int(a1) / d
                    
                    b2 = b1 / d
                    
                    #print("a2 = ", a2, " . b2 = ", b2)
                    
                    res_1 = my_puissance_1(l=s_n_to_liste_number_of_digit_after_the_floating_pointax(s=a, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax), n=a2, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

                    res_1 = my_racine_1(l=res_1, n=b2, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

                    res = liste_number_of_digit_after_the_floating_pointax_to_s_n(l=res_1, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)


                    #erreur = True

            else:

                erreur = True

        elif ((o == 'R') or (o == 'r')):

            t = is_numereau(s=b)

            s_b = s_n_to_liste_number_of_digit_after_the_floating_pointax(s=b, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

            s_a = s_n_to_liste_number_of_digit_after_the_floating_pointax(s=a, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

            # if ((h1 < 0) and (mod(a=h, b=2) == 0)):
            #
            #     erreur = True

            if ((t[0]) and (t[1] == 0) and (s_b[0] > 0)):

                if ((s_a[0] < 0) and (mod(a=s_b[0], b=2) == 0)):

                    erreur = True

                else:

                    res_1 = my_racine_1(l=s_n_to_liste_number_of_digit_after_the_floating_pointax(s=a, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax), n=s_to_numereau(s=b), number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

                    res = liste_number_of_digit_after_the_floating_pointax_to_s_n(l=res_1, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

            elif ((t[0]) and (s_b[0] > 0)):

                i = 0

                while (b[i] != '.'):

                    i += 1

                i += 1

                s = ""

                while (i < len(b)):

                    s += b[i]

                    i += 1

                if (int(s) == 0):

                    if ((s_a[0] < 0) and (mod(a=s_b[0], b=2) == 0)):

                        erreur = True

                    else:

                        res_1 = my_racine_1(l=s_n_to_liste_number_of_digit_after_the_floating_pointax(s=a, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax), n=s_to_numereau(s=b), number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

                        res = liste_number_of_digit_after_the_floating_pointax_to_s_n(l=res_1, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

                else:

                    erreur = True

            else:

                erreur = True

        # print("res_1 = ", res_1)

        return [erreur, res]



    def calcule_2(a, o, b, number_of_digit_after_the_floating_pointax):

        # clacule les deux nombre a et b avec l'operateur o

        res = ""

        erreur = False

        # print("l_a = ", s_n_to_liste_number_of_digit_after_the_floating_pointax(s=a, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax))

        # print("l_b = ", s_n_to_liste_number_of_digit_after_the_floating_pointax(s=b, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax))

        #print("a = ", a, " . b = ", b, " . o = ", o)

        res_1 = []

        if (o == '+'):

            res_1 = my_plus_1(l_a=s_n_to_liste_number_of_digit_after_the_floating_pointax(s=a, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax), l_b=s_n_to_liste_number_of_digit_after_the_floating_pointax(s=b, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax), number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

            res = liste_number_of_digit_after_the_floating_pointax_to_s_n(l=res_1, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

        elif (o == '-'):

            res_1 = my_moin_1(l_a=s_n_to_liste_number_of_digit_after_the_floating_pointax(s=a, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax), l_b=s_n_to_liste_number_of_digit_after_the_floating_pointax(s=b, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax), number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

            res = liste_number_of_digit_after_the_floating_pointax_to_s_n(l=res_1, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

        elif (o == '*'):

            res_1 = my_multip_1(l_a=s_n_to_liste_number_of_digit_after_the_floating_pointax(s=a, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax), l_b=s_n_to_liste_number_of_digit_after_the_floating_pointax(s=b, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax), number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

            res = liste_number_of_digit_after_the_floating_pointax_to_s_n(l=res_1, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

        elif (o == '/'):

            s_b = s_n_to_liste_number_of_digit_after_the_floating_pointax(s=b, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

            if ((s_b[0] == 0) and (s_b[1] == 0)):

                erreur = True

            else:

                res_1 = my_div_1(l_a=s_n_to_liste_number_of_digit_after_the_floating_pointax(s=a, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax), l_b=s_n_to_liste_number_of_digit_after_the_floating_pointax(s=b, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax), number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

                res = liste_number_of_digit_after_the_floating_pointax_to_s_n(l=res_1, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

        elif (o == '^'):

            t = is_numereau(s=b)
            
            #b_ = s_to_numereau(s=b)
            
            b_ = s_n_to_liste_number_of_digit_after_the_floating_pointax(s=b, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)
            
            #print("b_ = ", b_)

            if ((t[0]) and (t[1] == 0) and (b_[3] >= 0)):

                s_b = s_n_to_liste_number_of_digit_after_the_floating_pointax(s=b, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

                s_a = s_n_to_liste_number_of_digit_after_the_floating_pointax(s=a, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

                if ((s_b[0] < 0) and (s_a[0] == 0) and (s_a[1] == 0)):

                    erreur = True

                elif ((s_b[0] == 0) and (s_b[1] == 0) and (s_a[0] == 0) and (s_a[1] == 0)):

                    erreur = True

                else:

                    res_1 = my_puissance_2(l=s_n_to_liste_number_of_digit_after_the_floating_pointax(s=a, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax), n=s_to_numereau(s=b), number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

                    res = liste_number_of_digit_after_the_floating_pointax_to_s_n(l=res_1, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

            elif ((t[0]) and (b_[3] >= 0)):

                i = 0

                while (b[i] != '.'):

                    i += 1

                i += 1

                s = ""

                while (i < len(b)):

                    s += b[i]

                    i += 1

                if (int(s) == 0):

                    s_b = s_n_to_liste_number_of_digit_after_the_floating_pointax(s=b, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

                    s_a = s_n_to_liste_number_of_digit_after_the_floating_pointax(s=a, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

                    if ((s_b[0] < 0) and (s_a[0] == 0) and (s_a[1] == 0)):

                        erreur = True

                    elif ((s_b[0] == 0) and (s_b[1] == 0) and (s_a[0] == 0) and (s_a[1] == 0)):

                        erreur = True

                    else:

                        res_1 = my_puissance_2(l=s_n_to_liste_number_of_digit_after_the_floating_pointax(s=a, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax), n=s_to_numereau(s=b), number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

                        res = liste_number_of_digit_after_the_floating_pointax_to_s_n(l=res_1, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

                else:
                    
                    
                    s = b.split(".")
                    
                    a1 = s[0] + s[1]
                    
                    b1 = my_puissance(a=10, n=len(s[1]))
                    
                    d = pgcd(a=int(a1), b=b1)
                    
                    a2 = my_div(a=int(a1), b=d, number_of_digit_after_the_floating_pointax=1)
                    
                    b2 = my_div(a=b1, b=d, number_of_digit_after_the_floating_pointax=1)
                    
                    #print("a2 = ", a2, " . b2 = ", b2)
                    
                    res_1 = my_puissance_2(l=s_n_to_liste_number_of_digit_after_the_floating_pointax(s=a, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax), n=a2[0], number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

                    res_1 = my_racine_2(l=res_1, n=b2[0], number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

                    res = liste_number_of_digit_after_the_floating_pointax_to_s_n(l=res_1, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)


                    #erreur = True

            else:

                erreur = True

        elif ((o == 'R') or (o == 'r')):

            t = is_numereau(s=b)

            s_b = s_n_to_liste_number_of_digit_after_the_floating_pointax(s=b, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

            s_a = s_n_to_liste_number_of_digit_after_the_floating_pointax(s=a, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

            # if ((h1 < 0) and (mod(a=h, b=2) == 0)):
            #
            #     erreur = True

            if ((t[0]) and (t[1] == 0) and (s_b[0] > 0)):

                if ((s_a[0] < 0) and (mod(a=s_b[0], b=2) == 0)):

                    erreur = True

                else:

                    res_1 = my_racine_2(l=s_n_to_liste_number_of_digit_after_the_floating_pointax(s=a, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax), n=s_to_numereau(s=b), number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

                    res = liste_number_of_digit_after_the_floating_pointax_to_s_n(l=res_1, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

            elif ((t[0]) and (s_b[0] > 0)):

                i = 0

                while (b[i] != '.'):

                    i += 1

                i += 1

                s = ""

                while (i < len(b)):

                    s += b[i]

                    i += 1

                if (int(s) == 0):

                    if ((s_a[0] < 0) and (mod(a=s_b[0], b=2) == 0)):

                        erreur = True

                    else:

                        res_1 = my_racine_2(l=s_n_to_liste_number_of_digit_after_the_floating_pointax(s=a, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax), n=s_to_numereau(s=b), number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

                        res = liste_number_of_digit_after_the_floating_pointax_to_s_n(l=res_1, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

                else:

                    erreur = True

            else:

                erreur = True

        # print("res_1 = ", res_1)

        return [erreur, res]





    def trouv(l, n):

        # trouve la fin de parenthese par devan depuit 'n' dans la liste 'l'

        i = 0

        if ((n > -1) and (n < len(l)) and (l[n] == '(')):

            i = n + 1

            t = 1

            while ((i < len(l)) and (t != 0)):

                if (l[i] == '('):

                    t += 1

                elif (l[i] == ')'):

                    t -= 1

                # print("i = ", i, " . l[i] = ", l[i], " . t = ", t)

                i += 1

            if (t == 0):

                i -= 1

        else:

            i = len(l)


        return i

    def trouv_(l, n):

        # trouve la fin de parenthese par deriere

        i = 0

        if ((n > -1) and (n < len(l)) and (l[n] == ')')):

            i = n - 1

            t = 1

            while ((i > -1) and (t != 0)):

                if (l[i] == ')'):

                    t += 1

                elif (l[i] == '('):

                    t -= 1

                # print("i = ", i, " . l[i] = ", l[i], " . t = ", t)

                i -= 1

            if (t == 0):

                i += 1

        else:

            i = -1

        return i


    def mot(l, n):

        # donne la position des deux extrimité depuit l'operateur à l'indice n

        a = n - 1

        b = n + 1

        if ((n > 0) and (l[n - 1] == ')')):

            a = trouv_(l=l, n=n - 1)

        if ((n + 1 < len(l)) and (l[n + 1] == '(')):

            b = trouv(l=l, n=n + 1)

        return [a, b]


    def parentheser(l, a, b):

        # mais les parentheses dans la liste 'l' dans 'a' et 'b'

        m = []

        erreur = False

        c = 0

        # print("a = ", a, " . b = ", b)

        if (a - 1 > -1):

            c = trouv(l=l, n=a - 1)

        if ((b + 1 < len(l)) and (c == b + 1)):

            m = l

        elif ((a < b) and (b < len(l))):

            i = 0

            while (i < a):

                m.append(l[i])

                i += 1

            m.append("(")

            while (i < b + 1):

                m.append(l[i])

                i += 1

            m.append(")")

            while (i < len(l)):

                m.append(l[i])

                i += 1

        else:

            erreur = True

        return [m, erreur]


    def trouv_c(l, c, n):

        # trouve le caractere c dans la liste l

        i = n

        while ((i < len(l)) and (l[i] != c)):

            i += 1

        return i


    def insert_l(l, s, a, b):

        # insert la chaine s à la position [a, b] de la liste l

        m = []

        i = 0

        while (i < a):

            m.append(l[i])

            i += 1

        m.append(s)

        i = b + 1

        while (i < len(l)):

            m.append(l[i])

            i += 1

        return m


    def avec_signe(s):
        
        # differencie le signe de numero
        
        i = 0
        
        t = 1
        
        while ((i < len(s)) and ((s[i] == '+') or (s[i] == '-'))):
            
            if (s[i] == '-'):
                
                t = -t
                
            i += 1
            
        s_ = ""
        
        while (i < len(s)):
            
            s_ += s[i]
            
            i += 1
            
        t_ = ""
        
        if (t == -1):
            
            t_ = "-"
                
        
            
        return [t_, s_]

    def parentheser_l(l):

        # mais les parentheses dans la liste 'l'

        erreur = False

        if (len(l) > 1):

            i = 0

            while (i < len(l)):

                a = trouv_c(l=l, c='^', n=i)

                b = trouv_c(l=l, c='R', n=i)

                c = my_min(a=a, b=b)

                if (c < len(l)):

                    t = mot(l=l, n=c)

                    h = parentheser(l=l, a=t[0], b=t[1])

                    # print("a = ", a, " . b = ", b, " . c = ", c, " . t = ", t, " . h = ", h, " . l[c] = ", l[c])

                    if (not h[1]):

                        l = h[0]

                    else:

                        erreur = True

                i = c + 2

            i = 0

            while (i < len(l)):

                a = trouv_c(l=l, c='*', n=i)

                b = trouv_c(l=l, c='/', n=i)

                c = my_min(a=a, b=b)

                if (c < len(l)):

                    t = mot(l=l, n=c)

                    h = parentheser(l=l, a=t[0], b=t[1])

                    # print("a = ", a, " . b = ", b, " . c = ", c, " . t = ", t, " . h = ", h, " . l[c] = ", l[c])

                    if (not h[1]):

                        l = h[0]

                    else:

                        erreur = True

                i = c + 2

            i = 0

            while (i < len(l)):

                a = trouv_c(l=l, c='+', n=i)

                b = trouv_c(l=l, c='-', n=i)

                c = my_min(a=a, b=b)

                if (c < len(l)):

                    t = mot(l=l, n=c)

                    h = parentheser(l=l, a=t[0], b=t[1])

                    # print("a = ", a, " . b = ", b, " . c = ", c, " . t = ", t, " . h = ", h, " . l[c] = ", l[c])

                    if (not h[1]):

                        l = h[0]

                    else:

                        erreur = True

                i = c + 2

        elif (len(l) == 1):

            #l = [s_to_numereau(s=l[0])]

            if (is_numereau(s=l[0])[0]):

                a = avec_signe(s=l[0])
                
                s = a[0] + a[1]
                
                l = ["(", s, ")"]
                
            else:
                
                erreur = True

        return [erreur, l]

    def liste_to_s(l):
        
        #trensforme une liste 'l' à une chaine 's'
        
        i = 0
        
        s = ""
        
        while (i < len(l)):
            
            s += l[i]
            
            i += 1
            
        return s


    def check_parenthese_l(l):

        # check les parenthese de la liste 'l'

        h = liste_to_s(l=l)

        u = check_parentheses(s=h)

        # print("h = ", h, " . u = ", u)

        return u


    def calculatrice(s, l_, n):

        # calcule le resultat de s

        erreur = False

        d = []

        if (n == 0):

            s = supprime_espace(s=s)

            u = check_parentheses(s=s)

            # print("calc . u = ", u)

            m = s_to_liste(s=s)

            if (not m[0]):

                t = check_erreur(l=m[1])

                if (not t[0]):

                    l = t[1]

                    f = parentheser_l(l=l)

                    if (not f[0]):

                        d = f[1]

                        t = trouv_c(l=d, c=')', n=0)

                        while ((t < len(d)) and (not erreur)):

                            t_ = trouv_(l=d, n=t)

                            k = 0

                            if (t_ == t - 4):

                                r = calcule(a=d[t - 3], o=d[t - 2], b=d[t - 1])

                                if (not r[0]):

                                    k = r[1]

                                    # print("1 . d = ", d)

                                else:

                                    erreur = True

                            else:

                                if (is_numereau(s=d[t - 1][0])):

                                    k = s_to_numereau(s=d[t - 1])

                                else:

                                    erreur = True

                            d = insert_l(l=d, s=str(k), a=t_, b=t)

                            p = check_erreur(l=d)

                            d = p[1]

                            # print("2 . d = ", d)

                            t = trouv_c(l=d, c=')', n=0)

                    else:

                        erreur = True

                else:

                    erreur = True

            else:

                erreur = True

        elif (n == 1):

            u = check_parenthese_l(l=l_)

            # print("calc . u = ", u)

            if (u):

                t = check_erreur(l=l_)

                # print("calc . t = ", t)

                if (not t[0]):

                    l = t[1]

                    f = parentheser_l(l=l)

                    # print("calculatrice . f = ", f)

                    if (not f[0]):

                        d = f[1]

                        t = trouv_c(l=d, c=')', n=0)

                        while ((t < len(d)) and (not erreur)):

                            t_ = trouv_(l=d, n=t)

                            k = 0

                            if (t_ == t - 4):

                                r = calcule(a=d[t - 3], o=d[t - 2], b=d[t - 1])

                                if (not r[0]):

                                    k = r[1]

                                    # print("calculatrice . d = ", d)

                                else:

                                    erreur = True

                            else:

                                if (is_numereau(s=d[t - 1])[0]):

                                    # print("d[t - 1] = ", d[t - 1])

                                    k = s_to_numereau(s=d[t - 1])

                                else:

                                    erreur = True

                            d = insert_l(l=d, s=str(k), a=t_, b=t)

                            p = check_erreur(l=d)

                            d = p[1]

                            # print("calc  2 . d = ", d)

                            t = trouv_c(l=d, c=')', n=0)

                    else:

                        erreur = True

                else:

                    erreur = True

            else:

                erreur = True

        return [erreur, d]


    def calculatrice_1(s, l_, n, number_of_digit_after_the_floating_pointax, e):

        # calcule le resultat de s

        erreur = False

        d = []

        if (n == 0):

            s = supprime_espace(s=s)

            u = check_parentheses(s=s)

            if (e):

                print("calc . u = ", u)

            if (u):

                m = s_to_liste(s=s)

                if (e):

                    print("m = ", m)

                if (not m[0]):

                    t = check_erreur(l=m[1])

                    if (e):
                    
                        print("calcu . len(t[1]) = ", len(t[1]), " . t = ", t)

                    if (not t[0]):

                        l = t[1]

                        f = parentheser_l(l=l)

                        if (e):
                        
                            print("calcul . f = ", f)

                        if (not f[0]):

                            d = f[1]

                            t = trouv_c(l=d, c=')', n=0)

                            while ((t < len(d)) and (not erreur)):

                                t_ = trouv_(l=d, n=t)

                                k = 0

                                if (t_ == t - 4):

                                    r = calcule_1(a=d[t - 3], o=d[t - 2], b=d[t - 1], number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

                                    if (not r[0]):

                                        k = r[1]

                                        # print("1 . d = ", d)

                                    else:

                                        erreur = True

                                elif (t_ == t - 2):

                                    if (is_numereau(s=d[t - 1][0])):

                                        k = d[t - 1]

                                    else:

                                        erreur = True

                                else:
                                    
                                    erreur = True

                                if (not erreur):

                                    d = insert_l(l=d, s=k, a=t_, b=t)

                                    p = check_erreur(l=d)

                                    if (not erreur):

                                        erreur = p[0]

                                    d = p[1]

                                    if (e):
                                    
                                        print("calcul . d = ", d)

                                    t = trouv_c(l=d, c=')', n=0)

                        else:

                            erreur = True

                    else:

                        erreur = True

                else:

                    erreur = True

            else:
                
                erreur = True

        elif (n == 1):

            u = check_parenthese_l(l=l_)

            if (e):

                print("calc . u = ", u)

            if (u):

                t = check_erreur(l=l_)

                if (e):
                
                    print("calc . t = ", t)

                if (not t[0]):

                    l = t[1]

                    f = parentheser_l(l=l)

                    if (e):
                    
                        print("calculatrice . f = ", f)

                    if (not f[0]):

                        d = f[1]

                        t = trouv_c(l=d, c=')', n=0)

                        while ((t < len(d)) and (not erreur)):

                            t_ = trouv_(l=d, n=t)

                            k = 0

                            if (t_ == t - 4):

                                r = calcule_1(a=d[t - 3], o=d[t - 2], b=d[t - 1], number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

                                if (not r[0]):

                                    k = r[1]

                                    # print("calculatrice . d = ", d)

                                else:

                                    erreur = True

                            elif (t_ == t - 2):

                                if (is_numereau(s=d[t - 1])[0]):

                                    # print("d[t - 1] = ", d[t - 1])

                                    k = d[t - 1]

                                else:

                                    erreur = True

                            else:
                                
                                erreur = True
                            
                            if (not erreur):
                            
                            
                                d = insert_l(l=d, s=k, a=t_, b=t)

                                p = check_erreur(l=d)

                                if (not erreur):
            
                                    erreur = p[0]

                                d = p[1]

                                if (e):
                                
                                    print("calc  2 . d = ", d)

                                t = trouv_c(l=d, c=')', n=0)

                    else:

                        erreur = True

                else:

                    erreur = True

            else:

                erreur = True

        # if (len(d) == 1):
            
        #     d[0] = str(d[0])

        return [erreur, d]



    def calculatrice_2(s, l_, n, number_of_digit_after_the_floating_pointax, e):

        # calcule le resultat de s

        erreur = False

        d = []

        if (n == 0):

            s = supprime_espace(s=s)

            u = check_parentheses(s=s)

            if (e):

                print("calc . u = ", u)

            if (u):

                m = s_to_liste(s=s)

                if (e):

                    print("m = ", m)

                if (not m[0]):

                    t = check_erreur(l=m[1])

                    if (e):
                    
                        print("calcu . len(t[1]) = ", len(t[1]), " . t = ", t)

                    if (not t[0]):

                        l = t[1]

                        f = parentheser_l(l=l)

                        if (e):
                        
                            print("calcul . f = ", f)

                        if (not f[0]):

                            d = f[1]

                            t = trouv_c(l=d, c=')', n=0)

                            while ((t < len(d)) and (not erreur)):

                                t_ = trouv_(l=d, n=t)

                                k = 0

                                if (t_ == t - 4):

                                    r = calcule_2(a=d[t - 3], o=d[t - 2], b=d[t - 1], number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

                                    if (not r[0]):

                                        k = r[1]

                                        # print("1 . d = ", d)

                                    else:

                                        erreur = True

                                elif (t_ == t - 2):

                                    if (is_numereau(s=d[t - 1][0])):

                                        k = d[t - 1]

                                    else:

                                        erreur = True

                                else:
                                    
                                    erreur = True

                                if (not erreur):

                                    d = insert_l(l=d, s=k, a=t_, b=t)

                                    p = check_erreur(l=d)

                                    if (not erreur):

                                        erreur = p[0]

                                    d = p[1]

                                    if (e):
                                    
                                        print("calcul . d = ", d)

                                    t = trouv_c(l=d, c=')', n=0)

                        else:

                            erreur = True

                    else:

                        erreur = True

                else:

                    erreur = True

            else:
                
                erreur = True

        elif (n == 1):

            u = check_parenthese_l(l=l_)

            if (e):

                print("calc . u = ", u)

            if (u):

                t = check_erreur(l=l_)

                if (e):
                
                    print("calc . t = ", t)

                if (not t[0]):

                    l = t[1]

                    f = parentheser_l(l=l)

                    if (e):
                    
                        print("calculatrice . f = ", f)

                    if (not f[0]):

                        d = f[1]

                        t = trouv_c(l=d, c=')', n=0)

                        while ((t < len(d)) and (not erreur)):

                            t_ = trouv_(l=d, n=t)

                            k = 0

                            if (t_ == t - 4):

                                r = calcule_2(a=d[t - 3], o=d[t - 2], b=d[t - 1], number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_pointax)

                                if (not r[0]):

                                    k = r[1]

                                    # print("calculatrice . d = ", d)

                                else:

                                    erreur = True

                            elif (t_ == t - 2):

                                if (is_numereau(s=d[t - 1])[0]):

                                    # print("d[t - 1] = ", d[t - 1])

                                    k = d[t - 1]

                                else:

                                    erreur = True

                            else:
                                
                                erreur = True
                            
                            if (not erreur):
                            
                            
                                d = insert_l(l=d, s=k, a=t_, b=t)

                                p = check_erreur(l=d)

                                if (not erreur):
            
                                    erreur = p[0]

                                d = p[1]

                                if (e):
                                
                                    print("calc  2 . d = ", d)

                                t = trouv_c(l=d, c=')', n=0)

                    else:

                        erreur = True

                else:

                    erreur = True

            else:

                erreur = True

        # if (len(d) == 1):
            
        #     d[0] = str(d[0])

        return [erreur, d]






















    if __name__ == "__main__":




        oper = "10 ^ 2.5"
        
        number_of_digit_after_the_floating_point = 5
        
        t1 = time.time()

        m = calculatrice_2(s=oper, l_=[], n=0, number_of_digit_after_the_floating_pointax=number_of_digit_after_the_floating_point, e=False)
        
        t2 = time.time()
        
        print("oper = '", oper, "' . m = ", m, " . number_of_digit_after_the_floating_pointax = ", number_of_digit_after_the_floating_point, " . time = ", t2 - t1, " . len = ", len(m[1][0]))




























                

                

                
                

                

                
                

                """






                i_self.i["i_Economic_Partner_official_receiver_0"] = r"""



















global i

i = {}


i["pricipal-central"] = "i am here"


i["i am you"] = True


if (i["i am you"] == True):


    # i_Economic_Partner_official_receiver_0.py




    import os

    import socket

    import time

    import traceback

    from pathlib import Path





    i["i_cwd"] = os.getcwd() + "/"





    def i_number_to_str(i_number):


        global i

        i["i_string_of_i_number_to_str_0"] = str(i_number)

        i["i_counter_of_i_number_to_str_4"] = len(i["i_string_of_i_number_to_str_0"]) - 1

        i["i_counter_of_i_number_to_str_5"] = 0

        i["i_string_of_i_number_to_str_1"] = ""

        while (i["i_counter_of_i_number_to_str_4"] >= 0):

            if (i["i_counter_of_i_number_to_str_5"] == 3):

                i["i_string_of_i_number_to_str_1"] = "_" + i["i_string_of_i_number_to_str_1"]

                i["i_counter_of_i_number_to_str_5"] = 0

            i["i_string_of_i_number_to_str_1"] = i["i_string_of_i_number_to_str_0"][i["i_counter_of_i_number_to_str_4"]] + i["i_string_of_i_number_to_str_1"]


            i["i_counter_of_i_number_to_str_4"] -= 1

            i["i_counter_of_i_number_to_str_5"] += 1


        return i["i_string_of_i_number_to_str_1"]





    def i_get_ip_of_wifi():


        i_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:

            i_s.connect(("8.8.8.8", 80))

            i_ip = i_s.getsockname()[0]

        except Exception:

            i_ip = "NULL"

        finally:

            i_s.close()

        return i_ip




    i["i_ip_of_wifi_of_receiver"] = i_get_ip_of_wifi()

    print("i . i_ip_of_wifi_of_receiver = ", i["i_ip_of_wifi_of_receiver"])


    i["i_semaphore"] = False



    try:


        try:

            i["i_folder_for_receive"] = i["i_cwd"] + "i_folder_for_receive/"

            os.mkdir(i["i_folder_for_receive"])


        except Exception as i_e:


            i["i_semaphore_1"] = True




        try:

            i["i_folder_of_history"] = i["i_cwd"] + "i_folder_for_receive/i_folder_of_history/"

            os.mkdir(i["i_folder_of_history"])


        except Exception as i_e:


            i["i_semaphore_1"] = True



        try:


            i["i_folder_for_send"] = i["i_cwd"] + "i_folder_for_send/"

            os.mkdir(i["i_folder_for_send"])


        except Exception as i_e:


            i["i_semaphore_1"] = True







        i["server_socket"] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        i["server_socket"].bind((i["i_ip_of_wifi_of_receiver"], 12345))
        
        i["server_socket"].listen(1)
        

        print("i . start receiver with success .")



        i["client_socket"], i["client_address"] = i["server_socket"].accept()

        print("i . connect with sender ", i["client_address"]," success .")


        i["i_t1"] = time.time()
        










        i["i_number_of_file-s_byte-s"] = i["client_socket"].recv(8)

        i["i_number_of_file-s"] = int.from_bytes(i["i_number_of_file-s_byte-s"], 'big')




        if (i["i_number_of_file-s"] > 0):

            i["i_file-s"] = []


            i["i_counter"] = 0


            while (i["i_counter"] < i["i_number_of_file-s"]):



                i["i_length_of_name_file_in_byte-s"] = i["client_socket"].recv(8)

                i["i_length_of_name_file"] = int.from_bytes(i["i_length_of_name_file_in_byte-s"], 'big')



                i["i_name_of_file"] = ""

                while len(i["i_name_of_file"]) < i["i_length_of_name_file"]:

                    i["chunk"] = i["client_socket"].recv(1).decode('utf-8')
                    
                    if not i["chunk"]:

                        break

                    i["i_name_of_file"] += i["chunk"]

                    

                i["i_file-s"].append(i["i_name_of_file"])



                i["i_size_of_file_in_byte-s"] = i["client_socket"].recv(8)

                i["i_size_of_file"] = int.from_bytes(i["i_size_of_file_in_byte-s"], 'big')

                print("i . i['i_size_of_file'] = ", i["i_size_of_file"], " . i['i_counter'] = ", i["i_counter"])


                i["i_received_data"] = b''

                while len(i["i_received_data"]) < i["i_size_of_file"]:



                    if (len(i["i_received_data"]) < i["i_size_of_file"] - 10_000_000):

                        i["chunk"] = i["client_socket"].recv(10_000_000)


                    elif (len(i["i_received_data"]) < i["i_size_of_file"] - 1_000_000):

                        i["chunk"] = i["client_socket"].recv(1_000_000)


                    elif (len(i["i_received_data"]) < i["i_size_of_file"] - 100_000):

                        i["chunk"] = i["client_socket"].recv(100_000)


                    elif (len(i["i_received_data"]) < i["i_size_of_file"] - 10_000):

                        i["chunk"] = i["client_socket"].recv(10_000)


                    elif (len(i["i_received_data"]) < i["i_size_of_file"] - 1_000):

                        i["chunk"] = i["client_socket"].recv(1_000)


                    elif (len(i["i_received_data"]) < i["i_size_of_file"] - 100):

                        i["chunk"] = i["client_socket"].recv(100)


                    elif (len(i["i_received_data"]) < i["i_size_of_file"] - 10):

                        i["chunk"] = i["client_socket"].recv(10)

                    else:

                        i["chunk"] = i["client_socket"].recv(1)
                    
                    if not i["chunk"]:

                        break

                    i["i_received_data"] += i["chunk"]


                i["i_file"] = i["i_folder_for_receive"] + i["i_name_of_file"]

                i["i_d"] = Path(i["i_file"])

                i["i_d"].write_bytes(i["i_received_data"])


                i["i_counter"] += 1



            try:

                i["i_calcul"] = {}


                i["i_counter"] = 0


                while (i["i_counter"] < len(i["i_file-s"])):


                    i["i_quantity"] = 0

                    i["i_v_1"] = (i["i_file-s"][i["i_counter"]]).split("quantity_")


                    i["i_v_1"] = i["i_v_1"][1].split("_")

                    try:

                        i["i_quantity"] = int(i["i_v_1"][0])

                    except:

                        i["i_semaphore"] = True


                    i["i_v_1"] = (i["i_file-s"][i["i_counter"]]).split("unity_")

                    i["i_v_1"] = i["i_v_1"][1].split("_")

                    i["i_unity"] = i["i_v_1"][0]





                    if (i["i_unity"] in i["i_calcul"]):

                        i["i_calcul"][i["i_unity"]] += i["i_quantity"]

                    else:

                        i["i_calcul"][i["i_unity"]] = i["i_quantity"]

                    i["i_counter"] += 1

                i["i_string_of_i_calcul"] = ""

                i["i_string_of_i_calcul"] += time.strftime("\n\n{' %Y/%m/%d %H:%M:%S ' : \n\n    ")

                print("i . ", time.strftime("' %Y/%m/%d %H:%M:%S '"), " . i['i_calcul'] ==  {")
                
                for i["i_unity"] in i["i_calcul"]:


                    i["i_string_of_i_calcul"] += "     '" + i["i_unity"] + "' : " + i_number_to_str(i["i_calcul"][i["i_unity"]]) + " ,"
                    
                    print("     '", i["i_unity"], "' : ", i_number_to_str(i["i_calcul"][i["i_unity"]]), " ,")


                i["i_string_of_i_calcul"] += "    \n\n}\n\n,\n\n"
                
                print("    }")




                try:

                    i["i_file_of_history_of_receive"] = i["i_cwd"] + "i_file_of_history_of_receive.txt"

                    i["i_d"] = Path(i["i_file_of_history_of_receive"])

                    i["i_content"] = i["i_d"].read_text()

                    i["i_content"] = i["i_string_of_i_calcul"] + i["i_content"]
                    
                    i["i_d"].write_text(i["i_content"])

                except:

                    i["i_semaphore_2"] = True

                    i["i_file_of_history_of_receive"] = i["i_cwd"] + "i_file_of_history_of_receive.txt"

                    i["i_d"] = Path(i["i_file_of_history_of_receive"])

                    i["i_content"] = i["i_string_of_i_calcul"]
                    
                    i["i_d"].write_text(i["i_content"])


            except:


                i["i_semaphore_3"] = True



        i["i_t2"] = time.time()


        print("i . file-s receive-ed with success . i_time = ", i["i_t2"] - i["i_t1"])



        i["client_socket"].close()

        i["server_socket"].close()

        print("i . the operation is finish-ed with success .")


    except Exception as i_e:


        i["i_semaphore"] = True

        print("i . i_e = ", i_e)

        traceback.print_exc()

        i_e_ = str(traceback.format_exc())

        print("i . i_e_ = ", i_e_)



    print("i['i_semaphore'] = ", i["i_semaphore"])



    print("finish .")











                
                

                """




                i_self.i["i_Economic_Partner_official_sender_0"] = r"""























global i

i = {}



i["pricipal-central"] = "i am here"


i["i am you"] = True


if (i["i am you"] == True):


    # i_Economic_Partner_official_sender_0.py


    import os

    import socket

    import traceback

    from pathlib import Path

    import time





    # the place of modify

    # ------------------------------------------------------------------------
    # ------------------------------------------------------------------------

    i["i_ip_of_wifi_of_receiver"] = ""

    # ------------------------------------------------------------------------
    # ------------------------------------------------------------------------




    i["i_cwd"] = os.getcwd() + "/"

    i["i_semaphore"] = False




    try:



        try:

            i["i_folder_for_receive"] = i["i_cwd"] + "i_folder_for_receive/"

            os.mkdir(i["i_folder_for_receive"])


        except Exception as i_e:


            i["i_semaphore_1"] = True




        try:

            i["i_folder_of_history"] = i["i_cwd"] + "i_folder_for_receive/i_folder_of_history/"

            os.mkdir(i["i_folder_of_history"])


        except Exception as i_e:


            i["i_semaphore_1"] = True



        try:


            i["i_folder_for_send"] = i["i_cwd"] + "i_folder_for_send/"

            os.mkdir(i["i_folder_for_send"])


        except Exception as i_e:


            i["i_semaphore_1"] = True








        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client_socket.connect((i["i_ip_of_wifi_of_receiver"], 12345))


        print("i . connect to receiver with success .")

        i["i_t1"] = time.time()

        i["i_file-s"] = []


        for root, dirs, i["i_file-s"] in os.walk(i["i_folder_for_send"]):

            break



        client_socket.sendall(len(i["i_file-s"]).to_bytes(8, 'big'))



        i["i_counter"] = 0

        while (i["i_counter"] < len(i["i_file-s"])):

                

            i["i_path_of_file"] = i["i_cwd"] + i["i_file-s"][i["i_counter"]]

            i["i_name_of_file"] = i["i_file-s"][i["i_counter"]]

            print("i . len(i['i_name_of_file']) = ", len(i["i_name_of_file"]), " . i['i_counter'] = ", i["i_counter"])




            client_socket.sendall(len(i["i_name_of_file"].encode('utf-8')).to_bytes(8, 'big'))


            client_socket.send(i["i_name_of_file"].encode('utf-8'))



            i["i_d"] = Path(i["i_folder_for_send"] + i["i_name_of_file"])


            i["i_d_bytes"] = i["i_d"].read_bytes()



            client_socket.sendall(len(i["i_d_bytes"]).to_bytes(8, 'big'))


            client_socket.sendall(i["i_d_bytes"])


            os.remove(i["i_folder_for_send"] + i["i_file-s"][i["i_counter"]])


            i["i_counter"] += 1




        try:

            i["i_calcul"] = {}


            i["i_counter"] = 0


            while (i["i_counter"] < len(i["i_file-s"])):


                i["i_quantity"] = 0

                i["i_v_1"] = (i["i_file-s"][i["i_counter"]]).split("quantity_")


                i["i_v_1"] = i["i_v_1"][1].split("_")

                try:

                    i["i_quantity"] = int(i["i_v_1"][0])

                except:

                    i["i_semaphore"] = True


                i["i_v_1"] = (i["i_file-s"][i["i_counter"]]).split("unity_")

                i["i_v_1"] = i["i_v_1"][1].split("_")

                i["i_unity"] = i["i_v_1"][0]





                if (i["i_unity"] in i["i_calcul"]):

                    i["i_calcul"][i["i_unity"]] += i["i_quantity"]

                else:

                    i["i_calcul"][i["i_unity"]] = i["i_quantity"]

                i["i_counter"] += 1

            i["i_string_of_i_calcul"] = ""

            i["i_string_of_i_calcul"] += time.strftime("\n\n{' %Y/%m/%d %H:%M:%S ' : \n\n    ")

            print("i . ", time.strftime("' %Y/%m/%d %H:%M:%S '"), " . i['i_calcul'] ==  {")
            
            for i["i_unity"] in i["i_calcul"]:


                i["i_string_of_i_calcul"] += "     '" + i["i_unity"] + "' : " + i_number_to_str(i["i_calcul"][i["i_unity"]]) + " ,"
                
                print("     '", i["i_unity"], "' : ", i_number_to_str(i["i_calcul"][i["i_unity"]]), " ,")


            i["i_string_of_i_calcul"] += "    \n\n}\n\n,\n\n"
            
            print("    }")




            try:

                i["i_file_of_history_of_receive"] = i["i_cwd"] + "i_file_of_history_of_receive.txt"

                i["i_d"] = Path(i["i_file_of_history_of_receive"])

                i["i_content"] = i["i_d"].read_text()

                i["i_content"] = i["i_string_of_i_calcul"] + i["i_content"]
                
                i["i_d"].write_text(i["i_content"])

            except:

                i["i_semaphore_2"] = True

                i["i_file_of_history_of_receive"] = i["i_cwd"] + "i_file_of_history_of_receive.txt"

                i["i_d"] = Path(i["i_file_of_history_of_receive"])

                i["i_content"] = i["i_string_of_i_calcul"]
                
                i["i_d"].write_text(i["i_content"])


        except:


            i["i_semaphore_3"] = True




        i["i_t2"] = time.time()


        print("i . send-ed to receiver success . i_time = ", i["i_t2"] - i["i_t1"])

        print("i . the operation is finish-ed with success .")

        client_socket.shutdown(socket.SHUT_WR)

        client_socket.close()


        print("i . close success .")

    
    except Exception as i_e:


        i["i_semaphore"] = True

        print("i . i_e = ", i_e)


        traceback.print_exc()

        i_e_ = str(traceback.format_exc())


        print("i . i_e_ = ", i_e_)




    print("i . i['i_semaphore'] = ", i["i_semaphore"])


    print("finish .")














                
                

                      
                

                """





                i_self.i["i_cwd"] = os.getcwd() + "/"




                i_self.i["i_file"] = i_self.i["i_cwd"] + "i_Economic_Partner_official_receiver_0.py"

                i_self.i["i_d"] = Path(i_self.i["i_file"])

                i_self.i["i_d"].write_text(i_self.i["i_Economic_Partner_official_receiver_0"])




                i_self.i["i_file"] = i_self.i["i_cwd"] + "i_Economic_Partner_official_sender_0.py"

                i_self.i["i_d"] = Path(i_self.i["i_file"])

                i_self.i["i_d"].write_text(i_self.i["i_Economic_Partner_official_sender_0"])

                




                i_self.i["i_file"] = i_self.i["i_cwd"] + "i_math_0.py"

                i_self.i["i_d"] = Path(i_self.i["i_file"])

                i_self.i["i_d"].write_text(i_self.i["i_math"])







                i_self.i["print_personal_account_with_UTF8_Economic_Partner_official_photo_money_quantity_200_unity_USD_part_10186"] = b'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09a416D84pDRapIjrtpRVAYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD8IuC0AAAgAElEQVQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA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AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAwC8/AFmIw5EAlsBmAAAAAElFTkSuQmCC'



                i_self.i["i_file"] = i_self.i["i_cwd"] + "print_personal_account_with_UTF8_Economic_Partner_official_photo_money_quantity_200_unity_USD_part_10186.png"

                i_self.i["i_d"] = Path(i_self.i["i_file"])

                i_self.i["i_d"].write_bytes(i_self.i["print_personal_account_with_UTF8_Economic_Partner_official_photo_money_quantity_200_unity_USD_part_10186"])








                i_self.i["print_personal_account_with_UTF8_Economic_Partner_official_photo_money_quantity_2000_unity_DZD_part_10176"] = b'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AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPzKDfLPTS+ORu7cAAAAAElFTkSuQmCC'




                i_self.i["i_file"] = i_self.i["i_cwd"] + "print_personal_account_with_UTF8_Economic_Partner_official_photo_money_quantity_2000_unity_DZD_part_10176.png"

                i_self.i["i_d"] = Path(i_self.i["i_file"])

                i_self.i["i_d"].write_bytes(i_self.i["print_personal_account_with_UTF8_Economic_Partner_official_photo_money_quantity_2000_unity_DZD_part_10176"])





