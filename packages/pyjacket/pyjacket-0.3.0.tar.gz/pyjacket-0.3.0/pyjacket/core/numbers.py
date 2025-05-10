from math import floor, log10

"""Methods that apply to floats and ints"""

def sign(num):
    return (-1, 1)[num >= 0]

def order10(num):
    """Order of a magnitude belong to a number (base 10)"""
    return int(floor(log10(abs(num))))

def truncate(num, n):
    """Remove any floating points"""
    return int(num * 10**n) / 10**n

def truncate(num, n):
    number = str(float(num))
    return float(number[:number.index('.') + n + 1])



def round_significant(num, significance):
    """Round the number to nearest significant digits"""
    return round(num, significance - order10(num) - 1)

def truncate_significant(num, significance, count_zero=False):
    """Round the number down to desired significant digits"""
    _type = type(num)
    num = str(float(num))
    
    digits = list(num)
    for i, ch in enumerate(num): 
        if ch != '0':
            if ch.isdigit():  count_zero = True
            if significance <= 0 and ch.isdigit():  digits[i] = '0'
        if count_zero and ch.isdigit():
            significance -= 1
            
    return _type(float(''.join(digits)))
    
    


if __name__ == '__main__':
    
    def test():
        assert sign(-1) == -1    
        assert sign(-10) == -1
        assert sign(-1e99) == -1
        assert sign(0) == 1
        assert sign(0.000001) == 1
        assert sign(-1e-10) == -1
        assert sign(1e10) == 1
            
        assert order10(100) == 2
        assert order10(999) == 2
        assert order10(3) == 0
        assert order10(0.2) == -1
        assert order10(-10) == 1
                
        assert truncate(123.1433, 2) == 123.14    
        assert truncate(0.1433, 2) == 0.14    
        assert truncate(-0.5464933, 4) == -0.5464
            
        assert round_significant(123457, 3) == 123000
        assert round_significant(-123457, 4) == -123500
        assert round_significant(1.561, 1) == 2
        assert round_significant(1.561, 2) == 1.6
        assert round_significant(0.999999, 4) == 1
        assert round_significant(0.2413551, 3) == 0.241
        
        assert truncate_significant(123457, 3) == 123000
        assert truncate_significant(-123457, 4) == -123400
        assert truncate_significant(1.561, 1) == 1
        assert truncate_significant(1.561, 2) == 1.5
        assert truncate_significant(0.999999, 4) == 0.9999
        assert truncate_significant(0.2413551, 3) == 0.241
        assert truncate_significant(0.009, 3) == 0.009
        assert truncate_significant(5.809, 3) == 5.80
        assert truncate_significant(0.0409, 2) == 0.040
        assert truncate_significant(0.04099, 3) == 0.0409
    
    test()
    print('Passed all tests :)')