#!/usr/bin/python
import gtk

class GUI(gtk.Window):
	def __init__(self):
		#Init-Fenster
		super(GUI,self).__init__()
		#self.connect("destroy", gtk.main_quit)

		#Fenster-Properties
		self.set_size_request(250, 150)
		self.set_position(gtk.WIN_POS_CENTER)
		self.set_title('Test-Fenster')
		self.show()
		
		#Button-Objekt
		self.button = gtk.Button("Hello World")
		self.button.connect('clicked',self.hello)
		self.button.show()

		
		self.add(self.button)

	def main(self):
		gtk.main()

	def hello(self,widget,data=None):
		widget.set_label('geklickt')
		print('event: '+str(widget)+', '+str(data))

if __name__ == "__main__":
	try:
		gui = GUI()
		gui.main()
	except KeyboardInterrupt:
		print('Programm geschlossen')
