#!/usr/bin/env python

##This file is part of PyVot
#############################################################################
#############################################################################
##                                                                         ##
##                                   Imrime                                 ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2006-2009 Cédrick FAURY

#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


#import ImageGrab
##from Tkinter import *
#import tkFileDialog
#import tkMessageBox 

#from reportlab.pdfgen import canvas
#from reportlab.lib.pagesizes import A4, landscape
#from reportlab.lib.units import cm
import os, sys
import Const, Icones
import wx
import wx.richtext as rt
#import  wx.grid as gridlib
from wx import ImageFromStream, BitmapFromImage, EmptyIcon
#import cStringIO
from wx.lib.embeddedimage import PyEmbeddedImage 
##import gui
from globdef import *
from Analyse import Couleur

#class RTFWindow(wx.TextCtrl):
#    def __init__ (self,parent):
#      wx.TextCtrl.__init__(self, parent, style = wx.TE_MULTILINE |
#                                                 wx.TE_RICH | wx.TE_READONLY)

StyleText = {}
Couleur = {}
def charger_styleText():
    Couleur["rouge"] = wx.RED
    Couleur["vert"]  = wx.ColourDatabase().Find("FOREST GREEN")
    Couleur["bleu"]  = wx.BLUE
    StyleText["Titre1"] = Const.StyleDeTexte(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD, True),wx.BLUE)
    StyleText["Titre2"] = Const.StyleDeTexte(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False),wx.BLACK)
    StyleText["Messag"] = Const.StyleDeTexte(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD, False),wx.RED) 
    StyleText["Normal"] = Const.StyleDeTexte(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False),wx.BLACK)
    StyleText["Message"] = Const.StyleDeTexte(wx.Font(8, wx.DEFAULT, wx.ITALIC, wx.NORMAL, False),wx.BLACK)
    StyleText["Gras"] = Const.StyleDeTexte(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.BOLD, False),wx.BLACK)

# Les différents styles de texte ...
#Styles = {"Titre"     :     rt.RichTextParagraphStyleDefinition(). \
#                            SetStyle(wx.RichTextAttr().
#                                     SetFontSize(20)),
#          "Titre 1"   :     rt.RichTextParagraphStyleDefinition(). \
#                            SetStyle(wx.RichTextAttr().
#                                     SetFontSize(14)),
#          "Sous titre":     rt.RichTextParagraphStyleDefinition(). \
#                            SetStyle(wx.RichTextAttr().
#                                     SetFontSize(8).
#                                     SetFontStyle(1))}
#Styles = {"Titre"     :     rt.TextAttrEx(),
#          "Titre 1"   :     rt.TextAttrEx(),
#          "Titre 2"   :     rt.TextAttrEx(),
#          "Message"   :     rt.TextAttrEx(),
#          "Sous titre":     rt.TextAttrEx()}
Styles = {"Titre"     :     rt.RichTextAttr(),
          "Titre 1"   :     rt.RichTextAttr(),
          "Titre 2"   :     rt.RichTextAttr(),
          "Message"   :     rt.RichTextAttr(),
          "MessSens"  :     rt.RichTextAttr(),
          "Sous titre":     rt.RichTextAttr(),
          "Tableau"   :     rt.RichTextAttr()}

Styles["Titre"].SetParagraphStyleName("Titre")
Styles["Titre"].SetFontSize(20)
Styles["Titre"].SetTextColour((0,0,0))
Styles["Titre"].SetParagraphSpacingBefore(40)
Styles["Titre"].SetAlignment(wx.TEXT_ALIGNMENT_CENTRE)

Styles["Titre 1"].SetParagraphStyleName("Titre 1")
Styles["Titre 1"].SetFontSize(14)
Styles["Titre 1"].SetTextColour((0,0,255))
Styles["Titre 2"].SetParagraphSpacingBefore(20)
Styles["Titre 1"].SetParagraphSpacingAfter(10)
Styles["Titre 1"].SetBulletStyle(wx.TEXT_ATTR_BULLET_STYLE_RIGHT_PARENTHESIS)
Styles["Titre 1"].SetFontUnderlined(True)

Styles["Titre 2"].SetParagraphStyleName("Titre 2")
Styles["Titre 2"].SetFontSize(12)
Styles["Titre 2"].SetTextColour((0,0,160))
Styles["Titre 2"].SetParagraphSpacingAfter(0)
Styles["Titre 2"].SetParagraphSpacingBefore(20)
Styles["Titre 2"].SetFontUnderlined(True)

Styles["Message"].SetParagraphStyleName("Message")
Styles["Message"].SetFontSize(12)
#Styles["Message"].SetFontStyle(wx.BOLD)
Styles["Message"].SetParagraphSpacingAfter(10)
Styles["Message"].SetParagraphSpacingBefore(10)

Styles["MessSens"].SetParagraphStyleName("MessSens")
Styles["MessSens"].SetFontSize(10)
Styles["MessSens"].SetTextColour((0,0,0))
#Styles["Message"].SetFontStyle(wx.BOLD)
Styles["MessSens"].SetParagraphSpacingAfter(10)
Styles["MessSens"].SetParagraphSpacingBefore(10)
Styles["MessSens"].SetTabs((800, 2000))

Styles["Tableau"].SetParagraphStyleName("Tableau")
Styles["Tableau"].SetFontSize(10)
#Styles["Tableau"].SetTextColour((0,0,0))
#Styles["Message"].SetFontStyle(wx.BOLD)
#Styles["Tableau"].SetParagraphSpacingAfter(10)
#Styles["Tableau"].SetParagraphSpacingBefore(10)

Styles["Sous titre"].SetFontSize(8)
Styles["Sous titre"].SetFontStyle(wx.ITALIC)#rt.TEXT_ATTR_FONT_ITALIC)
Styles["Sous titre"].SetAlignment(wx.TEXT_ALIGNMENT_CENTRE)

class FrameRapport(wx.Frame):
    def __init__(self, parent, options, fichierCourant, analyse, zoneMtg, CdCF, 
                 SchemaPanel, panelEtanch, panelDevis, panelResist):
        wx.Frame.__init__(self, parent, -1, u"Rapport d'analyse",
                            size=(700, 500))#,
#                            style = wx.DEFAULT_FRAME_STYLE)
        
        self.SetMinSize((700, -1))
        
        charger_styleText()
        self.options = options
        self.parent = parent
        
        icon = Icones.getIconeFenetreIcon()
        self.SetIcon(icon)
        
        self.MakeMenuBar()
        self.MakeToolBar()
        self.CreateStatusBar()
        self.SetStatusText(u"Rapport d'analyse")
        
        self.rtp = RTPrinting(self)
        
        #
        # Instanciation du rapport en RTF
        #
        self.rtc = RapportRTF(self)#rt.RichTextCtrl(self, style=wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER)
        wx.CallAfter(self.rtc.SetFocus)
        
        self.rtc.Freeze()
        self.rtc.BeginSuppressUndo()
        
        #
        # On rempli le rapport
        #
        
        progBarr = Progression(parent, "Création du rapport ...")
        progBarr.Show()
        
        self.rtc.AddTitre(fichierCourant)

        if options["ImpMontage"]:
            self.rtc.AddMontage(zoneMtg)
        
        progBarr.Avancer(5)
        
        if options["ImpCdCFCharge"] or options["ImpCdCFEtanch"] or options["ImpCdCFCout"]:
            self.rtc.AddTitreCdCF()
            if options["ImpCdCFCharge"]:
                self.rtc.AddCdCFCharges(CdCF, SchemaPanel)
            if options["ImpCdCFEtanch"]:
                self.rtc.AddCdCFEtanch(CdCF)
            if options["ImpCdCFCout"]:
                self.rtc.AddCdCFCoutMax(CdCF)
            
        progBarr.Avancer(10)
        
        if not analyse.montageVide and (options["ImpAnImmob"] or options["ImpAnStruc"]):
            self.rtc.AddTitreAnImmob()
            if options["ImpAnImmob"]:
                self.rtc.AddAnImmob(analyse, zoneMtg)
            if options["ImpAnStruc"]:
                self.rtc.AddAnStruc(analyse, zoneMtg)
            
        progBarr.Avancer(15)
        
        if not analyse.montageVide and (options["ImpAnResistAx"] or options["ImpAnResistRl"]):
            self.rtc.AddTitreAnCharg()
            self.rtc.AddCdCFCharges(CdCF, SchemaPanel)
            if options["ImpAnResistAx"]:
                self.rtc.AddAnResistMtg(analyse, zoneMtg)
            if options["ImpAnResistRl"]:
                self.rtc.AddAnResistRlt(analyse, zoneMtg, panelResist)
            
        progBarr.Avancer(20)
        
        if not analyse.montageVide and (options["ImpAnMontabEns"] or options["ImpAnMontabRlt"]):
            self.rtc.AddTitreAnMontab(analyse)
            if options["ImpAnMontabEns"]:
                self.rtc.AddAnMontabEns(analyse, zoneMtg)
            if options["ImpAnMontabRlt"]:
                self.rtc.AddAnMontabRlt(analyse, zoneMtg)
#
        progBarr.Avancer(30)
        
        if options["ImpAnEtanch"]:
            self.rtc.AddAnEtanch(analyse, panelEtanch, CdCF)
#            
        progBarr.Avancer(10)
        
        if not analyse.montageVide and options["ImpAnCout"]:
            self.rtc.AddAnCout(analyse, panelDevis, CdCF)
        
        progBarr.Avancer(100)

        self.rtc.EndSuppressUndo()
        self.rtc.Thaw()
        
#        sizer = wx.BoxSizer(wx.VERTICAL)
#        sizer.Add(self.rtc, flag = wx.EXPAND)
#        self.SetSizer(sizer)
#        self.Bind(wx.EVT_CLOSE, self.quitter )

    def quitter(self, event):
        event.Skip()
        self.Destroy()
        
    def AddRTCHandlers(self):
        # make sure we haven't already added them.
        if rt.RichTextBuffer.FindHandlerByType(rt.RICHTEXT_TYPE_HTML) is not None:
            return
        
        rt.RichTextBuffer.GetHandlers()[0].SetEncoding("iso-8859-1")
#        f = rt.RichTextFileHandler()#.SetEncoding("iso-8859-1")
        # This would normally go in your app's OnInit method.  I'm
        # not sure why these file handlers are not loaded by
        # default by the C++ richtext code, I guess it's so you
        # can change the name or extension if you wanted...
        HTML = rt.RichTextHTMLHandler()
        HTML.SetEncoding("latin_1")#"iso-8859-1")
        rt.RichTextBuffer.AddHandler(HTML)
        rt.RichTextBuffer.AddHandler(rt.RichTextXMLHandler())
#        rt.RichTextBuffer.AddHandler(rt.RICHTEXT_TYPE_RTF)
        # This is needed for the view as HTML option since we tell it
        # to store the images in the memory file system.
        wx.FileSystem.AddHandler(wx.MemoryFSHandler())


        
    def OnFileSave(self, evt):
        if not self.rtc.GetFilename():
            self.OnFileSaveAs(evt)
            return
        self.rtc.SaveFile()

    def OnFileSaveAs(self, evt):
        wildcard, types = rt.RichTextBuffer.GetExtWildcard(save=True)

        dlg = wx.FileDialog(self, "Enregistrer le rapport",
                            wildcard=wildcard,
                            style=wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            if path:
                fileType = types[dlg.GetFilterIndex()]
                ext = rt.RichTextBuffer.FindHandlerByType(fileType).GetExtension()
                if not path.endswith(ext):
                    path += '.' + ext
                self.rtc.SaveFile(path, fileType)
        dlg.Destroy()
              
    def OnApplyStyle(self, evt):
#        self.rtc.ApplyStyle(Styles[evt.GetString()])
        self.rtc.SetStyle(self.rtc.GetSelectionRange(), Styles[evt.GetString()])
    
    def OnFileExit(self, evt):
        self.Close(True)

    def OnBold(self, evt):
        self.rtc.ApplyBoldToSelection()
        
    def OnItalic(self, evt): 
        self.rtc.ApplyItalicToSelection()
        
    def OnUnderline(self, evt):
        self.rtc.ApplyUnderlineToSelection()
        
    def OnAlignLeft(self, evt):
        self.rtc.ApplyAlignmentToSelection(wx.TEXT_ALIGNMENT_LEFT)
        
    def OnAlignRight(self, evt):
        self.rtc.ApplyAlignmentToSelection(wx.TEXT_ALIGNMENT_RIGHT)
        
    def OnAlignCenter(self, evt):
        self.rtc.ApplyAlignmentToSelection(wx.TEXT_ALIGNMENT_CENTRE)
        
    def OnIndentMore(self, evt):
        attr = rt.RichTextAttr()
        attr.SetFlags(wx.TEXT_ATTR_LEFT_INDENT)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection():
                r = self.rtc.GetSelectionRange()

            attr.SetLeftIndent(attr.GetLeftIndent() + 100)
            attr.SetFlags(wx.TEXT_ATTR_LEFT_INDENT)
            self.rtc.SetStyle(r, attr)
       
    def OnIndentLess(self, evt):
        attr = rt.RichTextAttr()
        attr.SetFlags(wx.TEXT_ATTR_LEFT_INDENT)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection():
                r = self.rtc.GetSelectionRange()

        if attr.GetLeftIndent() >= 100:
            attr.SetLeftIndent(attr.GetLeftIndent() - 100)
            attr.SetFlags(wx.TEXT_ATTR_LEFT_INDENT)
            self.rtc.SetStyle(r, attr)

    def OnParagraphSpacingMore(self, evt):
        attr = rt.RichTextAttr()
        attr.SetFlags(wx.TEXT_ATTR_PARA_SPACING_AFTER)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection():
                r = self.rtc.GetSelectionRange()

            attr.SetParagraphSpacingAfter(attr.GetParagraphSpacingAfter() + 20);
            attr.SetFlags(wx.TEXT_ATTR_PARA_SPACING_AFTER)
            self.rtc.SetStyle(r, attr)
  
    def OnParagraphSpacingLess(self, evt):
        attr = rt.RichTextAttr()
        attr.SetFlags(wx.TEXT_ATTR_PARA_SPACING_AFTER)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection():
                r = self.rtc.GetSelectionRange()

            if attr.GetParagraphSpacingAfter() >= 20:
                attr.SetParagraphSpacingAfter(attr.GetParagraphSpacingAfter() - 20);
                attr.SetFlags(wx.TEXT_ATTR_PARA_SPACING_AFTER)
                self.rtc.SetStyle(r, attr)

    def OnLineSpacingSingle(self, evt): 
        attr = rt.RichTextAttr()
        attr.SetFlags(wx.TEXT_ATTR_LINE_SPACING)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection():
                r = self.rtc.GetSelectionRange()

            attr.SetFlags(wx.TEXT_ATTR_LINE_SPACING)
            attr.SetLineSpacing(10)
            self.rtc.SetStyle(r, attr)
      
    def OnLineSpacingHalf(self, evt):
        attr = rt.RichTextAttr()
        attr.SetFlags(wx.TEXT_ATTR_LINE_SPACING)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection():
                r = self.rtc.GetSelectionRange()

            attr.SetFlags(wx.TEXT_ATTR_LINE_SPACING)
            attr.SetLineSpacing(15)
            self.rtc.SetStyle(r, attr)

    def OnLineSpacingDouble(self, evt):
        attr = rt.RichTextAttr()
        attr.SetFlags(wx.TEXT_ATTR_LINE_SPACING)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection():
                r = self.rtc.GetSelectionRange()

            attr.SetFlags(wx.TEXT_ATTR_LINE_SPACING)
            attr.SetLineSpacing(20)
            self.rtc.SetStyle(r, attr)
            
    def OnFont(self, evt):
        if not self.rtc.HasSelection():
            return

        r = self.rtc.GetSelectionRange()
        fontData = wx.FontData()
        fontData.EnableEffects(False)
        attr = rt.RichTextAttr()
        attr.SetFlags(wx.TEXT_ATTR_FONT)
        if self.rtc.GetStyle(self.rtc.GetInsertionPoint(), attr):
            fontData.SetInitialFont(attr.GetFont())

        dlg = wx.FontDialog(self, fontData)
        if dlg.ShowModal() == wx.ID_OK:
            fontData = dlg.GetFontData()
            font = fontData.GetChosenFont()
            if font:
                attr.SetFlags(wx.TEXT_ATTR_FONT)
                attr.SetFont(font)
                self.rtc.SetStyle(r, attr)
        dlg.Destroy()

    def OnColour(self, evt):
        colourData = wx.ColourData()
        attr = rt.RichTextAttr()
        attr.SetFlags(wx.TEXT_ATTR_TEXT_COLOUR)
        if self.rtc.GetStyle(self.rtc.GetInsertionPoint(), attr):
            colourData.SetColour(attr.GetTextColour())

        dlg = wx.ColourDialog(self, colourData)
        if dlg.ShowModal() == wx.ID_OK:
            colourData = dlg.GetColourData()
            colour = colourData.GetColour()
            if colour:
                if not self.rtc.HasSelection():
                    self.rtc.BeginTextColour(colour)
                else:
                    r = self.rtc.GetSelectionRange()
                    attr.SetFlags(wx.TEXT_ATTR_TEXT_COLOUR)
                    attr.SetTextColour(colour)
                    self.rtc.SetStyle(r, attr)
        dlg.Destroy()
        
    def OnUpdateBold(self, evt):
        evt.Check(self.rtc.IsSelectionBold())
    
    def OnUpdateItalic(self, evt): 
        evt.Check(self.rtc.IsSelectionItalics())
    
    def OnUpdateUnderline(self, evt): 
        evt.Check(self.rtc.IsSelectionUnderlined())
    
    def OnUpdateAlignLeft(self, evt):
        evt.Check(self.rtc.IsSelectionAligned(wx.TEXT_ALIGNMENT_LEFT))
        
    def OnUpdateAlignCenter(self, evt):
        evt.Check(self.rtc.IsSelectionAligned(wx.TEXT_ALIGNMENT_CENTRE))
        
    def OnUpdateAlignRight(self, evt):
        evt.Check(self.rtc.IsSelectionAligned(wx.TEXT_ALIGNMENT_RIGHT))

    def ForwardEvent(self, evt):
        # The RichTextCtrl can handle menu and update events for undo,
        # redo, cut, copy, paste, delete, and select all, so just
        # forward the event to it.
        self.rtc.ProcessEvent(evt)

    def MakeMenuBar(self):
        def doBind(item, handler, updateUI=None):
            self.Bind(wx.EVT_MENU, handler, item)
            if updateUI is not None:
                self.Bind(wx.EVT_UPDATE_UI, updateUI, item)
            
        fileMenu = wx.Menu()
        doBind( fileMenu.Append(-1, "&Enregistrer\tCtrl+S", "Enregistrer le rapport"),
                self.OnFileSave )
        doBind( fileMenu.Append(-1, "&Enregistrer sous...\tF12", "Enregistrer le rapport"),
                self.OnFileSaveAs )
        fileMenu.AppendSeparator()
        doBind( fileMenu.Append(-1, "&Mise en Page...", "Règle la mise en page de l'impression"),
                self.OnPageSetup )
        doBind( fileMenu.Append(-1, "&Aperçu avant impression...", "Affiche un aperçu de ce qui sera imprimé"),
                self.OnPrintPreview )
        doBind( fileMenu.Append(-1, "&Imprimer\tCtrl+S", "Affiche un aperçu de ce qui sera imprimé"),
                self.OnDoPrint )
        fileMenu.AppendSeparator()
        doBind( fileMenu.Append(-1, "&Quitter\tCtrl+Q", "Quitter le visualisateur de rapport"),
                self.OnFileExit )
    
        
        fileMenu.AppendSeparator()

        
        editMenu = wx.Menu()
        doBind( editMenu.Append(wx.ID_UNDO, "&Annuler\tCtrl+Z"),
                self.ForwardEvent, self.ForwardEvent)
        doBind( editMenu.Append(wx.ID_REDO, "&Rétablir\tCtrl+Y"),
                self.ForwardEvent, self.ForwardEvent )
        editMenu.AppendSeparator()
        doBind( editMenu.Append(wx.ID_CUT, "Co&uper\tCtrl+X"),
                self.ForwardEvent, self.ForwardEvent )
        doBind( editMenu.Append(wx.ID_COPY, "&Copier\tCtrl+C"),
                self.ForwardEvent, self.ForwardEvent)
        doBind( editMenu.Append(wx.ID_PASTE, "Co&ller\tCtrl+V"),
                self.ForwardEvent, self.ForwardEvent)
        doBind( editMenu.Append(wx.ID_CLEAR, "&E&ffacer\tDel"),
                self.ForwardEvent, self.ForwardEvent)
        editMenu.AppendSeparator()
        doBind( editMenu.Append(wx.ID_SELECTALL, "Selectionner tout\tCtrl+A"),
                self.ForwardEvent, self.ForwardEvent )
        
        #doBind( editMenu.AppendSeparator(),  )
        #doBind( editMenu.Append(-1, "&Find...\tCtrl+F"),  )
        #doBind( editMenu.Append(-1, "&Replace...\tCtrl+R"),  )

        formatMenu = wx.Menu()
        doBind( formatMenu.AppendCheckItem(-1, "&Gras\tCtrl+B"),
                self.OnBold, self.OnUpdateBold)
        doBind( formatMenu.AppendCheckItem(-1, "&Italic\tCtrl+I"),
                self.OnItalic, self.OnUpdateItalic)
        doBind( formatMenu.AppendCheckItem(-1, "&Souligné\tCtrl+U"),
                self.OnUnderline, self.OnUpdateUnderline)
        formatMenu.AppendSeparator()
        doBind( formatMenu.AppendCheckItem(-1, "Aligner à &gauche"),
                self.OnAlignLeft, self.OnUpdateAlignLeft)
        doBind( formatMenu.AppendCheckItem(-1, "&Centrer"),
                self.OnAlignCenter, self.OnUpdateAlignCenter)
        doBind( formatMenu.AppendCheckItem(-1, "Aligner à &droite"),
                self.OnAlignRight, self.OnUpdateAlignRight)
        formatMenu.AppendSeparator()
        doBind( formatMenu.Append(-1, "&Indenter"), self.OnIndentMore)
        doBind( formatMenu.Append(-1, "&Desindenter"), self.OnIndentLess)
        formatMenu.AppendSeparator()
        doBind( formatMenu.Append(-1, "&Augmenter l'espace entre paragraphe"), self.OnParagraphSpacingMore)
        doBind( formatMenu.Append(-1, "&Diminuer l'espace entre paragraphe"), self.OnParagraphSpacingLess)
        formatMenu.AppendSeparator()
        doBind( formatMenu.Append(-1, "Interligne &simple"), self.OnLineSpacingSingle)
        doBind( formatMenu.Append(-1, "Interligne &x1.5"), self.OnLineSpacingHalf)
        doBind( formatMenu.Append(-1, "Interligne &double"), self.OnLineSpacingDouble)
        formatMenu.AppendSeparator()
        doBind( formatMenu.Append(-1, "&Police..."), self.OnFont)

        mb = wx.MenuBar()
        mb.Append(fileMenu, "&Fichier")
        mb.Append(editMenu, "&Edition")
        self.SetMenuBar(mb)

    def MakeToolBar(self):
        def doBind(tool, handler, updateUI=None):
            self.Bind(wx.EVT_TOOL, handler, tool)
            if updateUI is not None:
                self.Bind(wx.EVT_UPDATE_UI, updateUI, tool)

        tbar = self.CreateToolBar()

        tool = tbar.AddTool(wx.NewIdRef(), "Enregistrer", _rt_save.GetBitmap())
        tool.SetShortHelp("Enregistrer")
        doBind(tool, self.OnFileSave)

        bmp = Icones.getBout_ImprimerBitmap().ConvertToImage().Rescale(17, 17, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
        tool = tbar.AddTool(wx.NewIdRef(), "Imprimer", bmp)
        tool.SetShortHelp("Imprimer le rapport")
        doBind(tool, self.OnDoPrint)

        tbar.AddSeparator()

        tool = tbar.AddTool(wx.ID_UNDO, "Undo", _rt_undo.GetBitmap())
        tool.SetShortHelp(u"Annuler")
        doBind(tool, self.ForwardEvent, self.ForwardEvent)

        tool = tbar.AddTool(wx.ID_REDO, "Redo", _rt_redo.GetBitmap())
        tool.SetShortHelp(u"Rétablir")
        doBind(tool, self.ForwardEvent, self.ForwardEvent)

        tbar.AddSeparator()

        tool = tbar.AddTool(wx.ID_CUT, "Cut", _rt_cut.GetBitmap())
        tool.SetShortHelp(u"Couper dans le presse-papier")
        doBind(tool, self.ForwardEvent, self.ForwardEvent)

        tool = tbar.AddTool(wx.ID_COPY, "Copy", _rt_copy.GetBitmap())
        tool.SetShortHelp(u"Copier dans le presse-papier")
        doBind(tool, self.ForwardEvent, self.ForwardEvent)

        tool = tbar.AddTool(wx.ID_PASTE, "Paste", _rt_paste.GetBitmap())
        tool.SetShortHelp(u"Coller depuis le presse-papier")
        doBind(tool, self.ForwardEvent, self.ForwardEvent)

        tbar.AddSeparator()

        # For toggle tools, use wx.ITEM_CHECK in AddTool
        tool = tbar.AddTool(wx.NewIdRef(), "", _rt_bold.GetBitmap(), kind=wx.ITEM_CHECK)
        tool.SetShortHelp(u"Gras")
        doBind(tool, self.OnBold, self.OnUpdateBold)

        tool = tbar.AddTool(wx.NewIdRef(), "", _rt_italic.GetBitmap(), kind=wx.ITEM_CHECK)
        tool.SetShortHelp(u"Italic")
        doBind(tool, self.OnItalic, self.OnUpdateItalic)

        tool = tbar.AddTool(wx.NewIdRef(), "", _rt_underline.GetBitmap(), kind=wx.ITEM_CHECK)
        tool.SetShortHelp(u"Souligné")
        doBind(tool, self.OnUnderline, self.OnUpdateUnderline)

        tbar.AddSeparator()

        tool = tbar.AddTool(wx.NewIdRef(), "", _rt_alignleft.GetBitmap(), kind=wx.ITEM_CHECK)
        tool.SetShortHelp(u"Aligner à gauche")
        doBind(tool, self.OnAlignLeft, self.OnUpdateAlignLeft)

        tool = tbar.AddTool(wx.NewIdRef(), "", _rt_centre.GetBitmap(), kind=wx.ITEM_CHECK)
        tool.SetShortHelp(u"Centrer")
        doBind(tool, self.OnAlignCenter, self.OnUpdateAlignCenter)

        tool = tbar.AddTool(wx.NewIdRef(), "", _rt_alignright.GetBitmap(), kind=wx.ITEM_CHECK)
        tool.SetShortHelp(u"Aligner à droite")
        doBind(tool, self.OnAlignRight, self.OnUpdateAlignRight)

        tbar.AddSeparator()

        tool = tbar.AddTool(wx.NewIdRef(), "", _rt_indentless.GetBitmap())
        tool.SetShortHelp("Indenter")
        doBind(tool, self.OnIndentLess)

        tool = tbar.AddTool(wx.NewIdRef(), "", _rt_indentmore.GetBitmap())
        tool.SetShortHelp("Desindenter")
        doBind(tool, self.OnIndentMore)

        tbar.AddSeparator()

        tool = tbar.AddTool(wx.NewIdRef(), "", _rt_font.GetBitmap())
        tool.SetShortHelp("Police")
        doBind(tool, self.OnFont)

        tool = tbar.AddTool(wx.NewIdRef(), "", _rt_colour.GetBitmap())
        tool.SetShortHelp("Couleur de police")
        doBind(tool, self.OnColour)

        tbar.AddSeparator()

        tbar.AddControl(wx.ComboBox(tbar, wx.ID_ANY, "Styles", choices=list(Styles.keys()), size=(150, -1), style=wx.CB_DROPDOWN))
        self.Bind(wx.EVT_COMBOBOX, self.OnApplyStyle)

        tbar.Realize()

    def OnPageSetup(self, evt):
        self.rtp.PageSetup() 
#        psdd = wx.PageSetupDialogData(self.printData)
#        psdd.CalculatePaperSizeFromId()
#        dlg = wx.PageSetupDialog(self, psdd)
#        dlg.ShowModal()
#
#        # this makes a copy of the wx.PrintData instead of just saving
#        # a reference to the one inside the PrintDialogData that will
#        # be destroyed when the dialog is destroyed
#        self.printData = wx.PrintData( dlg.GetPageSetupData().GetPrintData() )
#
#        dlg.Destroy()

    def OnPrintPreview(self, event = None):
        self.rtp.PreviewBuffer(self.rtc.GetBuffer()) 
#        data = wx.PrintDialogData(self.printData)
#        printout = MyPrintout(self.rtc)
#        printout2 = MyPrintout(self.rtc)
#        self.preview = wx.PrintPreview(printout, printout2, data)
##        rtp = rt.RichTextPrinting()
##        rt.RichTextPrinting(self, "test").PreviewBuffer(self.rtc.GetBuffer())
#        if not self.preview.Ok():
#            print "Erreur Preview"
#            return
#
#        pfrm = wx.PreviewFrame(self.preview, self, "This is a print preview")
#
#        pfrm.Initialize()
#        pfrm.SetPosition(self.rtc.GetPosition())
#        pfrm.SetSize(self.rtc.GetSize())
#        pfrm.Show(True)

    def OnDoPrint(self, event = None):
        self.rtp.PrintBuffer(self.rtc.GetBuffer()) 
        
#        pdd = wx.PrintDialogData(self.printData)
#        pdd.SetToPage(2)
#        printer = wx.Printer(pdd)
#        printout = MyPrintout(self.rtc)
#
#        if not printer.Print(self.rtc, printout, True):
#            wx.MessageBox("There was a problem printing.\nPerhaps your current printer is not set correctly?", "Printing", wx.OK)
#        else:
#            self.printData = wx.PrintData( printer.GetPrintDialogData().GetPrintData() )
#        printout.Destroy()
        
    
class RapportRTF(rt.RichTextCtrl): 
    def __init__(self, parent):
        rt.RichTextCtrl.__init__(self, parent)
        self.parent = parent   
         
    def GetImageMontage(self, zoneMtg, analyse = None, reduc = 2, offsetX = 0, agrandi = 0):
        bmp = wx.Bitmap(zoneMtg.maxWidth + agrandi, zoneMtg.maxHeight)
        memdc = wx.MemoryDC(bmp)
        memdc.SetBackground(wx.WHITE_BRUSH)
        memdc.Clear()
        zoneMtg.DessineTout(memdc, analyse, offsetX = offsetX)
        memdc.SelectObject(wx.NullBitmap)
        img = bmp.ConvertToImage()
        img = img.Scale(bmp.GetWidth()//reduc,bmp.GetHeight()//reduc, wx.IMAGE_QUALITY_HIGH)
        return img
    
    def GetImageChaine(self, sens, analyse, zoneMtg):
        analyse.SetTracerChaine(sens, True)
        img = self.GetImageMontage(zoneMtg, analyse, 3)
        analyse.SetTracerChaine(sens, None)
        return img
    
    def GetImageArret(self, sens, analyse, zoneMtg):
        analyse.animerManqueArret(zoneMtg, sens, 1)
        img = self.GetImageMontage(zoneMtg, analyse, 3)
        analyse.animerManqueArret(zoneMtg, sens, -1)
        return img
    
    def GetImageChaineSurbrill(self, sens, analyse, zoneMtg):
        analyse.tracerSurbrillanceArrets(zoneMtg, sens, True, montrer = False)
        analyse.SetTracerChaine(sens, True)
        img = self.GetImageMontage(zoneMtg, analyse, 3)
        analyse.tracerSurbrillanceArrets(zoneMtg, sens, False, montrer = False)
        analyse.SetTracerChaine(sens, None)
        return img
    
    def GetImagesDemontageRlt(self, analyse, zoneMtg):
        if analyse.obstacleEnsble[0] == []:
            tagE = "AnimEnsb0"
            offsetX = DISTANCE_DEMONTAGE_RLT_COURT
        elif analyse.obstacleEnsble[1] == []:
            tagE = "AnimEnsb1"
            offsetX = 0
        else:
            return []

        analyse.animerMontageDemontage(zoneMtg, tagE ,False, instant = True)
        
        lstImages = []
        for palier in ["G","D"]:
            for sensR in [0,1]:
                lstObs = analyse.obstacleRoults[palier][sensR]
                if lstObs != []:
                    analyse.montrerCollision(zoneMtg, lstObs, palier, True, True)
                    lstImages.append(self.GetImageMontage(zoneMtg, analyse, 6))
                    analyse.montrerCollision(zoneMtg, lstObs, palier, False, True)
                else:
                    tag = "AnimRlt"+palier+str(sensR)
                    analyse.animerMontageDemontage(zoneMtg, tag ,False, instant = True)
                    lstImages.append(self.GetImageMontage(zoneMtg, analyse, 6, 
                                                          offsetX = offsetX*sensR,
                                                          agrandi = DISTANCE_DEMONTAGE_RLT_COURT))
                    analyse.animerMontageDemontage(zoneMtg, tag ,True, instant = True)
        
        analyse.animerMontageDemontage(zoneMtg, tagE ,True, instant = True)
        return lstImages


    def GetImagesDemontageEns(self, analyse, zoneMtg):
        lstImagesEns = []
        for sens in [0,1]:
            lstObs = analyse.obstacleEnsble[sens]
            if lstObs != []: 
                analyse.tracerSurBrillanceMobiles(zoneMtg, sens , True)
                analyse.montrerCollision(zoneMtg, lstObs, None, True, True)
                lstImagesEns.append(self.GetImageMontage(zoneMtg, analyse, 3))
                analyse.tracerSurBrillanceMobiles(zoneMtg, sens , False)
                analyse.montrerCollision(zoneMtg, lstObs, None, False, True)
                continue
            else:
                tag = "AnimEnsb"+str(sens)
                analyse.animerMontageDemontage(zoneMtg, tag ,False, instant = True)
                
                lstImagesEns.append(self.GetImageMontage(zoneMtg, None, 6, 
                                                      offsetX = DISTANCE_DEMONTAGE_ENSEMBLE*sens,
                                                      agrandi = DISTANCE_DEMONTAGE_ENSEMBLE))
                
                analyse.animerMontageDemontage(zoneMtg, tag ,True, instant = True)
                
        zoneMtg.Redessiner()
        return lstImagesEns
    
    ######################################################################################################
    def AddTitre(self, fichierCourant):
        self.AddParagraphStyled(u"Rapport d'analyse", "Titre")
        self.AddParagraphStyled(os.path.basename(os.path.splitext(fichierCourant)[0]), "Sous titre")
        self.AddParagraphStyled(wx.GetApp().auteur, "Sous titre")
        
        
    ######################################################################################################
    def AddMontage(self, zoneMtg):
        self.AddParagraphStyled(u"Montage :", "Titre 1")
        self.AddImage(self.GetImageMontage(zoneMtg))
        self.AppendText("\n")
        
        
    ######################################################################################################
    # CdCF
    ######################################################################################################
    def AddCdCFCharges(self, CdCF, SchemaPanel):
        self.AddParagraphStyled(u"Efforts sur l'arbre :", "Titre 2")
        bmp = SchemaPanel.BitmapSchemaAvecFleches(CdCF.bagueTournante)
        self.AddImage(bmp.ConvertToImage())
        
    def AddCdCFEtanchStat(self, CdCF):
        self.AddParagraphStyled(u"Indice de Pression : "+ str(CdCF.pression.get()), "MessSens")
        
    def AddCdCFEtanchDyn(self, CdCF):
        self.AddParagraphStyled(u"Indice de Vitesse : "+ str(CdCF.vitesse.get()), "MessSens")
    
    def AddCdCFEtanchLub(self, CdCF):
        self.AddParagraphStyled(u"Lubrifiant : "+ CdCF.lubrifiant.getCh(),"MessSens")
        
    def AddCdCFCoutMax(self, CdCF):
        self.AddParagraphStyled(u"Coût Maximum admissible : "+str(CdCF.coutMax),"MessSens")
        self.AppendText("\n")
        
    def AddTitreCdCF(self):
        self.AddParagraphStyled(u"Cahier des Charges Fonctionnel (CdCF) :", "Titre 1")
        
    def AddCdCFEtanch(self, CdCF):
        self.AddParagraphStyled(u"Lubrification - Etanchéité :", "Titre 2")
        self.AddCdCFEtanchStat(CdCF)
        self.AddCdCFEtanchDyn(CdCF)
        self.AddCdCFEtanchLub(CdCF)
        self.AppendText("\n")
        
    ######################################################################################################
    # Analyse   
    ######################################################################################################
    def AddTitreAnImmob(self):
        self.AddParagraphStyled(u"Structure du Montage :", "Titre 1")
        
    def AddAnImmob(self, analyse, zoneMtg):
        self.AddParagraphStyled(u"Mise en position axiale :", "Titre 2")
        
        # Message principal
        self.AddParagraphStyled(analyse.messageImmobilisation.mess, "Message", analyse.messageImmobilisation.coul)
        self.AppendText("\n")
        
        # Message par sens
        for s in [1,0]: # différents sens ...
            self.BeginStyle(Styles["MessSens"])
            self.BeginTextColour(Couleur[analyse.resultatImmobilisation[s][0].coul])
            mess = self.AppendText(analyse.resultatImmobilisation[s][0].mess)
            if s == 1: self.WriteText("\t")
        self.AppendText("\n")
        
        # Image par sens
        for s in [1,0]: # différents sens ...
            if analyse.resultatImmobilisation[s][0].clef == 'ArretArbreSens':
                img = self.GetImageArret(s, analyse, zoneMtg)
            elif analyse.resultatImmobilisation[s][0].clef == 'ImmobCorrect':
                img = self.GetImageChaine(s, analyse, zoneMtg)
            self.WriteImage(img)
            self.WriteText("\t")
        self.AppendText("\n")
            
    def AddAnStruc(self, analyse, zoneMtg):
        titre = self.AddParagraph(u"Schéma de Structure :")
        self.SetStyle(titre, Styles["Titre 2"])
        img = analyse.schemaStructure.bitmap().ConvertToImage()
        self.AddImage(img)
        self.AppendText("\n")
        
    ######################################################################################################
    def AddTitreAnCharg(self):
        self.AddParagraphStyled(u"Résistance aux charges :", "Titre 1")
    
    def AddAnResistMtg(self, analyse, zoneMtg):
        self.AddParagraphStyled(u"Résistance axiale du montage :", "Titre 2")
              
        # Message principal
        self.AddParagraphStyled(analyse.messageResistanceAxiale.mess, "Message", analyse.messageResistanceAxiale.coul)
        self.AppendText("\n")
        
        # Message par sens
        for s in [1,0]: # différents sens ...
            self.BeginStyle(Styles["MessSens"])
            self.BeginTextColour(Couleur[analyse.resultatEffortAxialMtg[s][0].coul])
            mess = self.AppendText(analyse.resultatEffortAxialMtg[s][0].mess)
            if s == 1: self.WriteText("\t")
        self.AppendText("\n")

        # Image par sens
        for s in [1,0]: # différents sens ...
            if analyse.resultatEffortAxialMtg[s][0].clef == 'ElemResistPas':
                img = self.GetImageChaineSurbrill(s, analyse, zoneMtg)
            elif analyse.resultatEffortAxialMtg[s][0].clef == 'ChargeAxOk':
                img = self.GetImageChaine(s, analyse, zoneMtg)
            elif analyse.resultatEffortAxialMtg[s][0].clef == 'ArretArbreSens':
                img = self.GetImageArret(s, analyse, zoneMtg)
            self.WriteImage(img)
            if s == 1: self.WriteText("\t")
        self.AppendText("\n")
    
    
    def AddAnResistRlt(self, analyse, zoneMtg, panelResist):
        self.AddParagraphStyled(u"Résistance des roulements :", "Titre 2")
        
        # Message principal
        self.AddParagraphStyled(analyse.messageResistanceAxiale.mess, "Message", analyse.messageResistanceAxiale.coul)
        self.AppendText("\n")
        
        # Schéma de structure
        img = analyse.imageSchemaCharges.ConvertToImage()
        self.AddImage(img)
        
        # Tableau
        self.AddGrid(panelResist.tableResist)
        
        self.AppendText("\n")
        
        
    ######################################################################################################
    def AddTitreAnMontab(self, analyse):
        self.AddParagraphStyled(u"Montabilité :", "Titre 1")
        
        self.AddParagraphStyled(analyse.resultatMontabilite.mess, "Message", analyse.resultatMontabilite.coul)
        
    def AddAnMontabEns(self, analyse, zoneMtg):
        if analyse.cdcf.bagueTournante == "I": ens = u"""arbre"""
        else: ens = u"""alésage"""
        self.AddParagraphStyled(u"Montabilité de l'ensemble "+ens+" :", "Titre 2")
        self.AppendText("")
        
        # Images pour "Montabilité"
        imagMontabiliteEns = self.GetImagesDemontageEns(analyse, zoneMtg)
        for img in imagMontabiliteEns:
            self.WriteImage(img)
            self.WriteText("\t")
        
    def AddAnMontabRlt(self, analyse, zoneMtg):
        self.AddParagraphStyled(u"Montabilité des Roulements :", "Titre 2")
        self.AppendText("")
        
        # Images pour "Montabilité"
        imagMontabiliteRlt = self.GetImagesDemontageRlt(analyse, zoneMtg)
        for img in imagMontabiliteRlt:
            self.WriteImage(img)
            self.WriteText("\t")
            
            
    ######################################################################################################
    def AddAnEtanch(self, analyse, panelEtanch, CdCF):
        self.AddParagraphStyled(u"Etanchéité :", "Titre 1")
        
        #
        # Etanchéité statique
        #
        self.AddParagraphStyled(u"Etanchéité Statique :", "Titre 2")
        
        # CdCF
        self.AddCdCFEtanchStat(CdCF)
        
        # Resultat principal
        message = analyse.resultatEtancheite["SB"]
        self.AddParagraphStyled(message.mess, "Message", message.coul)
        
        # Détails 
        if "SB+" in analyse.resultatEtancheite.keys():
            for mess in analyse.resultatEtancheite["SB+"]:
                self.AddParagraphStyled(mess.mess, "MessSens", mess.coul)

        self.AppendText("\n")
        self.AddGrid(panelEtanch.tableStat)
        
        #
        # Etanchéité Dynamique
        #
        if "DB" in analyse.resultatEtancheite:
            self.AddParagraphStyled(u"Etanchéité Dynamique :", "Titre 2")
            
            # CdCF
            self.AddCdCFEtanchDyn(CdCF)
            
            mess = analyse.resultatEtancheite["DB"]
            self.AddParagraphStyled(mess.mess, "Message", mess.coul)
            
            if "DB+" in analyse.resultatEtancheite.keys():
                for mess in analyse.resultatEtancheite["DB+"]:
                    self.AddParagraphStyled(mess.mess, "MessSens", mess.coul)

            self.AppendText("\n")
            self.AddGrid(panelEtanch.tableDyn)
        
        #
        # Compatibilité lubrifiant
        #
        self.AddParagraphStyled(u"Compatibilité lubrifiant :", "Titre 2")
        
        # CdCF
        self.AddCdCFEtanchLub(CdCF)
        
        mess = analyse.resultatEtancheite["C"]
        self.AddParagraphStyled(mess.mess, "Message", mess.coul)
        
        self.AppendText("\n")
                    
                    
                    
    ######################################################################################################
    def AddAnCout(self, analyse, panelDevis, CdCF):
        self.AddParagraphStyled(u"Devis (coût indicatif) :", "Titre 1")
        
        # CdCF
        self.AddCdCFCoutMax(CdCF)
        
        # Devis
        self.AppendText("\n")
        self.AddGrid(panelDevis.devis)


    def AddGrid(self, grid):
        
        debut = self.GetInsertionPoint()
    
        def SsRc(s):
            return s.replace("\n", " ")

        # Définition des tabs
        coef = 5
        tabs = [max(coef*grid.GetRowLabelSize(), 30)]
        for c in range(grid.GetNumberCols()):
            tabs.append(tabs[-1:][0]+coef*grid.GetColSize(c))
        Styles["Tableau"].SetTabs(tabs)
        
        # Affichage du contenu
        for l in range(1+grid.GetNumberRows()):
            ll = l-1
            for c in range(1+grid.GetNumberCols()):
                # Titres colonnes
                cc = c-1
                if l == 0 and c > 0:
                     self.BeginTextColour(wx.BLACK)
                     self.AppendText(SsRc(grid.GetColLabelValue(cc)))
                     
                # Titres lignes
                elif c == 0 and l > 0:
                    self.BeginTextColour(wx.BLACK)
                    self.AppendText(SsRc(grid.GetRowLabelValue(ll)))
                
                elif c == 0 and l == 0:
                    pass
                
                # Valeurs
                else:
                    self.BeginTextColour(grid.GetCellTextColour(ll,cc))
                    self.AppendText(SsRc(grid.GetCellValue(ll,cc)))
                
                self.AppendText("\t")
            self.AppendText("\n")
            
        fin = self.GetInsertionPoint()
        tout = self.GetRange(debut, fin)
        
        self.SetStyle((debut, fin), Styles["Tableau"])
        
        self.EndTextColour()
        
    def AddParagraphStyled(self, texte, style, couleur = None):
        
#        if style == "MessSens":
#            print(Styles[style].GetTextColour(), texte)
        
        if couleur is not None:
            if isinstance(couleur, wx.Colour):
                c = couleur
            else:
                c = Couleur[couleur]
#            cs = Styles[style].GetTextColour()
#            Styles[style].SetTextColour(c)
            self.BeginTextColour(c)
            
        parag = self.AddParagraph(texte)
        self.SetStyle(parag, Styles[style])
        
        self.EndTextColour()
#        if couleur is not None:
#            Styles[style].SetTextColour(cs)
        
        
#class RT_CdCF(rt.RichTextBuffer):#rt.RichTextBuffer
#    def __init__(self, CdCF):
#        rt.RichTextBuffer.__init__(self)
#        self.Construire(CdCF)
#        
#    def Construire(self, CdCF):
#        self.AddParagraph(u"Cahier des charges fonctionnel", Styles["Titre"])
##        titre = self.AddParagraph(u"Cahier des charges fonctionnel")
##        self.SetStyle(titre, Styles["Titre"])
#        
#    
        
class Progression(wx.Frame):
    def __init__(self, parent, texte = ""):
        wx.Frame.__init__(self, parent, -1, style = wx.STAY_ON_TOP | wx.BORDER_SIMPLE | 
                                                    wx.FRAME_NO_TASKBAR | wx.CLIP_CHILDREN )
        
        self.SetBackgroundColour(wx.WHITE)
        
        self.count = 0
        self.max = 100
        self.Center()
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        if texte != "":
            sizer.Add(wx.StaticText(self, -1, texte), 
                      flag = wx.EXPAND|wx.ALL, border = 5)
        
        self.g1 = wx.Gauge(self, -1, self.max, (110, 50), (250, 25))
        sizer.Add(self.g1, flag = wx.EXPAND|wx.ALL, border = 5)
        
        self.SetSizerAndFit(sizer)
        
        
        
#        self.Update()
        
        self.Avancer(1)
        

    def Avancer(self, npc):
        self.count = self.count + npc*self.max//100

        if self.count >= self.max:
            self.Close()

        self.g1.SetValue(self.count)
        self.Refresh()

        
class RTPrinting(rt.RichTextPrinting):
    def __init__(self, parent):
        rt.RichTextPrinting.__init__(self, "", parent)
        
        self.SetTitle("Rapport d'analyse")

        printData = wx.PrintData()
        printData.SetPaperId(wx.PAPER_A4)
        printData.SetPrintMode(wx.PRINT_MODE_PRINTER)
        printData.SetQuality(wx.PRINT_QUALITY_HIGH)
        self.SetPrintData(printData)
        
#        pageSetup = wx.PageSetupDialogData()
#        pageSetup.SetMarginTopLeft((15,20))
#        pageSetup.SetMarginBottomRight((15,30))
#        self.SetPageSetupData(pageSetup)
        
###################
#########################################################################################################
#class MyPrintout(wx.Printout):
#    def __init__(self, canvas):
#        wx.Printout.__init__(self)
#        self.canvas = canvas
#
#    def OnBeginDocument(self, start, end):
#        return super(MyPrintout, self).OnBeginDocument(start, end)
#
#    def OnEndDocument(self):
#        super(MyPrintout, self).OnEndDocument()
#
#    def OnBeginPrinting(self):
#        super(MyPrintout, self).OnBeginPrinting()
#
#    def OnEndPrinting(self):
#        super(MyPrintout, self).OnEndPrinting()
#
#    def OnPreparePrinting(self):
#        super(MyPrintout, self).OnPreparePrinting()
#
#    def HasPage(self, page):
#        if page <= 1:
#            return True
#        else:
#            return False
#
#    def GetPageInfo(self):
#        return (1, 1, 1, 1)
#
#    def OnPrintPage(self, page):
#        dc = self.GetDC()
#
#        #-------------------------------------------
#        # One possible method of setting scaling factors...
#
#        maxX = self.canvas.GetSizeTuple()[0]
#        maxY = self.canvas.GetSizeTuple()[1]
#
#        # Let's have at least 50 device units margin
#        marginX = 50
#        marginY = 50
#
#        # Add the margin to the graphic size
#        maxX = maxX + (2 * marginX)
#        maxY = maxY + (2 * marginY)
#
#        # Get the size of the DC in pixels
#        (w, h) = dc.GetSizeTuple()
#
#        # Calculate a suitable scaling factor
#        scaleX = float(w) / maxX
#        scaleY = float(h) / maxY
#
#        # Use x or y scaling factor, whichever fits on the DC
#        actualScale = min(scaleX, scaleY)
#
#        # Calculate the position on the DC for centering the graphic
#        posX = (w - (self.canvas.GetSizeTuple()[0] * actualScale)) / 2.0
#        posY = (h - (self.canvas.GetSizeTuple()[1] * actualScale)) / 2.0
#
#        # Set the scale and origin
#        dc.SetUserScale(actualScale, actualScale)
#        dc.SetDeviceOrigin(int(posX), int(posY))
#        dc.SetBackgroundMode(wx.TRANSPARENT)
#        dc.SetBackground(wx.TRANSPARENT_BRUSH)
#        #-------------------------------------------
#        print "Taille rapport", self.canvas.GetVirtualSize()[0] ,self.canvas.GetVirtualSize()[1]+50
#        bmp = wx.Bitmap(self.canvas.GetVirtualSize()[0] ,self.canvas.GetVirtualSize()[1]+50)
#        memdc = wx.MemoryDC(bmp)
#        memdc.SetBackground(wx.WHITE_BRUSH)
#        memdc.SetBackgroundMode(wx.TRANSPARENT)
#        memdc.Clear()
#
##        self.canvas.DessineTout(memdc)
#        
#        
#        
##        if self.app.fichierCourant  == None:
##            t = ''
##        else:
##            t = self.app.fichierCourant
##        memdc.DrawText(t , marginX//2, maxY+marginY)
#        
#        dc.Blit(0, 0, bmp.GetWidth() ,bmp.GetHeight(), 
#                memdc, 0, 0, wx.COPY, True)
#
#        return True


##import win32com.client
##import sys
##import os
##import datetime
##
##
##def f_lance_pdf( z_fichier_in, z_directory, z_fichier_out):
##    """ crée un fichier PDF sur base d'un fichier imprimable (XLS,DOC,...)
##    arguments :
##    le nom complet du fichier IN
##    le répertoire
##    le nom du fichier de sortie (sans .pdf car implicite)
##
##    """
##
##    pdfcreator1 = win32com.client.Dispatch('PDFCreator.clsPDFCreator')
##    pdfopt = win32com.client.Dispatch('PDFCreator.clsPDFCreatorOptions')
##    pdferror = win32com.client.Dispatch('PDFCreator.clsPDFCreatorError')
##
##
##    pdfcreator1.cStart("/NoProcessingAtStartup")
##
##    ## sauver imprimante par défaut
##
##    imprimante_defaut = pdfcreator1.cDefaultPrinter
##
##    ## AutoSaveFormat = 0 pour PDF
##
##    pdfcreator1.cOptions.AutosaveFormat = 0
##    pdfcreator1.cOptions.UseAutosave = 1
##    pdfcreator1.cOptions.UseAutosaveDirectory = 1
##    pdfcreator1.cOptions.AutosaveDirectory = z_directory
##    pdfcreator1.cOptions.SaveFilename = z_fichier_out
##    pdfcreator1.cOptions.ShowAnimation = 1
##    pdfcreator1.cOptions.StartStandardProgram = 0
##
##    pdfcreator1.cDefaultPrinter = "PDFCreator"
##    pdfcreator1.cClearCache
##
##    print "f_lance_pdf : traitement"
##    print "-----------------------------------------------"
##    print "imprimante par defaut : " , imprimante_defaut
##    print "redirection imprimante : " , pdfcreator1.cDefaultPrinter
##    print "existence du fichier ",z_fichier_in,") ", os.path.exists( z_fichier_in )
##    print "existence du répertoire ",z_directory ,") ", os.path.exists( z_directory )
##    print "use auto save : ", pdfcreator1.cOption("UseAutosave")
##    print "use auto save directory " , pdfcreator1.cOption("AutosaveDirectory")
##
##    print "rep sortie :" , z_directory
##    print "fichier OUT :" , pdfcreator1.cOption("AutosaveFilename") , "pdf"
##    print "fichier produit",pdfcreator1.cOutputFilename
##
##
##    print "lancement de l'impression ...", datetime.datetime.now()
##    print "le fichier est il imprimable" , pdfcreator1.cIsPrintable( z_fichier_in)
##    try:
##        pdfcreator1.cPrintFile( z_fichier_in )
##    except:
##        print "erreur impression"
##
##
##
####    pdfcreator1.cPrintPrinterTestpage()
##
##    print "impression en cours ..."
##
##    print "fin de l'impression", datetime.datetime.now()
##
##    pdfcreator1.cPrinterStop = False
##
##
#### print "sauver les options"
#### pdfopt = pdfcreator1.cReadOptionsFromFile("c:/IRSA_TEMPO/pdftest.ini")
#### pdfcreator1.cSaveOptionsToFile("c:/IRSA_TEMPO/pdftest.ini")
##
##
##
##
##    ## print "restaurer l'imprimante par défaut"
##    print "imprimante redéfinie : ", imprimante_defaut
##    pdfcreator1.cDefaultPrinter = imprimante_defaut
##    pdfcreator1.cClearCache
##    ## terminer proprement en fermant le lien COM et en effacant les objets.
##    pdfcreator1.cClose
##    del pdfcreator1
##    del pdfopt
##
##    ##----------------------------------------------------
##
##
##    
##
##    
#----------------------------------------------------------------------

#----------------------------------------------------------------------
_rt_save = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAPCAYAAADtc08vAAAABHNCSVQICAgIfAhkiAAAAQ1J"
    "REFUKJFjjE/L/c9AJlg0ZxojCwMDA8Oee78YvOzNGGbVJBHUFFc7hWHfiSsMLkpsDAwMDAws"
    "DAwMDPE+rgyvP39kYGBgYNi7bz9Ozc5Ojgww9U+vHUQYgE0RsQDDAGJcgNcAsl0gysvPEFc7"
    "haAGWRFJ3C5AlyTJBTCw7fxVvBq8DLVxG7Dt/FWG0kBLOF+In5eBn5eHgYeXl4Gfl49BTlKQ"
    "wTChCcUQDBcwMDAwlE1Zy6CppsrAwMDA0JTkjtdFTHhlGRgYfv3+x8D89wfD7z9/yDOA+d93"
    "hq9/WBh+/f2LVR7DC3KifAwrGhMZhKXkGTQVJAiZz8DIyMTMEJeSRXKOXDRnGiMDAwMDALeo"
    "P7cp9rvcAAAAAElFTkSuQmCC")


#----------------------------------------------------------------------
_rt_undo = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAPCAYAAADtc08vAAAABHNCSVQICAgIfAhkiAAAAhVJ"
    "REFUKJGNkstrE1EYxX8zmcSZZDJp2rSNfSg22CANYhYijWjAjcviwkVxW2hBVyZ/gZu6aOtK"
    "aLC7dicqwcdGiIrUoCIhpUVDsPZhq4GENqE2aUu5LuqkLxv94Fvce885995zPkmSLRxVffce"
    "ikQ6W123N7i41XOR65fPSeaeFH3wTAz390h7ib2D4+J9ZhGXajskWqxscq27C5MjP0nOEInF"
    "hQkIDgyJpeUCvjoVjyrjtCoAOK0KHlXGV6eSSGUZefxaACgu1cbH6W/0Do6LL/M5WjQNpyqz"
    "tb3NbKnClaCPwMlmpudzJFJZ/G4Hhm2b+OQMAApAp8fOykoRv9uBrlpYq+yQU6NRKbXn+ZFY"
    "XCzNLeN22Jj9UdoV0FU7umoHYK2yTmblF6nR6D5fAFobXRR/5tBVO07r+o6A06pgGM59QMOx"
    "9ddU4pMzhDu8ICtAHgAZwDhmrXZbYz3hDi/BgSFxUMBjkzA0jbXNMucDp3YEJJsVQ9cwdI1S"
    "uczCaoFsLl+N0ySHI/fF1eAZDF3j00KhGqOyWCgy8TZNa0sDXSeauNTuqw6KaWD37Zi4caGT"
    "ekPnXeYrp9uaePPnTKo1iSb5ZjjA8WY333N5JpKfeXm3f9dgSbYc2aHomHj6Ki2mMnPiUWJK"
    "hKJj4iBGrnV7yO/lrL+dfHGD4RcfSI70H4q25hdME0vlDZ7f6TtE/i8P/lW/AfYJsF99ZciZ"
    "AAAAAElFTkSuQmCC")

#----------------------------------------------------------------------
_rt_redo = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAPCAYAAADtc08vAAAABHNCSVQICAgIfAhkiAAAAg5J"
    "REFUKJGdkr9rU1EcxT/3vbz2vfS924qRpmopVmIsFCWDiFkCAXHs5CDoJqSrJIP+BS5tXCw0"
    "EHDo4FBUguDgULVQImJJLe0Qu2hqWyKNMT9q0p/XofRHmtrBA9/l3HPPPffcK4Sms4fxyRn1"
    "NDXFYqG0z4Wv+kg+uC34B8SeQTSRUq/S87SbLU2iUn2D6/5unj+612AUTaSUEJpO/OV7Nfb2"
    "Mx5TA2B9W6OyuYVjuGjVdxq4zGhMHD5QCE0nFB1RHl1h6DrZ4hrhgI/+nk7mvueZyCzQK00M"
    "XadS32G5VuNyTydLywUqm1u4AMprNXxdkmp9m3DAx3BkoPHOg0PKf6qNrg4Dx9TYKJa45HEz"
    "vVJGA3AMF7bpxjZ1zp1pb+ogMxoT2eIaAN4Oh+7THdimG2A3AYCUDtK2SE3NH9u2bLOwTTdS"
    "OvucY6zuGlzrv0C1XuOsI/G0NL9YYHBIhXq9SMtqWtMAhiMDYjpXQNoWtwJ9hKIjak9w5/GY"
    "AljIr5L7XaBcqyFtC2lbiBbj4B/cfzKupLZN0H+RX+Uqzz5+JR2PNMQZn5xR2cU887mfLC0X"
    "+FH5c2AAcPNhQt290cf5Tg8r+SIjH+aaTJogNL1hgrGkejExq2az39Trd19UMJZURzWHRztq"
    "mI5HxPCbT6yW1rni7ybo954YwHUcmY5HRNxOKmm1nrgZaOzgf/AXUUy2DjrCDG0AAAAASUVO"
    "RK5CYII=")

#----------------------------------------------------------------------
_rt_copy = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAPCAYAAADtc08vAAAABHNCSVQICAgIfAhkiAAAATlJ"
    "REFUKJGFk71OwzAURo/tpE2AdihiAAmQWNiKWICpDIhnQEi8A0+ASsXAzDsgIcTEA3QANsZu"
    "XTMQBiqkUkFF04aB2sRJSO90bV+f+33+EUIqzq7bMam471UA6JzuiPRaMqROltc2KS9tMFhY"
    "JVArAJw31qlfPWfguYCqp6j5Lou+S81XpmAWRGgLe1t13r8i+sMxYdAtasrFyYGx5eik4v11"
    "DYHW8T6dl0/6w4i3wYjXjxFh0KV51ADasYYYQNUzKXlQDQYsiNnluzLJA6CsBKQgrdtHa2x2"
    "zJdkeoq5koLvsYEc7m5bdqxqRwk8V5C4GFwlDCRKKdR2Egq01IkpUhJgCsmKtkdKJiHTOSFA"
    "xoWQ7NFbgF8F+ZAU4PLuKbMopYBJXAhxwH5ZgPW5ZkH+tdC8eShyZ+IHUNNZHhrzal0AAAAA"
    "SUVORK5CYII=")

#----------------------------------------------------------------------
_rt_alignleft = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAEJJ"
    "REFUOI1jZGRiZqAEMFGkm4GBgYWBgYHBx9vrPzmat2zdxshIqRdIcsGWrdsY0cXo6wJsLhoN"
    "g2ERBhRnJooNAACQdhhQZbXeGAAAAABJRU5ErkJggg==")

#----------------------------------------------------------------------
_rt_alignright = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAADxJ"
    "REFUOI1jZGRiZqAEMFGkm4GBgYWBgYHBx9vrPzmat2zdxshIqRdYsAkS6yLquWA0DEZ8GFCc"
    "mSg2AADQZxhQFG0xxgAAAABJRU5ErkJggg==")

#----------------------------------------------------------------------
_rt_bold = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAEtJ"
    "REFUOI3NUkEKACAMyq3//7jWNQwWY0HzKNOJCIi2DCSlfmHQmbA5zBNAFG4CPoAodo4fFOyA"
    "wZGvHTDqdwCecnQHh0EU/ztIGyy1dBRJuH/9MwAAAABJRU5ErkJggg==")

#----------------------------------------------------------------------
_rt_centre = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAEJJ"
    "REFUOI1jZGRiZqAEMFGkm4GBgYWBgYHBx9vrPzmat2zdxshIqRdYkDnEumTL1m2MMDZ1XDAa"
    "BiM+DCjOTBQbAAAwdhhQDziCqAAAAABJRU5ErkJggg==")

#----------------------------------------------------------------------
_rt_colour = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAPZJ"
    "REFUOI1jZGRiZqAEsOCS+Mcu9h+bONPPV4wofEKa37Lz4zWYEd0LuGzG5RKsLiAFDEIDllTz"
    "MWxtyGJ4yiWKofgfCyTSkGMCJRDd/hr/Z2BgYGCZ5cAg8v0jg++C9wy6zx8ysP37zfCYXYFh"
    "g1gww+VfUSiGwg2AaRZ/JcPw6v0fhv/qLxg4vv1jCOv5zPBvZgrDSukghp8/ZRkY/rFiGgDT"
    "jBV84mX4572WgekzL8O/v5hBxoRXMwMDw/+3QgwM/3CHNeFY+MvMwMDyE6vtRBnAKPqWgUH2"
    "OQUu4P/IwGh8HrcFBAORgYFhF/NZRhetP1jVAACsCFJPHjA77wAAAABJRU5ErkJggg==")


#----------------------------------------------------------------------
_rt_cut = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAPCAYAAADtc08vAAAABHNCSVQICAgIfAhkiAAAAbBJ"
    "REFUKJGdk0FLG1EQx3/vpRdv7sG49CKYxvSmVDwkpd78ALbSShQkbU81guAH8BN4EE0KGlCQ"
    "5iAIoiaIwWAP3bi0WXZLW1q2WfGmJ8mhV19Pu+xqWsSBx/Bm/vObmQcPIWP4Jz83r96vb6pw"
    "LJxzXfdWThKyuJR8/2rjOI4Kxz8ZDQUwkHosuGERwOLKsohLydpaKSIqfyjfrOsM8C2VSlKr"
    "1RRAtVJRAK8mJ+8GWFxZFldui93dPTzvTFWqhwCMPnt6a3yAB52CWjLBSCLBwcH+P0f/7wpX"
    "bouLywvys+/uB9CSCfRendVCkezMm/tN8PnwiKHBQX59axKXHWUACCFjAHyp15VX2gIgbdg0"
    "MkO8LG+I7WxO+XeARwt5ngwPBw8q/eLe1wtI75y25QTCsG9bDtI7p+fFW6xmU0UAXmkLU9eY"
    "OK0LNf0cIOji+4ezOSZO68LUNX4vrUbfIG3YXPf3AdD9o4Wpa5E9TV3jT8MC4Lq/j7RhRwGm"
    "rtG2HPx9u6bGI4CuqXHShs12NqfalhNtIGSMn8cnaiczpnYyY6paKHb8jdVCMdA0Tz4Gmr9P"
    "zKg0oZ3GfwAAAABJRU5ErkJggg==")

#----------------------------------------------------------------------
_rt_font = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAIpJ"
    "REFUOI21k8ENgCAMRSmMpwzAgenUsgDMhweCgUpRJDYhJG362v8DAFKJmZBT3W8A67LFz4Bj"
    "T835HgY4V99DADqV24IF5Kk+WOht0QTkabm5twW03kHPeQoVIFV1EDFqjZHmtU55xLp2k8Bp"
    "NaZdrwCcdhqlF5cHVHcJ4TzxwULTxJH4/zM9xQmi7UCACkKFWgAAAABJRU5ErkJggg==")

#----------------------------------------------------------------------
_rt_idea = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAVtJ"
    "REFUWIXtl2FOwkAQhd8u3gAJp1EXuQEBrmOU24DxBtoWjmA8BAlXsOsPXNjadjtvRImJ708T"
    "pnS+fTudnRpjezinLjR/Wq5K//W3+cwazbMM40BIPJ3c1GKPT4UKRASQShxruyuwWYMC6QRY"
    "rkpfTZwBGCUhAGCzlkFYCeUxcTW5Ma521/Ay7RIFcFx9VouF5E0QAHB13VysFEBd7dbHYlxo"
    "BUitXgohcYFwQLZ6VoJGpE+834oieQ9ZA5zCK3kWAEnyJMB8Zk1or1pJmpHaAe/zylUrRSvu"
    "VjgTJK1YdRwD1Q4YuyDd+6DOLWBqgT2IAGIekGwFY30QVYQpJ+JZgJEYILUqzSASRBXh2+sd"
    "Bn3XGBv0gTzPASyYR/JvwT7J6UQDOOdaYxq4fwcogPuHhQHQOuF8xilRHyaxspfnA8jodqz6"
    "KvoWgC/fDwDG9n4f4FT60ZHsTwB8AA6FjDfFEDh8AAAAAElFTkSuQmCC")

#----------------------------------------------------------------------
_rt_indentless = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAHRJ"
    "REFUOI3Nkm8KgCAMxfe2TlftCJ0u6ATa9eyTIqZiKdEDYfj25+eQwEKlo6qu5oOFABbq0eSD"
    "dZldbBh7Ir3LaSTB7ozdEJstBOyL3xJA9bgVpyTVBmAJBK1PMPYMefx0YpagR7/6B2WCeGnD"
    "CbhmfrKDC/GuLg9MR0atAAAAAElFTkSuQmCC")

#----------------------------------------------------------------------
_rt_indentmore = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAHlJ"
    "REFUOI3NkmEKgCAMhbfZ6aododMJncB5PftlTE2TkuiBID7f9jkEJAO1xcyh5SMZQCQDbzTF"
    "zbrMQRtOPOZnVxpJYIOTDbXZQ0BpwN4GciHzXoRykmaBOIPYXYdrT3DizzuUGv2dC4Kn+tU/"
    "qBPooQ0noJb5yQwOwa4uD/KzgEcAAAAASUVORK5CYII=")

#----------------------------------------------------------------------
_rt_italic = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAGdJ"
    "REFUOI3Vk1EOgDAIQwt4/2P0lopfS6YOgsEfl+xntK8kMBE1dI623F8Atqzox+73N1GTcgez"
    "mOTDPEThJekAHIBHmhQwzCTfAyrpKaCSHgKq6SGgmi5qkHmVV3Nfzf5S+/9faANOrocplI0e"
    "xSoAAAAASUVORK5CYII=")


#----------------------------------------------------------------------
_rt_paste = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAPCAYAAADtc08vAAAABHNCSVQICAgIfAhkiAAAAXNJ"
    "REFUKJGFkzsvREEYhp/vzDnWWHuxdnsJjd+wRKPYgkIUKqHVKtYlQoi4FX6BiGQTolEpFBIU"
    "/gUJtbXWdSMuo1jGHueceJvJN5nvmff9JiPiKH6UL5YMITrfGJWwfQARR5EvlsxY8pqr6gvL"
    "60u+A3NT8wCcOd2hICdfLJmT/k+AQPPPXke6hcP241CHbmOxtboW5TRS0jO9a06HM5j7MgAf"
    "lRsAzE2N15cLBm77A02NURxLSmUBUJlcvc5pYi1dAGxODDI7WgDgaHHEF8UBkERbJAQgrV2y"
    "rZ510AixM5BEG+bxDkllMfdlVCZn46T071MXFvZ9cVwAiScxzw+hEIAm5ZDSsD05RLX2Tvnp"
    "jZXS0S8AnUAgFALQ7AlQh/yVHSI6gcSTNo5vJiI0e/LtRJHWrh8gno6EAHhKLCTepHwzqaNi"
    "McRVmNpTIA5U6J3ZC3r3AZz6IroV3j8wYCFn4532cN/OZeA/uAC98weRN/ynL78NdulpYuMM"
    "AAAAAElFTkSuQmCC")



#----------------------------------------------------------------------
_rt_sample = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAMNJ"
    "REFUWIXtl0sawiAMhGcoN2mvqIeoV6RHUVwoC5VqiOkXFsyahJ+8ADJM8FRw3X0A9AAQfy3I"
    "t2vWOGaYaAIAAPN8atp82y7ite4pEAOktCKl1Q/gKLkDiIpQovfCk3aPGQAA5MaGJYGo7XMr"
    "RQD4RiCaJi8q3mSWHRVhSSDr5MtyPgTAPQJEOftOBFpq4OlIbElKbsOaIT5vO203uafAHcB0"
    "Ej7UNjk6isBO/7dI48IsBdI3YBXg/7PrxfE1GwDeAHen2yjnZJXsxQAAAABJRU5ErkJggg==")


#----------------------------------------------------------------------
_rt_underline = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAFdJ"
    "REFUOI1jZGRiZqAEMFGkmxoGsKAL/P/39z8yn5GJmRGbGE4XIEvC2NjEcBpAKhg1gIABS5cs"
    "/o9MYwOMuJIyetwzMGBGIV4DiAUEUyI2gJKwBjw3AgDOdhYrghF5ggAAAABJRU5ErkJggg==")
