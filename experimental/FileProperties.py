import gtk
import gobject
from File import *
class FileProperties():
	def __init__(self,sys):
		self.sys = sys
		self.fobj = None
		self.xml = gtk.glade.XML("fileproperties.glade")
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
		self.tagTree = gtk.TreeView(self.tagModel)
		self.tagTree.connect('row-activated',self.addClickedTag)
		self.tagCont.add(self.tagTree)
		#Spalte 1
		self.tagCl1 = gtk.TreeViewColumn('Tag Name')
		self.tagTree.append_column(self.tagCl1)
		#Definition der Text der 1. Spalte
		tagRender = gtk.CellRendererText()
		self.tagCl1.pack_start(tagRender)
		self.tagCl1.add_attribute(tagRender,'text',0)
		


		#Model Tag
		self.restoreModel = gtk.TreeStore(gobject.TYPE_STRING, gobject.TYPE_PYOBJECT)
		self.restoreTree = gtk.TreeView(self.restoreModel)
		self.restoreTree.connect('cursor-changed',self.updateRestoreButton)
		self.restoreTree.connect('button_release_event',self.showContext)
		self.restoreCont.add(self.restoreTree)
		#Spalte 1
		self.restoreCl1 = gtk.TreeViewColumn('Datum')
		self.restoreTree.append_column(self.restoreCl1)
		#Definition der Text der 1. Spalte
		restoreRender = gtk.CellRendererText()
		self.restoreCl1.pack_start(restoreRender)
		self.restoreCl1.add_attribute(restoreRender,'text',0)
		#self.restoreTree.connect('row-activated',self.showRestoreBtn)
		

		self.update(None)
		self.main.show_all()

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
		if isinstance(self.fobj,File):
			backups = self.fobj.getBackups()
			for b in backups:
				self.restoreModel.append(None,[b.getFileName(),b])
		elif type(self.fobj) == list:
			backupArray = self.sys.tagmanager.getBackups(self.fobj[0])
			for b in backupArray:
				self.restoreModel.append(None,[b.getFileName(),b])


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
			tags = self.txtTags.get_text().split(',')
			l = len(tags)
			newtags = []
			for i in range(len(tags)):
				if tags[i].strip() != '':
					newtags.append(tags[i].strip())
			tags = list(set(newtags))
			self.fobj.setTags(newtags)
			self.sys.db.updateFile(self.fobj)
			self.update(self.fobj)
			self.sys.gui.actview.update()

	def updateButtons(self):
			if(isinstance(self.fobj,File) or type(self.fobj) == list):
				self.btnBackup.set_sensitive(True)
			else:
				self.btnBackup.set_sensitive(False)
			self.btnRestore.set_sensitive(False)
			
	def updateRestoreButton(self,event):
		self.btnRestore.set_sensitive(True)

	def backup(self,event):
		if isinstance(self.fobj,File):
			self.fobj.makeBackup()
		elif type(self.fobj) == list:
			self.sys.tagmanager.makeBackup(self.fobj[0])
		self.update(self.fobj)
		self.sys.gui.actview.update()

	def getSelectedBackup(self):
		treeview = self.restoreTree
		selection = treeview.get_selection()
		selection.set_mode(gtk.SELECTION_SINGLE)
		tree_model, tree_iter = selection.get_selected()
		return tree_model.get_value(tree_iter,1)

	def restore(self,event):
		if isinstance(self.fobj,File):
			self.fobj.restoreFrom(self.getSelectedBackup())
		elif type(self.fobj) == list:
			self.sys.tagmanager.restoreFrom(self.fobj[0],self.getSelectedBackup())

	def showContext(self, treeview, event):
		if event.button == 3:
			f = self.getSelectedBackup()
			m = gtk.Menu()
			m1 = gtk.MenuItem("Backup entfernen")
			m.append(m1)
			m1.connect('button_press_event',self.removeBackup,f)
			m.show_all()
			m.popup( None, None, None, event.button, event.time)
			return True
		return False

	def removeBackup(self,widget,event,bf):
		f = File(bf.getFullPath()+'/'+self.fobj.getFileName())
		f.remove()
		self.sys.db.updateFile(self.fobj)
		self.update(self.fobj)
		
