
class Escape:
	def escape_to_param(self, txt):
		if txt is not None:
			txt = str(txt)
			return txt.replace("'", "").replace('"', "").replace("<", "").replace(">", "")
		else:
			return txt
