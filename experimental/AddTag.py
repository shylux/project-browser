import gtk
import gobject
from File import *
class AddTag():
	def __init__(self,sys):
		self.sys = sys
		self.fobj = None
		self.xml = gtk.glade.XML("addTag.glade")
		self.main = self.xml .get_widget("vbxMain")
		self.txtFiles = self.xml.get_widget("txtFileNames")
		self.txtTags = self.xml.get_widget("txtTags")
		self.txtTags.connect('key-release-event',self.enterEventHandler)
		#self.txtTags.connect('drag_data_received', self.test)
		self.btnSave = self.xml.get_widget("btnSave")
		self.btnSave.connect('button_release_event',self.save)
		self.tagCont = self.xml.get_widget("conTagList")
		self.restoreCont = self.xml.get_widget("conRestoreList")

		#Backup/Restore
		self.btnBackup = self.xml.get_widget("btnBackup")
		self.btnBackup.connect('clicked',self.backup)
		self.btnBackup.set_sensitive(False)
		self.btnRestore = self.xml.get_widget("btnRestore")
		self.btnRestore.connect('clicked',self.restore)
		self.btnRestore.set_sensitive(False)

		#Model Tag
		self.tagModel = gtk.TreeStore(gobject.TYPE_STRING)
		self.treeTag = gtk.TreeView(self.tagModel)
		#self.treeTag.drag_source_set(gtk.gdk.BUTTON1_MASK,self.tagModel,gtk.gdk.ACTION_DEFAULT)
		self.treeTag.connect('row-activated',self.addClickedTag)
		self.tagCont.add(self.treeTag)
		#Spalte 1
		self.cl1 = gtk.TreeViewColumn('Tag Name')
		self.treeTag.append_column(self.cl1)
		#Definition der Text der 1. Spalte
		render = gtk.CellRendererText()
		self.cl1.pack_start(render)
		self.cl1.add_attribute(render,'text',0)
		
		#Model Tag
		self.restoreModel = gtk.TreeStore(gobject.TYPE_STRING)
		self.restoreTag = gtk.TreeView(self.tagModel)
		#self.restoreTag.connect('row-activated',self.showRestoreBtn)
		

		self.updateModel()
		self.main.show_all()

	def test(self):
		print('test')

	def update(self,fobj):
		self.clearAll()
		self.fobj = None
		self.fobj = fobj
		self.txtTags.set_text(', '.join(self.fobj.getTags()))
		self.txtFiles.set_text(self.fobj.getFileName())
		self.updateModel()

	def updateModel(self):
		self.tagModel.clear()
		for tag in self.sys.db.getAllTags():
			self.tagModel.append(None,[tag])
		pass
		self.updateButtons()

	def clearAll(self):
		self.fobj = None
		self.tagModel.clear()
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

	def enterEventHandler(self,widget,event):
		if event.keyval == gtk.gdk.keyval_from_name("Return"):
			self.save(widget,event)

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

	def updateButtons(self):
			if(isinstance(self.fobj,File) or type(self.fobj) == list):
				self.btnBackup.set_sensitive(True)
			else:
				self.btnBackup.set_sensitive(False)
			self.btnRestore.set_sensitive(False)

	def backup(self,event):
		self.fobj.ex_backup()

	def restore(self,event):
		print('test')
