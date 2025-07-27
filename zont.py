#!/usr/bin/env python3
"""
zont - Time Zone Converter
Convert times between time zones with clean terminal interface.
"""

import os
import sys
import argparse
import re
from datetime import datetime
from zoneinfo import ZoneInfo, available_timezones
import zoneinfo

# Optional dependency for TUI
try:
    from prompt_toolkit import prompt
    from prompt_toolkit.completion import WordCompleter
    from prompt_toolkit.shortcuts import confirm
    HAS_PROMPT_TOOLKIT = True
except ImportError:
    HAS_PROMPT_TOOLKIT = False

# Colors
GREEN = '\033[92m'
BLUE = '\033[94m'
CYAN = '\033[96m'
WHITE = '\033[97m'
GRAY = '\033[90m'
RED = '\033[91m'
BOLD = '\033[1m'
RESET = '\033[0m'

class TimeZoneConverter:
    def __init__(self):
        # Common timezone abbreviations to full names
        self.timezone_abbrevs = {
            'EST': 'America/New_York',
            'PST': 'America/Los_Angeles', 
            'MST': 'America/Denver',
            'CST': 'America/Chicago',
            'GMT': 'Europe/London',
            'UTC': 'UTC',
            'JST': 'Asia/Tokyo',
            'CET': 'Europe/Paris',
            'IST': 'Asia/Kolkata',
            'AEST': 'Australia/Sydney'
        }
        
        # Get all available timezones for autocomplete
        self.all_timezones = sorted(available_timezones())
        
    def normalize_timezone(self, tz_input):
        """Convert timezone input to proper ZoneInfo timezone"""
        tz_input = tz_input.strip()
        
        # Check if it's an abbreviation
        if tz_input.upper() in self.timezone_abbrevs:
            return self.timezone_abbrevs[tz_input.upper()]
            
        # Check if it's already a valid timezone
        if tz_input in self.all_timezones:
            return tz_input
            
        # Try to find a close match
        for tz in self.all_timezones:
            if tz_input.lower() in tz.lower():
                return tz
                
        raise ValueError(f"Unknown timezone: {tz_input}")
    
    def parse_time_input(self, time_str, source_tz):
        """Parse various time formats"""
        time_str = time_str.strip()
        
        if time_str.lower() == 'now':
            return datetime.now(ZoneInfo(source_tz))
        
        # Handle formats like "3pm", "15:00", "3:30pm"
        patterns = [
            (r'^(\d{1,2})([ap]m)$', '%I%p'),           # 3pm, 11am
            (r'^(\d{1,2}):(\d{2})([ap]m)$', '%I:%M%p'), # 3:30pm
            (r'^(\d{1,2}):(\d{2})$', '%H:%M'),         # 15:30, 03:30
            (r'^(\d{4}-\d{2}-\d{2}\s+\d{1,2}:\d{2})$', '%Y-%m-%d %H:%M') # 2024-01-15 15:00
        ]
        
        for pattern, fmt in patterns:
            if re.match(pattern, time_str, re.IGNORECASE):
                try:
                    if 'Y' in fmt:  # Full datetime
                        dt = datetime.strptime(time_str, fmt)
                        return dt.replace(tzinfo=ZoneInfo(source_tz))
                    else:  # Time only, use today's date
                        today = datetime.now().date()
                        dt = datetime.strptime(time_str.upper(), fmt)
                        dt = dt.replace(year=today.year, month=today.month, day=today.day)
                        return dt.replace(tzinfo=ZoneInfo(source_tz))
                except ValueError:
                    continue
        
        raise ValueError(f"Could not parse time: {time_str}")
    
    def convert_time(self, time_str, from_tz, to_tz):
        """Convert time from one timezone to another"""
        try:
            # Normalize timezone names
            source_tz = self.normalize_timezone(from_tz)
            target_tz = self.normalize_timezone(to_tz)
            
            # Parse the time
            source_time = self.parse_time_input(time_str, source_tz)
            
            # Convert to target timezone
            target_time = source_time.astimezone(ZoneInfo(target_tz))
            
            return {
                'source_time': source_time,
                'target_time': target_time,
                'source_tz': source_tz,
                'target_tz': target_tz
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def format_result(self, result):
        """Format conversion result for display"""
        if 'error' in result:
            return f"{RED}❌ Error: {result['error']}{RESET}"
        
        source = result['source_time']
        target = result['target_time']
        
        # Format times
        source_fmt = source.strftime('%I:%M %p %Z').lstrip('0')
        target_fmt = target.strftime('%I:%M %p %Z').lstrip('0')
        
        # Check if date changed
        date_info = ""
        if source.date() != target.date():
            if target.date() > source.date():
                date_info = f" {GRAY}(+1 day){RESET}"
            else:
                date_info = f" {GRAY}(-1 day){RESET}"
        
        output = f"{CYAN}🕐 {source_fmt}{RESET} → {GREEN}{target_fmt}{date_info}{RESET}"
        return output

def cli_mode(args):
    """Handle CLI conversions"""
    converter = TimeZoneConverter()
    
    if len(args.conversion) < 4 or args.conversion[-2].lower() != 'to':
        print(f"{RED}❌ Usage: zont <time> <from_tz> to <to_tz>{RESET}")
        print(f"{GRAY}Example: zont 3pm EST to PST{RESET}")
        return
    
    # Parse arguments
    to_index = -2  # 'to' is second to last
    time_parts = args.conversion[:to_index-1]
    from_tz = args.conversion[to_index-1]
    to_tz = args.conversion[-1]
    
    time_str = ' '.join(time_parts)
    
    result = converter.convert_time(time_str, from_tz, to_tz)
    print(converter.format_result(result))

def tui_mode():
    """Handle TUI with progressive forms"""
    if not HAS_PROMPT_TOOLKIT:
        print(f"{RED}❌ TUI mode requires prompt_toolkit{RESET}")
        print(f"{GRAY}Install with: pip install prompt-toolkit{RESET}")
        return
    
    converter = TimeZoneConverter()
    
    # Create timezone completer
    all_tz_options = converter.all_timezones + list(converter.timezone_abbrevs.keys())
    tz_completer = WordCompleter(all_tz_options, ignore_case=True)
    
    try:
        # Clear screen and show header
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{BLUE}╔═ ZONT - Time Zone Converter ═══════════════════════════════╗{RESET}")
        print(f"{BLUE}║{RESET} Enter time and zones for conversion                     {BLUE}║{RESET}")
        print(f"{BLUE}╚═════════════════════════════════════════════════════════════╝{RESET}")
        print()
        
        # Step 1: Get time
        time_input = prompt("🕐 Time (3pm, 15:30, now): ")
        
        # Step 2: Get source timezone
        from_tz = prompt("📍 From timezone: ", completer=tz_completer)
        
        # Step 3: Get target timezone  
        to_tz = prompt("📍 To timezone: ", completer=tz_completer)
        
        # Convert and display result
        print(f"\n{BLUE}╔═ Result ═══════════════════════════════════════════════════╗{RESET}")
        result = converter.convert_time(time_input, from_tz, to_tz)
        print(f"{BLUE}║{RESET} {converter.format_result(result):<60} {BLUE}║{RESET}")
        print(f"{BLUE}╚═════════════════════════════════════════════════════════════╝{RESET}")
        
        # Ask if they want to convert another
        print()
        if confirm("Convert another time?"):
            tui_mode()
            
    except KeyboardInterrupt:
        print(f"\n{GREEN}👋 Goodbye!{RESET}")
    except EOFError:
        print(f"\n{GREEN}👋 Goodbye!{RESET}")

def main():
    parser = argparse.ArgumentParser(
        description='zont - Convert times between time zones',
        epilog='Examples:\n'
               '  zont 3pm EST to PST\n'
               '  zont 15:30 UTC to Asia/Tokyo\n'
               '  zont now America/New_York to Europe/London\n'
               '  zont --tui  (interactive mode)',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--tui', action='store_true', 
                       help='Launch interactive TUI mode')
    parser.add_argument('--version', action='version', version='zont 1.0.0')
    parser.add_argument('conversion', nargs='*', 
                       help='Time and timezone conversion (e.g., "3pm EST to PST")')
    
    args = parser.parse_args()
    
    if args.tui:
        tui_mode()
    elif args.conversion:
        cli_mode(args)
    else:
        # No arguments, show help
        parser.print_help()

if __name__ == "__main__":
    main()