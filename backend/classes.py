#!/usr/bin/env python3
"""Classes dependent on the configuration of the server"""

class Stack:
    """Stack to keep temporary data"""
    def __init__(self):
        self.stack = {}

    def push(self, key, value):
        self.stack[key] = value

    def pop(self, key):
        return self.stack.pop(key)

    def get(self, key):
        return self.stack.get(key)

    def __str__(self):
        return str(self.stack)

    def __repr__(self):
        return str(self.stack)