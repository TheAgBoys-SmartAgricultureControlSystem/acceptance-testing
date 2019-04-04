from tkinter import *
from tkinter.ttk import *


class FloatEntry(Entry):

	def __init__(self, *args, **kwargs):
		initial_value = kwargs.pop('initial_value', '000.000000')
		assert self.validate(initial_value), 'Invalid initial_value given'
		self.last_valid_value = initial_value
		self.text = StringVar(value=initial_value)

		Entry.__init__(self, *args, textvariable=self.text, **kwargs)
		self.vcmd = self.register(self.validate)
		self.ivcmd = self.register(self.invalidate)
		self['validate'] = 'focusout'
		self['validatecommand'] = self.vcmd, '%P',
		self['invalidcommand'] = self.ivcmd,

	def validate(self, inp):
		try:
			float(inp)
		except ValueError:
			return False
		self.last_valid_value = inp
		return True

	def invalidate(self):
		self.text.set(self.last_valid_value)


class IntEntry(Entry):

	def __init__(self, *args, **kwargs):
		initial_value = kwargs.pop('initial_value', '99')
		assert self.validate(initial_value), 'Invalid initial_value given'
		self.last_valid_value = initial_value
		self.text = StringVar(value=initial_value)

		Entry.__init__(self, *args, textvariable=self.text, **kwargs)
		self.vcmd = self.register(self.validate)
		self.ivcmd = self.register(self.invalidate)
		self['validate'] = 'focusout'
		self['validatecommand'] = self.vcmd, '%P',
		self['invalidcommand'] = self.ivcmd,

	def validate(self, inp):
		try:
			int(inp)
		except ValueError:
			return False
		self.last_valid_value = inp
		return True

	def invalidate(self):
		self.text.set(self.last_valid_value)


class StrEntry(Entry):

	def __init__(self, *args, **kwargs):
		initial_value = kwargs.pop('initial_value', '99')
		assert self.validate(initial_value), 'Invalid initial_value given'
		self.last_valid_value = initial_value
		self.text = StringVar(value=initial_value)

		Entry.__init__(self, *args, textvariable=self.text, **kwargs)
		self.vcmd = self.register(self.validate)
		self.ivcmd = self.register(self.invalidate)
		self['validate'] = 'focusout'
		self['validatecommand'] = self.vcmd, '%P',
		self['invalidcommand'] = self.ivcmd,

	def validate(self, inp):
		try:
			str(inp)
		except ValueError:
			return False
		self.last_valid_value = inp
		return True

	def invalidate(self):
		self.text.set(self.last_valid_value)
