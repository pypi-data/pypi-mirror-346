def rev(s: str):
    """Reverse a string"""
    return s[::-1]

def complement(s: str):
    """Complement of DNA sequence, leaving unexpected characters untouched"""
    return s.translate(str.maketrans('ATCGatcg', 'TAGCtagc'))

def revcom(s: str):
    """Reverse complement of DNA sequence (case insensitive)"""
    return rev(complement(s))