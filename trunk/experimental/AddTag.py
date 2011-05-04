import gtk
import gobject
class AddTag():
	def __init__(self,sys):
		self.sys = sys
		self.fobj = None
		self.xml = gtk.glade.XML("addTag.glade")
		self.main = self.xml .get_widget("vbxMain")
		self.txtFiles = self.xml.get_widget("txtFileNames")
		self.txtTags = self.xml.get_widget("txtTags")
		self.btnSave = self.xml.get_widget("btnSave")
		self.btnSave.connect('button_release_event',self.save)
		self.con = self.xml.get_widget("conTagList")		

		#Model Definition
		self.model = gtk.TreeStore(gobject.TYPE_STRING)

		#Tree Definition
		self.tree = gtk.TreeView(self.model)
		self.tree.connect('row-activated',self.addClickedTag)
		self.con.add(self.tree)

		#Spalte 1
		self.cl1 = gtk.TreeViewColumn('Tag Name')
		self.tree.append_column(self.cl1)

		#Definition der Text der 1. Spalte
		render = gtk.CellRendererText()
		self.cl1.pack_start(render)
		self.cl1.add_attribute(render,'text',0)

		#Allgemeine Tree Definitionen
		self.tree.set_search_column(0)
		self.cl1.set_sort_column_id(0)
		
		self.updateModel()
		self.main.show_all()

	def update(self,fobj):
		self.clearAll()
		self.fobj = None
		self.fobj = fobj
		self.txtTags.set_text(', '.join(self.fobj.getTags()))
		print('gesetzte tags'+str(self.fobj.getTags()))
		self.txtFiles.set_text(self.fobj.getFileName())
		self.updateModel()

	def updateModel(self):
		self.model.clear()
		for tag in self.sys.db.getAllTags():
			self.model.append(None,[tag])
		pass

	def clearAll(self):
		print('clear all')
		self.fobj = None
		self.model.clear()
		self.txtFiles.set_text('')
		self.txtTags.set_text('')
		self.updateModel()
		
	def getWidget(self):
		return self.main
		
	def addClickedTag(self,treeview, path, user_data):
		selection = treeview.get_selection()
		selection.set_mode(gtk.SELECTION_SINGLE)
		tree_model, tree_iter = selection.get_selected()
		tagname = tree_model.get_value(tree_iter,0)
		if self.txtTags.get_text() == '':
			self.txtTags.set_text(tagname)
		else:
			self.txtTags.set_text(self.txtTags.get_text()+', '+tagname)

	
	def save(self,widget,event):
		print('save')
		tags = self.txtTags.get_text().split(',')
		for i in range(len(tags)):
			if tags[i].strip() != '':
				tags[i] = tags[i].strip()
			else:
				tags.remove(tags[i])
		tags = list(set(tags))
		if len(tags) != 0:
			self.fobj.setTags(tags)
			self.sys.db.updateFile(self.fobj)
		self.updateModel()
		self.sys.gui.actview.update()
