"""
FML Continuous Parser - Validates and processes Fibonacci Markup Language documents
with continuous Fibonacci indentation rules
"""
import re
import markdown
from typing import List, Tuple, Dict, Any, Optional


class FMLError(Exception):
    """Exception raised for errors in the FML syntax."""
    pass


class FMLContinuousParser:
    """Parser for Fibonacci Markup Language with continuous indentation rules."""
    
    # Pre-compute Fibonacci numbers for efficiency
    FIBONACCI_NUMBERS = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987]
    
    # Humorous error messages
    ERROR_MESSAGES = [
        "Fibonacci is disappointed in your indentation choices.",
        "Your indentation has disturbed the mathematical harmony of the universe.",
        "Leonardo Fibonacci would like a word with you about your spacing.",
        "That indentation is so non-Fibonacci it hurts.",
        "The ghost of Fibonacci has entered the chat and is not pleased.",
        "Your code's indentation is mathematically offensive.",
        "Fibonacci called. He wants his sequence back - properly used this time.",
        "Error: Indentation does not compute in the Fibonacci realm.",
        "Your spaces have failed to follow the divine mathematical order."
    ]
    
    def __init__(self):
        """Initialize the FML parser."""
        import random
        self.random = random
    
    def _get_indentation(self, line: str) -> int:
        """
        Count the number of leading spaces in a line.
        
        Args:
            line: The line to analyze
            
        Returns:
            The number of leading spaces
        """
        match = re.match(r'^(\s*)', line)
        if match:
            return len(match.group(1))
        return 0
    
    def _is_fibonacci(self, n: int) -> bool:
        """
        Check if a number is in the Fibonacci sequence.
        
        Args:
            n: The number to check
            
        Returns:
            True if the number is in the Fibonacci sequence, False otherwise
        """
        return n in self.FIBONACCI_NUMBERS
    
    def _get_next_fibonacci(self, n: int) -> int:
        """
        Get the next Fibonacci number after n.
        
        Args:
            n: The current number
            
        Returns:
            The next Fibonacci number
        """
        for fib in self.FIBONACCI_NUMBERS:
            if fib > n:
                return fib
        return self.FIBONACCI_NUMBERS[-1]  # Return the largest pre-computed Fibonacci number
    
    def _get_error_message(self, indentation: int, expected_indentation: int) -> str:
        """
        Generate a humorous error message for invalid indentation.
        
        Args:
            indentation: The invalid indentation level
            expected_indentation: The expected indentation level
            
        Returns:
            A humorous error message
        """
        message = self.random.choice(self.ERROR_MESSAGES)
        suggestion = f"Try {expected_indentation} spaces instead of {indentation}."
        return f"{message} {suggestion}"
    
    def parse(self, content: str) -> List[Dict[str, Any]]:
        """
        Parse FML content and validate continuous indentation levels.
        
        Args:
            content: The FML content to parse
            
        Returns:
            A list of parsed lines with their indentation levels and content
            
        Raises:
            FMLError: If any line has an indentation level that doesn't follow the continuous rules
        """
        lines = content.splitlines()
        result = []
        
        in_code_block = False
        code_block_indent = 0
        code_language = None
        current_indent = 0  # Track the current indentation level
        
        for i, line in enumerate(lines, 1):
            if not line.strip():  # Skip empty lines
                continue
                
            indentation = self._get_indentation(line)
            content = line.strip()
            
            # Check if this is the start or end of a code block
            if content.startswith('```'):
                if not in_code_block:  # Start of code block
                    in_code_block = True
                    code_block_indent = indentation
                    if len(content) > 3:
                        code_language = content[3:].strip()
                    
                    # Validate the indentation of the code block marker
                    if indentation != 0 and indentation != current_indent and indentation != self._get_next_fibonacci(current_indent):
                        expected = self._get_next_fibonacci(current_indent)
                        error_msg = f"{self.random.choice(self.ERROR_MESSAGES)} Try {expected} spaces instead of {indentation}. (Current: {current_indent}, Next: {expected})"
                        raise FMLError(f"Line {i}: {error_msg}")
                    
                    # Update current indentation
                    current_indent = indentation
                else:  # End of code block
                    in_code_block = False
                    code_language = None
                    
                    # Validate the indentation of the code block marker
                    if indentation != code_block_indent:
                        error_msg = f"Code block closing marker must have the same indentation as opening marker. (Current: {indentation}, Expected: {code_block_indent})"
                        raise FMLError(f"Line {i}: {error_msg}")
            elif not in_code_block:  # Regular line outside code block
                # Validate continuous indentation rules
                if indentation == 0:
                    # 0 is always allowed to reset the sequence
                    pass
                elif indentation == current_indent:
                    # Same indentation as previous line is allowed
                    pass
                elif indentation == self._get_next_fibonacci(current_indent):
                    # Next Fibonacci number is allowed
                    pass
                elif indentation < current_indent:
                    # Decreasing indentation is not allowed (except reset to 0)
                    error_msg = f"Decreasing indentation is not allowed. You can only reset to 0 spaces or increase to the next Fibonacci number. (Current: {current_indent}, Your indentation: {indentation})"
                    raise FMLError(f"Line {i}: {error_msg}")
                else:
                    # Check if the indentation is a Fibonacci number but not the next one in sequence
                    if self._is_fibonacci(indentation):
                        expected = self._get_next_fibonacci(current_indent)
                        error_msg = f"You can't skip Fibonacci numbers! After {current_indent} spaces, you must use exactly {expected} spaces, not {indentation}. (Current: {current_indent}, Next: {expected})"
                        raise FMLError(f"Line {i}: {error_msg}")
                    else:
                        # Not a Fibonacci number at all
                        expected = self._get_next_fibonacci(current_indent)
                        error_msg = f"{self.random.choice(self.ERROR_MESSAGES)} Try {expected} spaces instead of {indentation}. (Current: {current_indent}, Next: {expected})"
                        raise FMLError(f"Line {i}: {error_msg}")
                
                # Update current indentation
                current_indent = indentation
            
            # Add the line to the result
            result.append({
                "line_number": i,
                "indentation": indentation,
                "content": content,
                "raw": line,
                "is_code_block": content.startswith('```'),
                "code_language": code_language if content.startswith('```') and not in_code_block else None,
                "in_code_block": in_code_block and not content.startswith('```')
            })
        
        return result
    
    def validate(self, content: str) -> Tuple[bool, Optional[str]]:
        """
        Validate FML content without parsing it fully.
        
        Args:
            content: The FML content to validate
            
        Returns:
            A tuple of (is_valid, error_message)
        """
        try:
            self.parse(content)
            return True, None
        except FMLError as e:
            return False, str(e)
