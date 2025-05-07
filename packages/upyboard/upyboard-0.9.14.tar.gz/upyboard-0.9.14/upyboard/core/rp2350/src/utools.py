import usys
import utime
import uos
import gc
import uselect
import machine

from micropython import const


def _read_rp2350a_vsys(): 
    wl_cs = machine.Pin(25)          
    wl_cs.init(mode=machine.Pin.OUT, value=1)  # wireless SPI CS - when high also enables GPIO29 ADC pin to read VSYS
    vsys = machine.ADC(29).read_u16() * 3.3 / 65535 * 3
    wl_cs.init(mode=machine.Pin.ALT, pull=machine.Pin.PULL_DOWN, alt=1)  # restore 
    return vsys

def get_sys_info() -> tuple:
    """
    Get the CPU temperature of the AutoCON.
    
    :return: tuple of (frequency, voltage, temperature)
    """
    
    freq = machine.freq()
        
    try: # rp2350b (plus2w)
        machine.Pin(43, machine.Pin.IN)
        vsys = machine.ADC(3).read_u16() * (3.3 / 65535) * 3
        TEMP_ADC  = 8
    except ValueError: # rp2350a (pico2w)
        vsys = _read_rp2350a_vsys()
        TEMP_ADC  = 4
                         
    raw = machine.ADC(TEMP_ADC).read_u16()
    temp = 27 - ((raw * 3.3 / 65535) - 0.706) / 0.001721
    
    return freq, vsys, temp

def get_mem_info() -> tuple:
    """
    Get memory usage information.
    
    :return: tuple of (free, used, total) memory in bytes
    """
    
    gc.collect()
    
    free = gc.mem_free()
    used = gc.mem_alloc()
    total = free + used
    
    return free, used, total

def get_fs_info(path='/') -> tuple:
    """
    Get filesystem information for the given path.
    
    :param path: Path to check filesystem info for.
    :return: tuple of (total, used, free, usage percentage)
    """
    
    stats = uos.statvfs(path)
    block_size = stats[0]
    total_blocks = stats[2]
    free_blocks = stats[3]

    total = block_size * total_blocks
    free = block_size * free_blocks
    used = total - free
    usage_pct = round(used / total * 100, 2)

    return total, used, free, usage_pct
    
    
class ANSIEC:
    """
    ANSI Escape Codes for terminal text formatting.
    This class provides methods for setting foreground and background colors, as well as text attributes.
    It uses ANSI escape codes to format text in the terminal.
    """
    
    class FG:
        """
        ANSI escape codes for foreground colors.
        This class provides methods for setting foreground colors using ANSI escape codes.
        It includes standard colors, bright colors, and RGB color support.
        """
        
        BLACK = "\u001b[30m"
        RED = "\u001b[31m"
        GREEN = "\u001b[32m"
        YELLOW = "\u001b[33m"
        BLUE = "\u001b[34m"
        MAGENTA = "\u001b[35m"
        CYAN = "\u001b[36m"
        WHITE = "\u001b[37m"
        BRIGHT_BLACK= "\u001b[30;1m"
        BRIGHT_RED = "\u001b[31;1m"
        BRIGHT_GREEN = "\u001b[32;1m"
        BRIGHT_YELLOW = "\u001b[33;1m"
        BRIGHT_BLUE = "\u001b[34;1m"
        BRIGHT_MAGENTA = "\u001b[35;1m"
        BRIGHT_CYAN = "\u001b[36;1m"
        BRIGHT_WHITE = "\u001b[37;1m"
                
        @classmethod
        def rgb(cls, r:int, g:int, b:int) -> str:
            """
            Returns an ANSI escape code for RGB foreground color.
            :param r: Red component (0-255).
            :param g: Green component (0-255).
            :param b: Blue component (0-255).
            :return: An ANSI escape code for RGB foreground color.
            """
             
            return "\u001b[38;2;{};{};{}m".format(r, g, b)

    class BG:
        """
        ANSI escape codes for background colors.
        This class provides methods for setting background colors using ANSI escape codes.
        It includes standard colors, bright colors, and RGB color support.
        """
        
        BLACK = "\u001b[40m"
        RED = "\u001b[41m"
        GREEN = "\u001b[42m"
        YELLOW = "\u001b[43m"
        BLUE = "\u001b[44m"
        MAGENTA = "\u001b[45m"
        CYAN = "\u001b[46m"
        WHITE = "\u001b[47m"
        BRIGHT_BLACK= "\u001b[40;1m"
        BRIGHT_RED = "\u001b[41;1m"
        BRIGHT_GREEN = "\u001b[42;1m"
        BRIGHT_YELLOW = "\u001b[43;1m"
        BRIGHT_BLUE = "\u001b[44;1m"
        BRIGHT_MAGENTA = "\u001b[45;1m"
        BRIGHT_CYAN = "\u001b[46;1m"
        BRIGHT_WHITE = "\u001b[47;1m"
                
        @classmethod
        def rgb(cls, r:int, g:int, b:int) -> str:
            """
            Returns an ANSI escape code for RGB background color.
            
            :param r: Red component (0-255).
            :param g: Green component (0-255).
            :param b: Blue component (0-255).
            :return: An ANSI escape code for RGB background color.
            """
             
            return "\u001b[48;2;{};{};{}m".format(r, g, b)

    class OP:
        """
        A class for managing ANSI escape codes for font attributes and cursor positioning.
        This class provides methods to control font styles and cursor movement using ANSI escape codes.
        It supports actions such as resetting attributes, applying bold, underline, and reverse effects, clearing the screen or lines, and moving the cursor.
        """
        
        RESET = "\u001b[0m"
        BOLD = "\u001b[1m"
        UNDER_LINE = "\u001b[4m"
        REVERSE = "\u001b[7m"
        CLEAR = "\u001b[2J"
        CLEAR_LINE = "\u001b[2K"
        TOP = "\u001b[0;0H"

        @classmethod
        def up(cls, n:int) -> str:
            """
            Cursor up
            
            :param n: Number of lines to move up.
            :return: An ANSI escape code to move the cursor up.
            """
            return "\u001b[{}A".format(n)

        @classmethod
        def down(cls, n:int) -> str:
            """
            Cursor down
            
            :param n: Number of lines to move down.
            :return: An ANSI escape code to move the cursor down.
            """
            
            return "\u001b[{}B".format(n)

        @classmethod
        def right(cls, n:int) -> str:
            """
            Cursor right
            
            :param n: Number of columns to move right.
            :return: An ANSI escape code to move the cursor right.
            """
            
            return "\u001b[{}C".format(n)

        @classmethod
        def left(cls, n:int) -> str:
            """
            Cursor left
            
            :param n: Number of columns to move left.
            :return: An ANSI escape code to move the cursor left.
            """
            
            return "\u001b[{}D".format(n)
        
        @classmethod
        def next_line(cls, n:int) -> str:
            """
            Cursor down to next line
            
            :param n: Number of lines to move down.
            :return: An ANSI escape code to move the cursor down.
            """
            
            return "\u001b[{}E".format(n)

        @classmethod
        def prev_line(cls, n:int) -> str:
            """
            Cursor up to previous line
            
            :param n: Number of lines to move up.
            :return: An ANSI escape code to move the cursor up.
            """
            
            return "\u001b[{}F".format(n)
                
        @classmethod
        def to(cls, row:int, colum:int) -> str:
            """
            Move cursor to specified row and column.
            
            :param row: Row number (1-based).
            :param colum: Column number (1-based).
            :return: An ANSI escape code to move the cursor.
            """
            
            return "\u001b[{};{}H".format(row, colum)

def rand(size:int=4) -> int:
    """
    Generates a random number of the specified size in bytes.
    
    :param size: The size of the random number in bytes. Default is 4 bytes.
    :return: A random number of the specified size.
    """
    
    return int.from_bytes(uos.urandom(size), "big")

def map(x:int|float, min_i:int|float, max_i:int|float, min_o:int|float, max_o:int|float) -> int|float:
    """
    Maps a value from one range to another.

    :param x: The value to be mapped.
    :param min_i: The minimum value of the input range.
    :param min_o: The minimum value of the output range.
    :return: The mapped value.
    """
    
    return (x - min_i) * (max_o - min_o) / (max_i - min_i) + min_o

def xrange(start:float, stop:float=None, step:float=None) -> any:
    """
    A generator function to create a range of floating point numbers.
    This is a replacement for the built-in range function for floating point numbers.   
    :param start: Starting value of the range.
    :param stop: Ending value of the range.
    :param step: Step size for the range.
    :return: A range object that generates floating point numbers.
    """
    
    if stop is None:
        stop = start
        start = 0.0

    if step is None:
        step = 1.0 if stop > start else -1.0

    if step == 0.0:
        raise ValueError("step must not be zero")
    if (stop - start) * step < 0.0:
        return  # empty range

    round_digits = len(f"{step}".split('.')[1])
    
    current = start
    epsilon = abs(step) / 10_000_000

    while (step > 0 and current < stop - epsilon) or (step < 0 and current > stop + epsilon):
        yield round(current, round_digits)
        current += step

def intervalChecker(interval:int) -> callable:
    """
    Creates a function that checks if the specified interval has passed since the last call.
    
    :param interval: The interval in milliseconds.
    :return: A function that checks if the interval has passed.
    """
    
    current_tick = utime.ticks_us()   
    
    def check_interval():
        nonlocal current_tick
        
        if utime.ticks_diff(utime.ticks_us(), current_tick) >= interval * 1000:
            current_tick = utime.ticks_us()
            return True
        return False
    
    return check_interval

def WDT(timeout:int) -> machine.WDT:
    """
    Creates a watchdog timer (WDT) object with the specified timeout.
    
    :param timeout: The timeout in seconds.
    :return: A WDT object.
    """
    
    return machine.WDT(0, timeout)

def i2cdetect(bus:int=1, show:bool=False) -> list | None:
    """
    Detect I2C devices on the specified bus.
    
    :param bus: The I2C bus number. Default is 1.
    :param show: If True, print the detected devices. Default is False.
    :return: A list of detected I2C devices.
    """
    
    i2c = machine.I2C(bus)
    devices = i2c.scan()

    if not show:
        return devices
    else:
        print("     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f")
        for i in range(0, 8):
            print("{:02x}:".format(i*16), end='')
            for j in range(0, 16):
                address = i * 16 + j
                if address in devices:
                    print(ANSIEC.FG.BRIGHT_YELLOW + " {:02x}".format(address) + ANSIEC.OP.RESET, end='')
                else:
                    print(" --", end='')
            print()


class Slip:
    """
    SLIP (Serial Line Internet Protocol) encoder/decoder.
    This class provides methods to encode and decode SLIP packets.
    It uses the SLIP protocol to encapsulate data for transmission over serial lines.
    """

    END = b'\xC0'
    ESC = b'\xDB'
    ESC_END = b'\xDC'
    ESC_ESC = b'\xDD'
    
    __decode_state = {'started': False, 'escaped': False, 'data': bytearray(), 'pending_end': False, 'junk': bytearray()}
    
    @staticmethod
    def decode(chunk: bytes) -> list:
        """
        SLIP decoder. Returns a list of decoded byte strings.
        
        :param chunk: A byte string to decode.
        :return: A list of bytes.
        """
        result = []
        data = Slip.__decode_state['data']
        junk = Slip.__decode_state['junk']
        started = Slip.__decode_state['started']
        escaped = Slip.__decode_state['escaped']
        pending_end = Slip.__decode_state['pending_end']

        for char in chunk:
            if escaped:
                if char == ord(Slip.ESC_END):
                    data.append(ord(Slip.END))
                elif char == ord(Slip.ESC_ESC):
                    data.append(ord(Slip.ESC))
                else:
                    data.clear()
                    started = False
                    pending_end = False
                    return []
                escaped = False
            elif char == ord(Slip.ESC):
                escaped = True
            elif char == ord(Slip.END):
                if pending_end:
                    if started:
                        result.append(bytes(data))
                        data.clear()
                    else:
                        junk.clear()
                    started = True
                    pending_end = False
                elif started:
                    result.append(bytes(data))
                    data.clear()
                    started = False
                    pending_end = True
                else:
                    started = True
                    pending_end = True
            else:
                if pending_end:
                    started = True
                    data.append(char)
                    pending_end = False
                elif started:
                    data.append(char)
                else:
                    junk.append(char)

        Slip.__decode_state['started'] = started
        Slip.__decode_state['escaped'] = escaped
        Slip.__decode_state['pending_end'] = pending_end

        return result
    
    @staticmethod
    def encode(payload: bytes) -> bytes:
        """
        SLIP encoder. Returns a byte string.
        
        :param payload: A byte string to encode.
        :return: A byte string.
        """
        return Slip.END + payload.replace(Slip.ESC, Slip.ESC + Slip.ESC_ESC).replace(Slip.END, Slip.ESC + Slip.ESC_END) + Slip.END


class ReplSerial:
    """
    Handle REPL UART or USB I/O with optional timeout support.
    Uses non-blocking, select-based reads.
    """

    def __init__(self, timeout:float=None):
        """
        Initialize with an optional timeout (in seconds).
        
        :param timeout: The timeout in seconds. Default is None (blocking read).
        - timeout=None : blocking read
        - timeout=0    : non-blocking read
        - timeout>0    : wait up to timeout seconds
        """
        self._timeout = timeout
        self._stdin = usys.stdin.buffer
        self._stdout = usys.stdout

    @property
    def timeout(self):
        """Get the current timeout in seconds."""
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        """Set the timeout in seconds."""
        self._timeout = value

    def read(self, size=1) -> bytes:
        """
        Read up to `size` bytes from the REPL.
        - Blocking if timeout is None.
        - Non-blocking if timeout == 0.
        - Wait up to timeout seconds if timeout > 0.
        
        :param size: The number of bytes to read (default is 1).
        :return: The read bytes as a byte string.
        """
        if self._timeout is None:
            return self._stdin.read(size) or b''

        ready, _, _ = uselect.select([self._stdin], [], [], self._timeout)
        if not ready:
            return b''

        return self._stdin.read(size) or b''

    def read_until(self, expected: bytes = b'\n', max_size: int | None = None) -> bytes:
        """
        Read until `expected` sequence is seen, `max_size` reached, or timeout occurs.
        
        :param expected: The expected byte sequence to look for (default is b'\n').
        :param max_size: The maximum size of data to read (default is None, no limit).
        :return: The data including the expected sequence.
        """
        buf = bytearray()
        exp_len = len(expected)
        # calculate deadline if we have a positive timeout
        deadline = None
        if self._timeout and self._timeout > 0:
            deadline = utime.ticks_add(utime.ticks_ms(), int(self._timeout * 1000))

        while True:
            # check for timeout
            if deadline and utime.ticks_diff(deadline, utime.ticks_ms()) <= 0:
                break

            ready, _, _ = uselect.select([self._stdin], [], [], self._timeout)
            if not ready:
                continue

            chunk = self._stdin.read(1)
            if not chunk:
                continue

            buf += chunk
            # stop if we've hit max_size
            if max_size and len(buf) >= max_size:
                return bytes(buf[:max_size])
            # stop if we see the expected pattern
            if len(buf) >= exp_len and buf[-exp_len:] == expected:
                return bytes(buf)

        return bytes(buf)

    def write(self, data: bytes) -> int:
        """
        Write `data` to the REPL UART.
        
        :param data: The data to write (must be bytes or bytearray).
        :return: The number of bytes written.
        """
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("data must be bytes or bytearray")
        return self._stdout.write(data)


def __char_width(ch: str) -> int:
    """
    Return 1 for ASCII, 2 for anything that encodes to >1 byte in UTF-8.
    (Good enough for Hangul/CJK; replace with wcwidth() if you need full Unicode support.)
    """
    return 1 if len(ch.encode('utf-8')) == 1 else 2

def _input(prompt: str = "") -> str:
    """
    Blocking input() replacement with:
      - UTF-8 decoding (1–4 bytes per char)
      - ←/→ arrow cursor movement
      - Backspace deletes before cursor
      - Deletes at cursor
      - Proper insertion anywhere in the line
    """
    repl = ReplSerial(timeout=None)
    if prompt:
        repl.write(prompt.encode())

    buf = []    # list of str characters
    pos = 0     # cursor position in characters

    while True:
        b = repl.read(1)
        if not b:
            continue
        
        # Enter
        if b in (b'\r', b'\n'):
            repl.write(b'\r\n')
            break
        
        # Escape sequences: arrows and delete
        if b == b'\x1b':
            seq = repl.read(2)
            
            # Left arrow
            if seq == b'[D' and pos > 0:
                pos -= 1
                w = __char_width(buf[pos])
                repl.write(f"\x1b[{w}D".encode())
            # Right arrow
            elif seq == b'[C' and pos < len(buf):
                w = __char_width(buf[pos])
                repl.write(f"\x1b[{w}C".encode())
                pos += 1
            # Delete key
            elif seq == b'[3':
                terminator = repl.read(1) # consume the '~'
                if pos < len(buf):
                    removed = buf.pop(pos)
                    repl.write(b'\x1b[K')
                    tail = "".join(buf[pos:])
                    if tail:
                        repl.write(tail.encode())
                        tail_w = sum(__char_width(c) for c in tail)
                        repl.write(f"\x1b[{tail_w}D".encode())
            continue

        # Backspace
        if b in (b'\x08', b'\x7f'):
            if pos > 0:
                pos -= 1
                removed = buf.pop(pos)
                w = __char_width(removed)
                repl.write(f"\x1b[{w}D".encode())
                repl.write(b'\x1b[K')
                tail = "".join(buf[pos:]).encode()
                if tail:
                    repl.write(tail)
                    tail_w = sum(__char_width(c) for c in buf[pos:])
                    repl.write(f"\x1b[{tail_w}D".encode())
            continue


        # Decode a full UTF-8 character
        first = b[0]
        if first & 0x80 == 0:
            seq = b
        elif first & 0xE0 == 0xC0:
            seq = b + repl.read(1)
        elif first & 0xF0 == 0xE0:
            seq = b + repl.read(2)
        elif first & 0xF8 == 0xF0:
            seq = b + repl.read(3)
        else:
            continue

        try:
            ch = seq.decode('utf-8')
        except UnicodeError:
            continue

        # Insert & redraw
        buf.insert(pos, ch)
        w = __char_width(ch)
        tail = "".join(buf[pos+1:]).encode()

        repl.write(seq)

        if tail:
            repl.write(tail)
            tail_w = sum(__char_width(c) for c in buf[pos+1:])
            repl.write(f"\x1b[{tail_w}D".encode())
        pos += 1

    return "".join(buf)
