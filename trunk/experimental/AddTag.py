import gtk
import gobject
from File import *
class AddTag():
	def __init__(self,sys):
		self.sys = sys
		self.fobj = None
		self.xml = gtk.glade.XML("addTag.glade")
		self.main = self.xml .get_widget("vbxMain")
		self.txtObjNames = self.xml.get_widget("txtNames")
		self.lblName = self.xml.get_widget("lblName")
		self.txtTags = self.xml.get_widget("txtTags")
		self.txtTags.connect('key-release-event',self.enterEventHandler)
		#self.txtTags.connect('drag_data_received', self.test)
		self.btnSave = self.xml.get_widget("btnSave")
		self.btnSave.connect('button_release_event',self.save)
		self.hbxTag = self.xml.get_widget("hbxTag")
		self.tagCont = self.xml.get_widget("conTagList")
		self.restoreCont = self.xml.get_widget("conRestoreCont")

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
		self.treeTag.connect('row-activated',self.addClickedTag)
		self.tagCont.add(self.treeTag)
		#Spalte 1
		self.tagCl1 = gtk.TreeViewColumn('Tag Name')
		self.treeTag.append_column(self.tagCl1)
		#Definition der Text der 1. Spalte
		tagRender = gtk.CellRendererText()
		self.tagCl1.pack_start(tagRender)
		self.tagCl1.add_attribute(tagRender,'text',0)
		


		#Model Tag
		self.restoreModel = gtk.TreeStore(gobject.TYPE_STRING)
		self.restoreTag = gtk.TreeView(self.restoreModel)
		self.restoreCont.add(self.restoreTag)
		#Spalte 1
		self.restoreCl1 = gtk.TreeViewColumn('Datum')
		self.restoreTag.append_column(self.restoreCl1)
		#Definition der Text der 1. Spalte
		restoreRender = gtk.CellRendererText()
		self.restoreCl1.pack_start(restoreRender)
		self.restoreCl1.add_attribute(restoreRender,'text',0)
		#self.restoreTag.connect('row-activated',self.showRestoreBtn)
		

		self.update(None)
		self.main.show_all()

	def test(self):
		print('test')

	def update(self,fobj):
		self.clearAll()
		self.fobj = None
		self.fobj = fobj
		self.lblName.set_label('')
		self.hbxTag.set_sensitive(False)
		if isinstance(fobj,File):
			self.lblName.set_label('Datei(en)')
			self.txtTags.set_text(', '.join(self.fobj.getTags()))
			self.txtObjNames.set_text(self.fobj.getFileName())
			self.updateTagModel()
			self.updateRestoreModel('file')
			self.hbxTag.set_sensitive(True)
		elif type(fobj) == list:
			self.lblName.set_label('Tag(s)')
			self.txtObjNames.set_text(fobj[0])
			self.updateRestoreModel('tag')
			self.hbxTag.set_sensitive(False)		
		self.updateButtons()

	def updateTagModel(self):
		self.tagModel.clear()
		for tag in self.sys.db.getAllTags():
			self.tagModel.append(None,[tag])

	def updateRestoreModel(self,typ):
		self.restoreModel.clear()

	def clearAll(self):
		self.fobj = None
		self.tagModel.clear()
		self.txtObjNames.set_text('')
		self.txtTags.set_text('')
		self.updateTagModel()
		
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
				self.fobj.setTags('')
		tags = list(set(tags))
		if len(tags) != 0:
			self.fobj.setTags(tags)
			self.sys.db.updateFile(self.fobj)
		self.update(self.fobj)
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
