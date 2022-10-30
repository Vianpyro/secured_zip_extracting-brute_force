from functools import wraps
from time import perf_counter
from zipfile import ZipFile
import string

def print_timing(func):
    @wraps(func) 
    def wrapper(*arg):
        timestamp = perf_counter()
        result = func(*arg)
        print(f'{func.__name__} took {perf_counter() - timestamp:.2f} seconds')
        return result
    return wrapper

@print_timing
def crack_zip(file_name: str) -> str:
    with ZipFile(f'{file_name}.zip') as zf:
        for i in Cracker(uppercase=True, digits=True):
            try:
                print(i)
                zf.extractall(pwd=i.encode())
                print(f'Successfuly cracked password: "{i}"')
                break
            except RuntimeError:
                pass


class Cracker:
    def __init__(self, start_from: str=None, lowercase: bool=True, uppercase: bool=False, digits: bool=False, punctuation=False, additional_characters: str|list=None, max_lenght: int=None) -> None:
        self.password_max_lenght = 100 if max_lenght is None else max_lenght + 1
        self.password_chars = str()
        self.password = str() if start_from is None else start_from

        if lowercase: self.password_chars += string.ascii_lowercase
        if uppercase: self.password_chars += string.ascii_uppercase
        if digits: self.password_chars += string.digits
        if punctuation: self.password_chars += string.punctuation

        if isinstance(additional_characters, str):
            self.password_chars += additional_characters
        elif isinstance(additional_characters, list):
            for c in additional_characters:
                self.password_chars += c

        if self.password_chars == str():
            raise ValueError('')

    def next_password(self, password_string: str) -> str:
        if not isinstance(password_string, str):
            raise ValueError

        if password_string == '':
            return self.password_chars[0]

        if password_string[-1] == self.password_chars[-1]:
            if len(password_string) >= 2:
                return self.next_password(password_string[:-1]) + self.password_chars[0]
            return self.password_chars[0] * 2

        return password_string[:-1] + self.password_chars[self.password_chars.index(password_string[-1]) + 1]            
        
    def __iter__(self):
        return self

    def __next__(self) -> str:
        self.password = self.next_password(self.password)

        if len(self.password) >= self.password_max_lenght:
            raise StopIteration(f'Trying to crack passwords over {self.password_max_lenght} would take too much time.')

        return self.password


crack_zip('')
input('Press "enter" to close this window...')
